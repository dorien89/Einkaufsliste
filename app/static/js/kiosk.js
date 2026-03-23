// ── Theme ─────────────────────────────────────────────
const THEMES = ['küche', 'garten', 'nacht'];

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.querySelectorAll('.theme-option').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === theme);
    });
}

function setTheme(theme) {
    applyTheme(theme);
    localStorage.setItem('kiosk-theme', theme);
    closeThemePicker();
}

function toggleThemePicker() {
    const panel = document.getElementById('theme-picker-panel');
    panel.classList.toggle('hidden');
}

function closeThemePicker() {
    document.getElementById('theme-picker-panel').classList.add('hidden');
}

// ── Init theme from localStorage ──────────────────────
applyTheme(localStorage.getItem('kiosk-theme') || 'küche');

const DAY_NAMES = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];
const SLOTS = ['Frühstück', 'Vormittag', 'Mittagessen', 'Nachmittag', 'Abendessen'];

let allRecipes = [];
let activeCategory = null;
// weekPlan key: "weekStartStr|dayIndex|slotIndex" -> recipe_id
let weekPlan = {};

// ── Helpers ───────────────────────────────────────────
function getMonday(d) {
    d = new Date(d);
    const day = d.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    d.setDate(d.getDate() + diff);
    d.setHours(0, 0, 0, 0);
    return d;
}

function formatYMD(d) {
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

function formatDMY(d) {
    return `${d.getDate()}.${d.getMonth()+1}.`;
}

// Generate the next 21 days starting from today
function getUpcomingDays() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const days = [];
    for (let i = 0; i < 20; i++) {
        const d = new Date(today);
        d.setDate(d.getDate() + i);
        const mon = getMonday(d);
        const dow = d.getDay(); // 0=Sun
        const dayIndex = dow === 0 ? 6 : dow - 1; // 0=Mon..6=Sun
        days.push({
            date: d,
            weekStartStr: formatYMD(mon),
            dayIndex,
            name: DAY_NAMES[dayIndex],
            display: formatDMY(d),
            isToday: i === 0
        });
    }
    return days;
}

// ── Load week plan (3 weeks) ──────────────────────────
async function loadWeekPlan() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const weeks = new Set();
    for (let i = 0; i < 20; i++) {
        const d = new Date(today);
        d.setDate(d.getDate() + i);
        weeks.add(formatYMD(getMonday(d)));
    }
    weekPlan = {};
    await Promise.all([...weeks].map(async ws => {
        try {
            const r = await fetch(`/api/wochenplan/${ws}`);
            const data = await r.json();
            if (data.slots) {
                data.slots.forEach(s => {
                    if (s.recipe_id) weekPlan[`${ws}|${s.day_index}|${s.slot_index}`] = {
                        id: s.recipe_id,
                        is_bought: s.is_bought,
                        in_shopping_list: s.in_shopping_list,
                        servings: s.servings
                    };
                });
            }
        } catch(e) {}
    }));
}

// Returns {planned: Set, bought: Set} considering only today-or-future slots
function relevantEntries() {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const planned = new Set();
    const bought = new Set();
    Object.entries(weekPlan).forEach(([key, v]) => {
        const parts = key.split('|');
        const d = new Date(parts[0]);
        d.setDate(d.getDate() + parseInt(parts[1]));
        d.setHours(0, 0, 0, 0);
        if (d >= today) {
            if (v.is_bought) bought.add(v.id);
            else planned.add(v.id);
        }
    });
    bought.forEach(id => { if (planned.has(id)) bought.delete(id); });
    return { planned, bought };
}

// ── Grid ──────────────────────────────────────────────
function renderGrid() {
    const container = document.querySelector('.grid-container');
    container.innerHTML = '';
    const filtered = activeCategory
        ? allRecipes.filter(r => r.category === activeCategory)
        : allRecipes;
    const shuffled = [...filtered].sort(() => Math.random() - 0.5).slice(0, 9);
    const { planned, bought } = relevantEntries();

    shuffled.forEach(recipe => {
        const div = document.createElement('div');
        let cls = 'grid-item';
        if (planned.has(recipe.id)) cls += ' planned';
        else if (bought.has(recipe.id)) cls += ' bought';
        div.className = cls;
        div.textContent = recipe.name;
        div.dataset.recipeId = recipe.id;
        div.dataset.recipeName = recipe.name;
        div.addEventListener('click', () => openSlotPicker(recipe.id, recipe.name));
        container.appendChild(div);
    });
}

// ── Category filter ───────────────────────────────────
function setCategory(cat) {
    activeCategory = cat;
    renderFilterBar();
    renderGrid();
}

