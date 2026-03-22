const DAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];
const SLOTS = ['Frühstück', 'Vormittag', 'Mittagessen', 'Nachmittag', 'Abendessen'];

let weekStart = getMonday(new Date());
let activeDay = (() => {
    const d = new Date().getDay(); // 0=Sun
    return d === 0 ? 6 : d - 1;   // 0=Mon..6=Sun
})();

let plan = {}; // "dayIndex_slotIndex" -> { recipe_id, name }
let allRecipes = [];
let pickerTarget = null;

function getMonday(d) {
    d = new Date(d);
    const day = d.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    d.setDate(d.getDate() + diff);
    d.setHours(0, 0, 0, 0);
    return d;
}

function formatDate(d) {
    return `${d.getDate()}.${d.getMonth() + 1}.`;
}

function weekStartStr() {
    const y = weekStart.getFullYear();
    const m = String(weekStart.getMonth() + 1).padStart(2, '0');
    const day = String(weekStart.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function renderWeekLabel() {
    const end = new Date(weekStart);
    end.setDate(end.getDate() + 6);
    document.getElementById('wp-week-label').textContent =
        `${formatDate(weekStart)} – ${formatDate(end)}${end.getFullYear()}`;
}

function isToday(dayIndex) {
    const d = new Date(weekStart);
    d.setDate(d.getDate() + dayIndex);
    const t = new Date();
    return d.getFullYear() === t.getFullYear() &&
           d.getMonth() === t.getMonth() &&
           d.getDate() === t.getDate();
}

function renderDayTabs() {
    const container = document.getElementById('wp-day-tabs');
    container.innerHTML = DAYS.map((name, i) => {
        const d = new Date(weekStart);
        d.setDate(d.getDate() + i);
        const hasFilled = SLOTS.some((_, s) => plan[`${i}_${s}`]);
        const today = isToday(i);
        return `<div class="wp-day-tab${i === activeDay ? ' active' : ''}${hasFilled ? ' has-entries' : ''}${today ? ' today' : ''}" data-day="${i}">
            <div class="day-name">${today ? '•' + name : name}</div>
            <div class="day-date">${formatDate(d)}</div>
            <div class="day-dot"></div>
        </div>`;
    }).join('');
}

function renderSlots() {
    const container = document.getElementById('wp-slots');
    container.innerHTML = SLOTS.map((label, s) => {
        const key = `${activeDay}_${s}`;
        const entry = plan[key];
        const bought = entry && entry.is_bought;
        const inList = entry && !bought && entry.in_shopping_list;
        let slotClass = 'empty';
        let icon = '';
        if (bought)       { slotClass = 'bought';   icon = '<span class="wp-slot-icon">✓</span>'; }
        else if (inList)  { slotClass = 'in-list';  icon = '<span class="wp-slot-icon">🛒</span>'; }
        else if (entry)   { slotClass = 'filled'; }
        return `<div class="wp-slot">
            <span class="wp-slot-label">${label}</span>
            <div class="wp-slot-recipe ${slotClass}" data-day="${activeDay}" data-slot="${s}">
                <span class="wp-slot-recipe-name">${icon}${entry ? escHtml(entry.name) : '+ Rezept wählen'}</span>
            </div>
            ${entry && !bought ? `<button class="wp-slot-clear" data-day="${activeDay}" data-slot="${s}" title="Entfernen">✕</button>` : ''}
            ${entry && !bought && !inList ? `
            <div class="wp-slot-servings">
                <button class="wp-srv-btn" data-day="${activeDay}" data-slot="${s}" data-delta="-1">−</button>
                <span class="wp-srv-count">${entry.servings} Pers.</span>
                <button class="wp-srv-btn" data-day="${activeDay}" data-slot="${s}" data-delta="1">+</button>
            </div>` : ''}
            ${entry && !bought && inList ? `
            <div class="wp-slot-servings">
                <span class="wp-srv-count wp-srv-locked">${entry.servings} Pers.</span>
            </div>` : ''}
        </div>`;
    }).join('');
}

function setDay(i) {
    activeDay = i;
    renderDayTabs();
    renderSlots();
}

function render() {
    renderWeekLabel();
    renderDayTabs();
    renderSlots();
}

// ── Event delegation ──────────────────────────────────

document.getElementById('wp-day-tabs').addEventListener('click', e => {
    const tab = e.target.closest('.wp-day-tab');
    if (tab) setDay(parseInt(tab.dataset.day));
});

document.getElementById('wp-slots').addEventListener('click', e => {
    const recipe = e.target.closest('.wp-slot-recipe');
    if (recipe) { openPicker(parseInt(recipe.dataset.day), parseInt(recipe.dataset.slot)); return; }

    const srv = e.target.closest('.wp-srv-btn');
    if (srv) { changeServings(parseInt(srv.dataset.day), parseInt(srv.dataset.slot), parseInt(srv.dataset.delta)); return; }

    const clear = e.target.closest('.wp-slot-clear');
    if (clear) clearSlot(parseInt(clear.dataset.day), parseInt(clear.dataset.slot));
});

async function changeServings(day, slot, delta) {
    const key = `${day}_${slot}`;
    const entry = plan[key];
    if (!entry) return;
    const newServings = Math.max(1, (entry.servings || 1) + delta);
    entry.servings = newServings;
    // Update count display without full re-render
    const countEl = document.querySelector(`.wp-srv-btn[data-day="${day}"][data-slot="${slot}"][data-delta="-1"]`)
        ?.parentElement?.querySelector('.wp-srv-count');
    if (countEl) countEl.textContent = newServings;
    try {
        await fetch(`/api/wochenplan/${weekStartStr()}/${day}/${slot}/servings`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ servings: newServings })
        });
    } catch(e) {}
}

