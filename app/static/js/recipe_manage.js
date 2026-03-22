let allRecipes = [];
let allCategories = [];
let activeRecipeId = null;
let activeCategory = null;
let filterExpanded = window.innerWidth > 767; // collapsed by default on mobile

// ── Scroll progress ───────────────────────────────────
function updateScrollProgress() {
    const el = document.getElementById('rm-list-items');
    const bar = document.getElementById('rm-scroll-progress');
    if (!el || !bar) return;
    const { scrollTop, scrollHeight, clientHeight } = el;
    const scrollable = scrollHeight - clientHeight;
    bar.style.width = (scrollable > 0 ? (scrollTop / scrollable) * 100 : 100) + '%';
}

// ── Init ─────────────────────────────────────────────
async function init() {
    await loadCategories();
    await loadRecipeList();
    document.getElementById('rm-list-items').addEventListener('scroll', updateScrollProgress);
}

// ── Categories ───────────────────────────────────────
async function loadCategories() {
    const res = await fetch('/api/categories');
    allCategories = await res.json();
    renderCategoryFilter();
}

function renderCategoryFilter() {
    const bar = document.getElementById('rm-category-filter');
    bar.innerHTML = '';

    // Toggle button (mobile only — hidden on desktop via CSS)
    const toggle = document.createElement('button');
    toggle.className = 'rm-filter-toggle';
    const label = activeCategory ? activeCategory : 'Alle';
    toggle.textContent = `Kategorie: ${label} ${filterExpanded ? '▴' : '▾'}`;
    toggle.onclick = () => { filterExpanded = !filterExpanded; renderCategoryFilter(); };
    bar.appendChild(toggle);

    // Pills container
    const pills = document.createElement('div');
    pills.className = 'rm-filter-pills' + (filterExpanded ? '' : ' collapsed');
    bar.appendChild(pills);

    const all = document.createElement('button');
    all.className = 'rm-cat-btn' + (activeCategory === null ? ' active' : '');
    all.textContent = 'Alle';
    all.onclick = () => { activeCategory = null; filterExpanded = false; renderCategoryFilter(); renderList(getFilteredRecipes()); };
    pills.appendChild(all);

    allCategories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'rm-cat-btn' + (activeCategory === cat.name ? ' active' : '');
        btn.textContent = cat.name;
        btn.onclick = () => { activeCategory = cat.name; filterExpanded = false; renderCategoryFilter(); renderList(getFilteredRecipes()); };
        pills.appendChild(btn);
    });
}

function getFilteredRecipes() {
    const q = document.getElementById('rm-search').value.toLowerCase();
    return allRecipes.filter(r => {
        const matchesSearch = r.name.toLowerCase().includes(q) || (r.category || '').toLowerCase().includes(q);
        const matchesCategory = activeCategory === null || r.category === activeCategory;
        return matchesSearch && matchesCategory;
    });
}

// ── Recipe list ──────────────────────────────────────
async function loadRecipeList() {
    const response = await fetch('/api/recipes/all');
    allRecipes = await response.json();
    renderList(getFilteredRecipes());
}

function renderList(recipes) {
    const ul = document.getElementById('rm-list-items');
    ul.innerHTML = '';

    const countEl = document.getElementById('rm-list-count');
    if (countEl) countEl.textContent = recipes.length === allRecipes.length
        ? `${recipes.length} Rezepte`
        : `${recipes.length} von ${allRecipes.length}`;

    if (recipes.length === 0) {
        ul.innerHTML = '<li style="padding:16px;color:#aaa">Keine Rezepte gefunden</li>';
        updateScrollProgress();
        return;
    }
    recipes.forEach(recipe => {
        const li = document.createElement('li');
        li.className = 'rm-list-item' + (recipe.id === activeRecipeId ? ' active' : '');
        li.innerHTML = `<span class="item-title">${recipe.name}</span><span class="item-category">${recipe.category || ''}</span>`;
        li.onclick = () => openRecipe(recipe.id);
        ul.appendChild(li);
    });
    updateScrollProgress();
}

function filterList() {
    renderList(getFilteredRecipes());
}