function renderFilterBar() {
    const bar = document.getElementById('category-filter-bar');
    bar.className = 'kiosk-filter-bar' + (activeCategory !== null ? ' has-filter' : '');
    bar.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.className = 'kiosk-cat-btn' + (activeCategory === null ? ' active' : '');
    allBtn.textContent = 'Alle';
    allBtn.onclick = () => setCategory(null);
    bar.appendChild(allBtn);

    const categories = [...new Set(allRecipes.map(r => r.category).filter(Boolean))].sort();
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'kiosk-cat-btn' + (activeCategory === cat ? ' active' : '');
        btn.textContent = cat;
        btn.onclick = () => setCategory(cat);
        bar.appendChild(btn);
    });
}

// ── Slot picker ───────────────────────────────────────
let pickerRecipeId = null;
let pickerRecipeName = null;
let pickerDayInfo = null;
let pickerSlotIndex = null;

function openSlotPicker(id, name) {
    pickerRecipeId = id;
    pickerRecipeName = name;
    pickerDayInfo = null;

    document.getElementById('slot-picker-title').textContent = name;
    showDayStep();
    document.getElementById('slot-backdrop').classList.remove('hidden');
    document.getElementById('slot-picker').classList.remove('hidden');
}

function closeSlotPicker() {
    closeThemePicker();
    document.getElementById('slot-backdrop').classList.add('hidden');
    document.getElementById('slot-picker').classList.add('hidden');
    pickerRecipeId = null;
    pickerRecipeName = null;
    pickerDayInfo = null;
    pickerSlotIndex = null;
}

function showDayStep() {
    document.getElementById('slot-step-day').style.display = 'block';
    document.getElementById('slot-step-meal').style.display = 'none';
    document.getElementById('slot-step-servings').style.display = 'none';
    document.getElementById('slot-picker-footer').style.display = 'none';

    const days = getUpcomingDays();
    const grid = document.getElementById('slot-day-grid');
    grid.innerHTML = days.map((day, i) => {
        const hasAny = SLOTS.some((_, s) => weekPlan[`${day.weekStartStr}|${day.dayIndex}|${s}`] !== undefined);
        return `<button class="slot-day-btn${hasAny ? ' has-entries' : ''}${day.isToday ? ' today' : ''}" data-idx="${i}">
            <span class="slot-day-name">${day.isToday ? 'Heute' : day.name}</span>
            <span class="slot-day-date">${day.display}</span>
        </button>`;
    }).join('');

    grid.querySelectorAll('.slot-day-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            selectDay(days[parseInt(btn.dataset.idx)]);
        });
    });
}

function selectDay(dayInfo) {
    pickerDayInfo = dayInfo;
    document.getElementById('slot-step-day').style.display = 'none';
    document.getElementById('slot-step-meal').style.display = 'block';
    document.getElementById('slot-picker-footer').style.display = 'block';
    document.getElementById('slot-meal-label').textContent =
        `${dayInfo.isToday ? 'Heute' : dayInfo.name}, ${dayInfo.display} — Welche Mahlzeit?`;

    const list = document.getElementById('slot-meal-list');
    list.innerHTML = SLOTS.map((label, s) => {
        const key = `${dayInfo.weekStartStr}|${dayInfo.dayIndex}|${s}`;
        const entry = weekPlan[key];
        const takenId = entry?.id;
        const isBought = entry?.is_bought;
        const inList = entry?.in_shopping_list && !isBought;
        const isThisRecipe = takenId === pickerRecipeId;
        const takenRecipe = takenId ? allRecipes.find(r => r.id === takenId) : null;
        let btnClass = '';
        if (isThisRecipe && isBought)   btnClass = ' bought selected';
        else if (isThisRecipe && inList) btnClass = ' in-list selected';
        else if (isThisRecipe)           btnClass = ' selected';
        else if (isBought)               btnClass = ' bought';
        else if (inList)                 btnClass = ' in-list';
        else if (takenId)                btnClass = ' taken';
        const servingsLabel = entry?.servings ? ` · ${entry.servings} Pers.` : '';
        return `<button class="slot-meal-btn${btnClass}" data-slot="${s}">
            <span class="slot-meal-name">${label}</span>
            ${isThisRecipe
                ? `<span class="slot-meal-taken">${isBought ? '✓ gekauft' : inList ? '🛒 in Liste' : '✓ gewählt'}${servingsLabel} — tippen zum ${isBought || inList ? 'Ersetzen' : 'Entfernen'}</span>`
                : takenRecipe
                    ? `<span class="slot-meal-taken">${isBought ? '✓ ' : inList ? '🛒 ' : ''}${takenRecipe.name}${servingsLabel}</span>`
                    : ''}
        </button>`;
    }).join('');

    list.querySelectorAll('.slot-meal-btn').forEach(btn => {
        btn.addEventListener('click', () => assignOrRemoveSlot(parseInt(btn.dataset.slot)));
    });
}

