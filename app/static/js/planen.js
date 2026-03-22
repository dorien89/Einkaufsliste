let allRecipes = [];
let allCategories = [];
let shoppingList = [];
let activeCategory = null;
let searchQuery = '';

// ── Init ─────────────────────────────────────────────
window.onload = async () => {
    await Promise.all([loadDraft(), loadData()]);
    document.getElementById('plan-search').addEventListener('input', e => {
        searchQuery = e.target.value.toLowerCase();
        render();
    });
};

async function loadData() {
    const [recipesRes, catsRes] = await Promise.all([
        fetch('/api/recipes/all'),
        fetch('/api/categories')
    ]);
    allRecipes = await recipesRes.json();
    allCategories = await catsRes.json();
    renderCategoryFilter();
    render();
}

async function loadDraft() {
    const res = await fetch('/api/shopping-list/draft');
    const data = await res.json();
    if (data.success) shoppingList = data.items;
}

// ── Category filter ───────────────────────────────────
function renderCategoryFilter() {
    const bar = document.getElementById('plan-cat-bar');
    bar.innerHTML = '';
    appendCatBtn(bar, 'Alle', null);
    allCategories.forEach(cat => appendCatBtn(bar, cat.name, cat.name));
}

function appendCatBtn(bar, label, value) {
    const btn = document.createElement('button');
    btn.className = 'plan-cat-btn' + (activeCategory === value ? ' active' : '');
    btn.textContent = label;
    btn.onclick = () => { activeCategory = value; renderCategoryFilter(); render(); };
    bar.appendChild(btn);
}

// ── Render list ───────────────────────────────────────
function getFiltered() {
    return allRecipes.filter(r => {
        const matchesCat = !activeCategory || r.category === activeCategory;
        const matchesSearch = !searchQuery || r.name.toLowerCase().includes(searchQuery);
        return matchesCat && matchesSearch;
    });
}

function render() {
    const list = document.getElementById('plan-list');
    const recipes = getFiltered();
    list.innerHTML = '';

    if (recipes.length === 0) {
        list.innerHTML = '<div class="plan-empty">Keine Rezepte gefunden</div>';
        updateFooter();
        return;
    }

    // Group by category, sort groups and items within alphabetically
    const groups = {};
    recipes.forEach(r => {
        const cat = r.category || 'Sonstige';
        if (!groups[cat]) groups[cat] = [];
        groups[cat].push(r);
    });

    Object.keys(groups).sort().forEach(cat => {
        const header = document.createElement('div');
        header.className = 'plan-group-header';
        header.textContent = cat;
        list.appendChild(header);

        groups[cat]
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach(recipe => list.appendChild(makeItem(recipe)));
    });

    updateFooter();
}

function makeItem(recipe) {
    const listItem = shoppingList.find(i => i.id === recipe.id);
    const inList = listItem && listItem.servings > 0;
    const servings = inList ? listItem.servings : 0;

    const div = document.createElement('div');
    div.className = 'plan-item' + (inList ? ' in-list' : '');
    div.id = 'plan-item-' + recipe.id;

    const safeName = recipe.name.replace(/'/g, "\\'");

    div.innerHTML = `
        <div class="plan-item-info" onclick="handleTap(${recipe.id}, '${safeName}')">
            <span class="plan-item-name">${recipe.name}</span>
            <span class="plan-item-cat">${recipe.category || ''}</span>
        </div>
        <div class="plan-item-controls">
            ${inList ? `
                <button class="plan-btn plan-minus" onclick="changeServings(${recipe.id}, -1)">−</button>
                <span class="plan-count">${servings}</span>
                <button class="plan-btn plan-plus" onclick="changeServings(${recipe.id}, 1)">+</button>
            ` : `
                <button class="plan-btn plan-add" onclick="handleTap(${recipe.id}, '${safeName}')">+</button>
            `}
        </div>
    `;
    return div;
}

function refreshItem(recipeId) {
    const recipe = allRecipes.find(r => r.id === recipeId);
    if (!recipe) return;
    const el = document.getElementById('plan-item-' + recipeId);
    if (el) el.replaceWith(makeItem(recipe));
    updateFooter();
}

// ── Shopping list actions ─────────────────────────────
async function handleTap(recipeId, recipeName) {
    const existing = shoppingList.find(i => i.id === recipeId);
    if (existing) {
        await changeServings(recipeId, 1);
    } else {
        shoppingList.push({ id: recipeId, name: recipeName, servings: 1 });
        refreshItem(recipeId);
        await fetch('/api/shopping-list/item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: recipeId })
        });
    }
}

async function changeServings(recipeId, delta) {
    const item = shoppingList.find(i => i.id === recipeId);
    if (!item) return;

    if (item.servings + delta <= 0) {
        shoppingList = shoppingList.filter(i => i.id !== recipeId);
        refreshItem(recipeId);
        await fetch(`/api/shopping-list/item/${recipeId}`, { method: 'DELETE' });
    } else {
        item.servings += delta;
        refreshItem(recipeId);
        await fetch(`/api/shopping-list/item/${recipeId}/servings`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ servings: item.servings })
        });
    }
}

// ── Footer button ─────────────────────────────────────
function updateFooter() {
    const total = shoppingList.reduce((s, i) => s + i.servings, 0);
    const btn = document.getElementById('plan-footer-btn');
    if (total > 0) {
        const count = shoppingList.length;
        btn.textContent = `🛒  ${count} ${count === 1 ? 'Gericht' : 'Gerichte'} — Einkaufsliste ansehen`;
        btn.style.display = 'block';
    } else {
        btn.style.display = 'none';
    }
}