// ── Detail view ──────────────────────────────────────
async function openRecipe(recipeId) {
    activeRecipeId = recipeId;
    renderList(allRecipes.filter(r => {
        const q = document.getElementById('rm-search').value.toLowerCase();
        return r.name.toLowerCase().includes(q) || (r.category || '').toLowerCase().includes(q);
    }));

    const response = await fetch(`/api/recipe/${recipeId}`);
    const recipe = await response.json();

    const panel = document.getElementById('rm-detail-content');
    panel.innerHTML = `
        <button class="rm-back-btn" onclick="closeDetail()">← Zurück</button>
        <div class="rm-detail-header">
            <div>
                <div class="rm-detail-title">${recipe.name}</div>
                <span class="rm-detail-category">${recipe.category || '—'}</span>
            </div>
            <div class="rm-action-btns">
                <button class="rm-btn rm-btn-edit" onclick="openEditForm(${recipe.id})">Bearbeiten</button>
                <button class="rm-btn rm-btn-delete" onclick="deleteRecipe(${recipe.id})">Löschen</button>
            </div>
        </div>
        ${recipe.description ? `<p class="rm-detail-description">${recipe.description}</p>` : ''}
        <table class="rm-ingredient-table">
            <thead><tr><th>Zutat</th><th>Menge</th><th>Einheit</th></tr></thead>
            <tbody>
                ${recipe.ingredients.map(i => `
                    <tr>
                        <td>${i.name}</td>
                        <td>${i.amount}</td>
                        <td>${i.unit}</td>
                    </tr>`).join('')}
            </tbody>
        </table>
    `;
    document.getElementById('rm-container').classList.add('detail-open');
}

function closeDetail() {
    activeRecipeId = null;
    document.getElementById('rm-detail-content').innerHTML = '<div class="rm-detail-empty">Wähle ein Rezept oder füge ein neues hinzu.</div>';
    document.getElementById('rm-container').classList.remove('detail-open');
    renderList(allRecipes);
}

// ── Delete ───────────────────────────────────────────
async function deleteRecipe(recipeId) {
    if (!confirm('Rezept wirklich löschen?')) return;
    await fetch(`/api/recipe/${recipeId}`, { method: 'DELETE' });
    activeRecipeId = null;
    await loadRecipeList();
    document.getElementById('rm-detail-content').innerHTML = '<div class="rm-detail-empty">Wähle ein Rezept oder füge ein neues hinzu.</div>';
    document.getElementById('rm-container').classList.remove('detail-open');
}

// ── Add / Edit form ──────────────────────────────────
async function openAddForm() {
    activeRecipeId = null;
    renderList(allRecipes);
    renderForm(null);
    document.getElementById('rm-container').classList.add('detail-open');
}

async function openEditForm(recipeId) {
    const response = await fetch(`/api/recipe/${recipeId}`);
    const recipe = await response.json();
    renderForm(recipe);
}

function renderForm(recipe) {
    const isEdit = recipe !== null;
    const panel = document.getElementById('rm-detail-content');
    panel.innerHTML = `
        <button class="rm-back-btn" onclick="closeDetail()">← Zurück</button>
        <div class="rm-form-title">${isEdit ? 'Rezept bearbeiten' : 'Neues Rezept'}</div>
        <div class="rm-form-group">
            <label>Name</label>
            <input type="text" id="f-name" value="${isEdit ? recipe.name : ''}" placeholder="Rezeptname">
        </div>
        <div class="rm-form-group">
            <label>Kategorie</label>
            <select id="f-category">
                <option value="">-- Keine --</option>
                ${allCategories.map(c => `<option value="${c.name}" ${isEdit && recipe.category === c.name ? 'selected' : ''}>${c.name}</option>`).join('')}
            </select>
        </div>
        <div class="rm-form-group">
            <label>Beschreibung (optional)</label>
            <textarea id="f-description" placeholder="Kurze Beschreibung...">${isEdit ? recipe.description : ''}</textarea>
        </div>
        <div class="rm-form-group">
            <label>Zutaten</label>
            <div class="rm-ingredient-rows" id="ingredient-rows"></div>
            <button class="rm-add-ingredient-btn" onclick="addIngredientRow()">+ Zutat hinzufügen</button>
        </div>
        <div class="rm-action-btns">
            <button class="rm-btn rm-btn-save" onclick="saveRecipe(${isEdit ? recipe.id : 'null'})">Speichern</button>
            <button class="rm-btn rm-btn-cancel" onclick="${isEdit ? `openRecipe(${recipe.id})` : 'closeDetail()'}">Abbrechen</button>
        </div>
    `;

    if (isEdit) {
        recipe.ingredients.forEach(i => addIngredientRow(i));
    } else {
        addIngredientRow();
    }
}