document.getElementById('wp-picker-list').addEventListener('click', e => {
    const item = e.target.closest('.wp-picker-item');
    if (item) selectRecipe(parseInt(item.dataset.id), item.dataset.name);
});

// ── Data loading ──────────────────────────────────────

async function loadWeek() {
    try {
        const r = await fetch(`/api/wochenplan/${weekStartStr()}`);
        const data = await r.json();
        plan = {};
        if (data.slots) {
            data.slots.forEach(s => {
                if (s.recipe_id) {
                    plan[`${s.day_index}_${s.slot_index}`] = {
                        recipe_id: s.recipe_id,
                        name: s.recipe_name,
                        servings: s.servings,
                        is_bought: s.is_bought,
                        in_shopping_list: s.in_shopping_list
                    };
                }
            });
        }
    } catch(e) {
        plan = {};
    }
}

async function loadRecipes() {
    if (allRecipes.length) return;
    try {
        const r = await fetch('/api/recipes/all');
        allRecipes = await r.json();
    } catch(e) {
        allRecipes = [];
    }
}

const TODAY_MONDAY = getMonday(new Date());

function updateNavButtons() {
    const msPerWeek = 7 * 24 * 3600 * 1000;
    const weeksAhead = (weekStart - TODAY_MONDAY) / msPerWeek;
    document.getElementById('wp-prev').disabled = weeksAhead <= 0;
    document.getElementById('wp-next').disabled = weeksAhead >= 2;
    document.getElementById('wp-today-bar').style.display = weeksAhead !== 0 ? 'flex' : 'none';
}

async function changeWeek(delta) {
    weekStart.setDate(weekStart.getDate() + delta * 7);
    weekStart = getMonday(weekStart);
    // On the current week land on today; on other weeks start at Monday
    const todayDayIndex = (() => { const d = new Date().getDay(); return d === 0 ? 6 : d - 1; })();
    activeDay = weekStart.getTime() === TODAY_MONDAY.getTime() ? todayDayIndex : 0;
    await loadWeek();
    render();
    updateNavButtons();
}

