const DAYS  = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];
const SLOTS = ['Frühstück', 'Vormittag', 'Mittagessen', 'Nachmittag', 'Abendessen'];

let weekStart  = getMonday(new Date());
let activeDay  = (() => { const d = new Date().getDay(); return d === 0 ? 6 : d - 1; })();

// plan["day_slot"] = [ { id, recipe_id, name, servings, is_bought, in_shopping_list }, … ]
let plan       = {};
let allRecipes = [];
let pickerTarget = null;
let familySize   = 1.0;

function getMonday(d) {
    d = new Date(d);
    const day = d.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    d.setDate(d.getDate() + diff);
    d.setHours(0, 0, 0, 0);
    return d;
}

function formatDate(d) { return `${d.getDate()}.${d.getMonth() + 1}.`; }

function weekStartStr() {
    const y = weekStart.getFullYear();
    const m = String(weekStart.getMonth() + 1).padStart(2, '0');
    const day = String(weekStart.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function fmtSrv(n) {
    const v = Math.round(n * 10) / 10;
    return (Number.isInteger(v) ? v : v.toFixed(1)) + ' Pers.';
}

// ── Week label ────────────────────────────────────────

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
           d.getMonth()    === t.getMonth()    &&
           d.getDate()     === t.getDate();
}

// ── Day tabs ──────────────────────────────────────────

function renderDayTabs() {
    const container = document.getElementById('wp-day-tabs');
    container.innerHTML = DAYS.map((name, i) => {
        const d = new Date(weekStart);
        d.setDate(d.getDate() + i);
        const hasFilled = SLOTS.some((_, s) => (plan[`${i}_${s}`] || []).length > 0);
        const today = isToday(i);
        return `<div class="wp-day-tab${i === activeDay ? ' active' : ''}${hasFilled ? ' has-entries' : ''}${today ? ' today' : ''}" data-day="${i}">
            <div class="day-name">${today ? '•' + name : name}</div>
            <div class="day-date">${formatDate(d)}</div>
            <div class="day-dot"></div>
        </div>`;
    }).join('');
}

// ── Slot rendering ────────────────────────────────────

function isSlotPast() {
    const d = new Date(weekStart);
    d.setDate(d.getDate() + activeDay);
    d.setHours(0, 0, 0, 0);
    const today = new Date(); today.setHours(0, 0, 0, 0);
    return d < today;
}

function renderSlots() {
    const container = document.getElementById('wp-slots');
    const past = isSlotPast();

    const filledSlots = SLOTS
        .map((label, s) => ({ label, s, entries: plan[`${activeDay}_${s}`] || [] }))
        .filter(({ entries }) => entries.length > 0);

    let html = '';

    filledSlots.forEach(({ label, s, entries }) => {
        let entriesHtml = '';
        entries.forEach(e => {
            const bought = e.is_bought;
            const inList = !bought && e.in_shopping_list;
            const icon   = bought ? '<span class="wp-slot-icon">✓</span>'
                         : inList ? '<span class="wp-slot-icon">🛒</span>' : '';
            const cls    = bought ? 'bought' : inList ? 'in-list' : 'filled';

            if (past || bought) {
                entriesHtml += `<div class="wp-entry ${cls}">
                    <span class="wp-entry-name">${icon}${escHtml(e.name)}</span>
                </div>`;
            } else {
                entriesHtml += `<div class="wp-entry ${cls}">
                    <div class="wp-entry-top">
                        <span class="wp-entry-name">${icon}${escHtml(e.name)}</span>
                        <button class="wp-slot-clear" data-entry-id="${e.id}" title="Entfernen">✕</button>
                    </div>
                    <div class="wp-entry-servings">
                        <button class="wp-srv-btn" data-entry-id="${e.id}" data-delta="-0.5">−</button>
                        <span class="wp-srv-count" data-srv-entry="${e.id}">${fmtSrv(e.servings)}</span>
                        <button class="wp-srv-btn" data-entry-id="${e.id}" data-delta="0.5">+</button>
                    </div>
                </div>`;
            }
        });

        const addMore = !past
            ? `<div class="wp-slot-add" data-day="${activeDay}" data-slot="${s}">＋ Rezept</div>` : '';

        html += `<div class="wp-slot${past ? ' wp-slot-past' : ''}">
            <span class="wp-slot-label">${label}</span>
            <div class="wp-slot-entries">
                ${entriesHtml}
                ${addMore}
            </div>
        </div>`;
    });

    if (!past) {
        html += `<div class="wp-add-slot-btn" onclick="openSlotPicker(${activeDay})">＋ Mahlzeit hinzufügen</div>`;
    } else if (filledSlots.length === 0) {
        html += `<div class="wp-day-empty-past">Nichts geplant</div>`;
    }

    container.innerHTML = html;
}

function setDay(i) { activeDay = i; renderDayTabs(); renderSlots(); }

function render() { renderWeekLabel(); renderDayTabs(); renderSlots(); }

// ── Event delegation ──────────────────────────────────

document.getElementById('wp-day-tabs').addEventListener('click', e => {
    const tab = e.target.closest('.wp-day-tab');
    if (tab) setDay(parseInt(tab.dataset.day));
});

document.getElementById('wp-slots').addEventListener('click', e => {
    // Open picker
    const add = e.target.closest('.wp-slot-add');
    if (add) { openPicker(parseInt(add.dataset.day), parseInt(add.dataset.slot)); return; }

    // Servings
    const srv = e.target.closest('.wp-srv-btn');
    if (srv && srv.dataset.entryId) {
        changeServings(parseInt(srv.dataset.entryId), parseFloat(srv.dataset.delta));
        return;
    }

    // Clear entry
    const clear = e.target.closest('.wp-slot-clear');
    if (clear && clear.dataset.entryId) clearEntry(parseInt(clear.dataset.entryId));
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
                    const key = `${s.day_index}_${s.slot_index}`;
                    if (!plan[key]) plan[key] = [];
                    plan[key].push({
                        id: s.id,
                        recipe_id: s.recipe_id,
                        name: s.recipe_name,
                        servings: s.servings,
                        is_bought: s.is_bought,
                        in_shopping_list: s.in_shopping_list
                    });
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
    const msPerWeek  = 7 * 24 * 3600 * 1000;
    const weeksAhead = (weekStart - TODAY_MONDAY) / msPerWeek;
    document.getElementById('wp-prev').disabled = weeksAhead <= -4;
    document.getElementById('wp-next').disabled = weeksAhead >= 2;
    document.getElementById('wp-today-bar').style.display = weeksAhead !== 0 ? 'flex' : 'none';
}

async function changeWeek(delta) {
    weekStart.setDate(weekStart.getDate() + delta * 7);
    weekStart = getMonday(weekStart);
    const todayDayIndex = (() => { const d = new Date().getDay(); return d === 0 ? 6 : d - 1; })();
    activeDay = weekStart.getTime() === TODAY_MONDAY.getTime() ? todayDayIndex : 0;
    await loadWeek();
    render();
    updateNavButtons();
    if (overviewMode) renderOverview();
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
    if (overviewMode) renderOverview();
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

// ── Slot-type picker ──────────────────────────────────

let slotPickerDay = null;

function openSlotPicker(day) {
    slotPickerDay = day;
    const list = document.getElementById('wp-slot-picker-list');
    list.innerHTML = SLOTS.map((label, s) => {
        const count = (plan[`${day}_${s}`] || []).length;
        const badge = count > 0
            ? `<span class="wp-slot-option-count">${count} Rezept${count > 1 ? 'e' : ''}</span>` : '';
        return `<div class="wp-slot-option" onclick="selectSlotType(${s})">${escHtml(label)}${badge}</div>`;
    }).join('');
    document.getElementById('wp-slot-picker-backdrop').style.display = 'block';
    document.getElementById('wp-slot-picker').style.display = 'block';
}

function closeSlotPicker() {
    document.getElementById('wp-slot-picker-backdrop').style.display = 'none';
    document.getElementById('wp-slot-picker').style.display = 'none';
    slotPickerDay = null;
}

function selectSlotType(slotIndex) {
    const day = slotPickerDay;
    closeSlotPicker();
    openPicker(day, slotIndex);
}

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

document.getElementById('wp-picker-list').addEventListener('click', e => {
    const item = e.target.closest('.wp-picker-item');
    if (item) selectRecipe(parseInt(item.dataset.id), item.dataset.name);
});

async function selectRecipe(id, name) {
    if (!pickerTarget) return;
    const { day, slot } = pickerTarget;
    closePicker();

    try {
        const r = await fetch(`/api/wochenplan/${weekStartStr()}/${day}/${slot}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipe_id: id, servings: familySize })
        });
        if (!r.ok) throw new Error();
        const data = await r.json();
        const key = `${day}_${slot}`;
        if (!plan[key]) plan[key] = [];
        // Avoid duplicate in local state (same recipe added twice to same slot)
        if (!plan[key].find(e => e.id === data.entry_id)) {
            plan[key].push({ id: data.entry_id, recipe_id: id, name, servings: familySize, is_bought: false, in_shopping_list: false });
        }
        renderDayTabs();
        renderSlots();
    } catch(e) {
        showToast('Fehler beim Speichern');
    }
}

// ── Entry management ──────────────────────────────────

function findEntry(entryId) {
    for (const key of Object.keys(plan)) {
        const idx = plan[key].findIndex(e => e.id === entryId);
        if (idx !== -1) return { key, idx, entry: plan[key][idx] };
    }
    return null;
}

async function clearEntry(entryId) {
    try {
        await fetch(`/api/wochenplan/entry/${entryId}`, { method: 'DELETE' });
        for (const key of Object.keys(plan)) {
            plan[key] = plan[key].filter(e => e.id !== entryId);
            if (plan[key].length === 0) delete plan[key];
        }
        renderDayTabs();
        renderSlots();
    } catch(e) {
        showToast('Fehler');
    }
}

async function changeServings(entryId, delta) {
    const found = findEntry(entryId);
    if (!found) return;
    const { entry } = found;
    const newServings = Math.max(0.5, Math.round(((entry.servings || familySize) + delta) * 10) / 10);
    entry.servings = newServings;

    // Update count in DOM without full re-render
    const countEl = document.querySelector(`.wp-srv-count[data-srv-entry="${entryId}"]`);
    if (countEl) countEl.textContent = fmtSrv(newServings);

    try {
        await fetch(`/api/wochenplan/entry/${entryId}/servings`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ servings: newServings })
        });

        // Keep shopping list in sync: sum all plan entries for this recipe
        if (entry.in_shopping_list) {
            const total = Object.values(plan).flat()
                .filter(e => e.recipe_id === entry.recipe_id)
                .reduce((sum, e) => sum + e.servings, 0);
            await fetch(`/api/shopping-list/item/${entry.recipe_id}/servings`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ servings: Math.max(0.5, total) })
            });
        }
    } catch(e) {}
}

// ── Shopping list button ──────────────────────────────

document.getElementById('wp-to-list-btn').addEventListener('click', async () => {
    if (!Object.values(plan).some(arr => arr.length > 0)) {
        showToast('Keine Rezepte geplant');
        return;
    }
    try {
        const r = await fetch(`/api/wochenplan/${weekStartStr()}/to-shopping-list`, { method: 'POST' });
        const data = await r.json();
        if (data.success) {
            if (data.added > 0 || data.updated > 0) {
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

document.getElementById('wp-clear-btn').addEventListener('click', () => {
    document.getElementById('wp-clear-backdrop').style.display = 'block';
    document.getElementById('wp-clear-sheet').style.display = 'block';
});

function closeClearConfirm() {
    document.getElementById('wp-clear-backdrop').style.display = 'none';
    document.getElementById('wp-clear-sheet').style.display = 'none';
}

async function confirmClearWeek() {
    closeClearConfirm();
    try {
        await fetch(`/api/wochenplan/${weekStartStr()}/clear`, { method: 'DELETE' });
        plan = {};
        renderDayTabs();
        renderSlots();
        if (overviewMode) renderOverview();
    } catch(e) {
        showToast('Fehler');
    }
}

function showToast(msg) {
    const t = document.getElementById('wp-toast');
    t.textContent = msg;
    t.style.display = 'block';
    setTimeout(() => t.style.display = 'none', 2500);
}

// ── Week overview ─────────────────────────────────────

let overviewMode = false;

function toggleOverview() {
    overviewMode = !overviewMode;
    const label = document.getElementById('wp-week-label');
    label.classList.toggle('active', overviewMode);
    document.getElementById('wp-day-tabs').style.display  = overviewMode ? 'none' : '';
    document.getElementById('wp-slots').style.display     = overviewMode ? 'none' : '';
    document.getElementById('wp-overview').style.display  = overviewMode ? 'block' : 'none';
    if (overviewMode) renderOverview();
}

function renderOverview() {
    const container = document.getElementById('wp-overview');
    const today = new Date(); today.setHours(0, 0, 0, 0);

    container.innerHTML = DAYS.map((name, i) => {
        const d = new Date(weekStart);
        d.setDate(d.getDate() + i);
        const isPast  = d < today;
        const isTod   = d.getTime() === today.getTime();

        // Flatten all entries for this day across all slots
        const entries = SLOTS.flatMap((slotName, s) =>
            (plan[`${i}_${s}`] || []).map(e => ({ slotName, ...e }))
        );

        let html = `<div class="wp-overview-day${isPast ? ' past' : ''}${isTod ? ' today' : ''}" data-day="${i}">
            <div class="wp-overview-day-header">
                <span class="wp-overview-day-name">${isTod ? '• ' : ''}${name}</span>
                <span class="wp-overview-day-date">${d.getDate()}.${d.getMonth()+1}.</span>
            </div>
            <div class="wp-overview-entries">`;

        if (entries.length === 0) {
            html += `<span class="wp-overview-empty">Nichts geplant</span>`;
        } else {
            entries.forEach(e => {
                const icon = e.is_bought ? '✓ ' : e.in_shopping_list ? '🛒 ' : '';
                html += `<div class="wp-overview-entry${e.is_bought ? ' bought' : e.in_shopping_list ? ' in-list' : ''}">
                    <span class="wp-overview-slot">${e.slotName}</span>
                    <span class="wp-overview-recipe">${icon}${escHtml(e.name)}</span>
                </div>`;
            });
        }
        html += `</div></div>`;
        return html;
    }).join('');

    container.querySelectorAll('.wp-overview-day:not(.past)').forEach(el => {
        el.addEventListener('click', () => { toggleOverview(); setDay(parseInt(el.dataset.day)); });
    });
}

// ── Init ──────────────────────────────────────────────

window.onload = async () => {
    const [, , settingsRes] = await Promise.all([
        loadWeek(),
        loadRecipes(),
        fetch('/api/settings').catch(() => null)
    ]);
    if (settingsRes && settingsRes.ok) {
        try { familySize = (await settingsRes.json()).family_size || 1.0; } catch {}
    }
    render();
    updateNavButtons();
};