// ── Ingredient row with typeahead ────────────────────
function addIngredientRow(data = null) {
    const container = document.getElementById('ingredient-rows');
    const rowId = Date.now() + Math.random();
    const div = document.createElement('div');
    div.className = 'rm-ingredient-row';
    div.dataset.rowId = rowId;
    div.dataset.ingredientId = data ? data.ingredient_id : '';
    div.innerHTML = `
        <div class="typeahead-wrapper ing-name">
            <input type="text" class="ing-name-input" placeholder="Zutat suchen..."
                value="${data ? data.name : ''}"
                oninput="onTypeahead(this, '${rowId}')"
                onblur="closeDropdown('${rowId}')"
                autocomplete="off">
            <div class="typeahead-dropdown" id="dropdown-${rowId}" style="display:none"></div>
        </div>
        <input type="number" class="ing-amount" placeholder="Menge" min="0" step="0.1"
            value="${data ? data.amount : ''}" style="padding:10px;font-size:1em;border:1px solid #ccc;border-radius:6px;">
        <input type="text" class="ing-unit" placeholder="Einheit"
            value="${data ? data.unit : ''}" style="padding:10px;font-size:1em;border:1px solid #ccc;border-radius:6px;width:90px;">
        <button class="ing-remove" onclick="this.closest('.rm-ingredient-row').remove()"
            style="background:#e53935;color:#fff;border:none;border-radius:6px;width:40px;height:40px;font-size:1.2em;cursor:pointer;">✕</button>
    `;
    container.appendChild(div);
}

let typeaheadTimer = null;

function onTypeahead(input, rowId) {
    const row = document.querySelector(`[data-row-id="${rowId}"]`);
    row.dataset.ingredientId = '';

    clearTimeout(typeaheadTimer);
    typeaheadTimer = setTimeout(async () => {
        const q = input.value.trim();
        const dropdown = document.getElementById(`dropdown-${rowId}`);
        if (!q) { dropdown.style.display = 'none'; return; }

        const res = await fetch(`/api/ingredients?q=${encodeURIComponent(q)}`);
        const items = await res.json();

        dropdown.innerHTML = '';
        items.slice(0, 8).forEach(item => {
            const div = document.createElement('div');
            div.className = 'typeahead-option';
            div.textContent = item.name + (item.default_unit ? ` (${item.default_unit})` : '');
            div.onmousedown = () => selectIngredient(rowId, item.id, item.name, item.default_unit);
            dropdown.appendChild(div);
        });

        const exactMatch = items.some(i => i.name.toLowerCase() === q.toLowerCase());
        if (!exactMatch) {
            const div = document.createElement('div');
            div.className = 'typeahead-option create-new';
            div.textContent = `+ Neu anlegen: "${q}"`;
            div.onmousedown = () => selectIngredient(rowId, null, q, null);
            dropdown.appendChild(div);
        }

        dropdown.style.display = items.length || !exactMatch ? 'block' : 'none';
    }, 200);
}

function selectIngredient(rowId, ingredientId, name, defaultUnit) {
    const row = document.querySelector(`[data-row-id="${rowId}"]`);
    row.dataset.ingredientId = ingredientId || '';
    row.querySelector('.ing-name-input').value = name;
    document.getElementById(`dropdown-${rowId}`).style.display = 'none';
    if (defaultUnit) {
        row.querySelector('.ing-unit').value = defaultUnit;
    }
    row.querySelector('.ing-amount').focus();
}

function closeDropdown(rowId) {
    setTimeout(() => {
        const dropdown = document.getElementById(`dropdown-${rowId}`);
        if (dropdown) dropdown.style.display = 'none';
    }, 150);
}

// ── Save recipe ──────────────────────────────────────
async function saveRecipe(recipeId) {
    const name = document.getElementById('f-name').value.trim();
    const category = document.getElementById('f-category').value.trim();
    const description = document.getElementById('f-description').value.trim();

    if (!name) { alert('Bitte einen Namen eingeben.'); return; }

    const rows = document.querySelectorAll('.rm-ingredient-row');
    const ingredients = [];
    for (const row of rows) {
        const ingName = row.querySelector('.ing-name-input').value.trim();
        const amount = parseFloat(row.querySelector('.ing-amount').value);
        const unit = row.querySelector('.ing-unit').value.trim();
        if (!ingName || isNaN(amount) || !unit) {
            alert('Bitte alle Zutatenfelder ausfüllen.'); return;
        }
        const ingredientId = row.dataset.ingredientId ? parseInt(row.dataset.ingredientId) : null;
        ingredients.push({ ingredient_id: ingredientId, name: ingName, amount, unit });
    }

    const url = recipeId ? `/api/recipe/${recipeId}` : '/api/recipe';
    const method = recipeId ? 'PUT' : 'POST';
    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, description, ingredients }),
    });

    const data = await res.json();
    if (!res.ok) { alert(`Fehler: ${data.error}`); return; }

    await loadRecipeList();
    openRecipe(data.id);
}

window.onload = init;