document.getElementById('wp-prev').addEventListener('click', () => changeWeek(-1));
document.getElementById('wp-next').addEventListener('click', () => changeWeek(1));
document.getElementById('wp-today-btn').addEventListener('click', async () => {
    const todayDayIndex = (() => { const d = new Date().getDay(); return d === 0 ? 6 : d - 1; })();
    weekStart = getMonday(new Date());
    activeDay = todayDayIndex;
    await loadWeek();
    render();
    updateNavButtons();
});

// ── Picker ────────────────────────────────────────────

function openPicker(day, slot) {
    pickerTarget = { day, slot };
    document.getElementById('wp-picker-search').value = '';
    filterPicker();
    document.getElementById('wp-picker-backdrop').style.display = 'block';
    document.getElementById('wp-picker').style.display = 'flex';
    document.getElementById('wp-picker-search').focus();
}

function closePicker() {
    document.getElementById('wp-picker-backdrop').style.display = 'none';
    document.getElementById('wp-picker').style.display = 'none';
    pickerTarget = null;
}

document.getElementById('wp-picker-backdrop').addEventListener('click', closePicker);

function filterPicker() {
    const q = document.getElementById('wp-picker-search').value.toLowerCase().trim();
    const filtered = allRecipes.filter(r => !q || r.name.toLowerCase().includes(q));

    const list = document.getElementById('wp-picker-list');
    if (!filtered.length) {
        list.innerHTML = '<div style="color:#aaa;padding:20px;text-align:center;">Keine Rezepte gefunden</div>';
        return;
    }

    const groups = {};
    filtered.forEach(r => {
        const cat = r.category || 'Sonstiges';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(r);
    });

    let html = '';
    Object.keys(groups).sort().forEach(cat => {
        if (!q) html += `<div class="wp-picker-category">${escHtml(cat)}</div>`;
        groups[cat].forEach(r => {
            html += `<div class="wp-picker-item" data-id="${r.id}" data-name="${escHtml(r.name)}">${escHtml(r.name)}</div>`;
        });
    });
    list.innerHTML = html;
}

async function selectRecipe(id, name) {
    if (!pickerTarget) return;
    const { day, slot } = pickerTarget;
    closePicker();

    try {
        const r = await fetch(`/api/wochenplan/${weekStartStr()}/${day}/${slot}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipe_id: id })
        });
        if (!r.ok) throw new Error();
        plan[`${day}_${slot}`] = { recipe_id: id, name, servings: 1, is_bought: false, in_shopping_list: false };
        renderDayTabs();
        renderSlots();
    } catch(e) {
        showToast('Fehler beim Speichern');
    }
}

async function clearSlot(day, slot) {
    try {
        await fetch(`/api/wochenplan/${weekStartStr()}/${day}/${slot}`, { method: 'DELETE' });
        delete plan[`${day}_${slot}`];
        renderDayTabs();
        renderSlots();
    } catch(e) {
        showToast('Fehler');
    }
}

// ── Shopping list button ──────────────────────────────

document.getElementById('wp-to-list-btn').addEventListener('click', async () => {
    if (!Object.keys(plan).length) {
        showToast('Keine Rezepte geplant');
        return;
    }
    try {
        const r = await fetch(`/api/wochenplan/${weekStartStr()}/to-shopping-list`, { method: 'POST' });
        const data = await r.json();
        if (data.success) {
            if (data.added > 0) {
                window.location.href = '/shopping-list/';
            } else {
                showToast('Keine neuen Rezepte');
            }
        } else {
            showToast(data.error || 'Fehler');
        }
    } catch(e) {
        showToast('Fehler');
    }
});

document.getElementById('wp-clear-btn').addEventListener('click', async () => {
    if (!confirm('Alle Einträge dieser Woche löschen?')) return;
    try {
        await fetch(`/api/wochenplan/${weekStartStr()}/clear`, { method: 'DELETE' });
        plan = {};
        renderDayTabs();
        renderSlots();
    } catch(e) {
        showToast('Fehler');
    }
});

function showToast(msg) {
    const t = document.getElementById('wp-toast');
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => t.style.display = 'none', 2500);
}

window.onload = async () => {
    await Promise.all([loadWeek(), loadRecipes()]);
    render();
    updateNavButtons();
};