function slotBackToDay() {
    showDayStep();
}

function slotBackToMeal() {
    document.getElementById('slot-step-servings').style.display = 'none';
    document.getElementById('slot-step-meal').style.display = 'block';
    document.getElementById('slot-picker-footer').querySelector('.slot-back-btn').onclick = slotBackToDay;
}

function assignOrRemoveSlot(slotIndex) {
    const { weekStartStr, dayIndex } = pickerDayInfo;
    const key = `${weekStartStr}|${dayIndex}|${slotIndex}`;
    const oldEntry = weekPlan[key];
    const oldId = oldEntry?.id;
    const isToggleOff = oldId === pickerRecipeId && !oldEntry?.is_bought && !oldEntry?.in_shopping_list;

    pickerSlotIndex = slotIndex;
    const defaultServings = oldEntry?.servings || 1;
    showServingsStep(defaultServings, isToggleOff);
}

function showServingsStep(defaultServings, showDelete = false) {
    document.getElementById('slot-step-meal').style.display = 'none';
    document.getElementById('slot-step-servings').style.display = 'block';
    const backBtn = document.getElementById('slot-picker-footer').querySelector('.slot-back-btn');
    backBtn.onclick = slotBackToMeal;

    const grid = document.getElementById('slot-servings-grid');
    const numbers = [1, 2, 3, 4, 5, 6, 7, 8].map(n =>
        `<button class="slot-servings-btn${n === defaultServings ? ' selected' : ''}" onclick="confirmServings(${n})">${n}</button>`
    ).join('');
    const deleteBtn = showDelete
        ? `<button class="slot-servings-delete" onclick="deleteCurrentSlot()">🗑 Entfernen</button>`
        : '';
    grid.innerHTML = numbers + deleteBtn;
}

async function deleteCurrentSlot() {
    const { weekStartStr, dayIndex } = pickerDayInfo;
    const slotIndex = pickerSlotIndex;
    const key = `${weekStartStr}|${dayIndex}|${slotIndex}`;
    const id = pickerRecipeId;
    const name = pickerRecipeName;
    closeSlotPicker();
    try {
        await fetch(`/api/wochenplan/${weekStartStr}/${dayIndex}/${slotIndex}`, { method: 'DELETE' });
        delete weekPlan[key];
        showFeedback(`${name} entfernt`);
        updateTile(id);
    } catch(e) {}
}

async function confirmServings(servings) {
    const { weekStartStr, dayIndex } = pickerDayInfo;
    const slotIndex = pickerSlotIndex;
    const key = `${weekStartStr}|${dayIndex}|${slotIndex}`;
    const oldId = weekPlan[key]?.id;
    const id = pickerRecipeId;
    const name = pickerRecipeName;
    closeSlotPicker();

    try {
        await fetch(`/api/wochenplan/${weekStartStr}/${dayIndex}/${slotIndex}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipe_id: id, servings })
        });
        weekPlan[key] = { id, is_bought: false, servings };
        showFeedback(`✓ ${name} · ${servings} Pers.`);
        updateTile(id);
        if (oldId !== undefined && oldId !== id) updateTile(oldId);
    } catch(e) {}
}

function updateTile(recipeId) {
    const tile = document.querySelector(`.grid-item[data-recipe-id="${recipeId}"]`);
    if (!tile) return;
    const { planned, bought } = relevantEntries();
    tile.classList.toggle('planned', planned.has(recipeId));
    tile.classList.toggle('bought', bought.has(recipeId));
}

function showFeedback(msg) {
    let toast = document.getElementById('kiosk-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'kiosk-toast';
        toast.style.cssText = 'position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:12px 24px;border-radius:24px;font-size:1rem;font-weight:600;z-index:2000;pointer-events:none;white-space:nowrap;';
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 2000);
}

// ── Load ──────────────────────────────────────────────
async function loadRecipes() {
    try {
        const r = await fetch('/api/recipes/all');
        allRecipes = await r.json();
        renderFilterBar();
        renderGrid();
    } catch(e) {
        console.error('Fehler:', e);
    }
}

async function refreshWeekPlan() {
    await loadWeekPlan();
    const { planned, bought } = relevantEntries();
    document.querySelectorAll('.grid-item').forEach(tile => {
        const id = parseInt(tile.dataset.recipeId);
        tile.classList.toggle('planned', planned.has(id));
        tile.classList.toggle('bought', bought.has(id));
    });
}

window.onload = async () => {
    await Promise.all([loadWeekPlan(), loadRecipes()]);
    setInterval(refreshWeekPlan, 30000);
    document.querySelector('.kiosk-wrapper').addEventListener('click', closeThemePicker);
};
