let allRecipes = [];
let allCategories = [];
let activeRecipeId = null;
let activeCategory = null;
let filterExpanded = window.innerWidth > 767; // collapsed by default on mobile
let selectMode = false;
let selectedIds = new Set();
let familySize = 1.0;

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
    // Load settings and categories/recipes in parallel
    const [settingsRes] = await Promise.all([
        fetch('/api/settings'),
        loadCategories(),
        loadRecipeList(),
    ]);
    try {
        const s = await settingsRes.json();
        familySize = s.family_size || 1.0;
    } catch {}
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
    all.onclick = () => { activeCategory = null; if (window.innerWidth <= 767) filterExpanded = false; renderCategoryFilter(); renderList(getFilteredRecipes()); };
    pills.appendChild(all);

    const usedNames = new Set(allRecipes.map(r => r.category).filter(Boolean));
    allCategories.filter(cat => usedNames.has(cat.name)).forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'rm-cat-btn' + (activeCategory === cat.name ? ' active' : '');
        btn.textContent = cat.name;
        btn.onclick = () => { activeCategory = cat.name; if (window.innerWidth <= 767) filterExpanded = false; renderCategoryFilter(); renderList(getFilteredRecipes()); };
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
    renderCategoryFilter();
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
        li.className = 'rm-list-item' + (recipe.id === activeRecipeId ? ' active' : '') + (selectMode && selectedIds.has(recipe.id) ? ' selected' : '');
        li.dataset.id = recipe.id;

        if (selectMode) {
            li.innerHTML = `
                <input type="checkbox" class="rm-select-cb" ${selectedIds.has(recipe.id) ? 'checked' : ''}>
                <span class="item-title">${recipe.name}</span>
                <span class="item-category">${recipe.category || ''}</span>`;
            li.onclick = () => toggleSelect(recipe.id);
        } else {
            li.innerHTML = `
                <span class="item-title">${recipe.name}</span>
                <span class="item-category">${recipe.category || ''}</span>
                <button class="rm-swipe-delete-btn" title="Löschen" onclick="quickDelete(event, ${recipe.id})">🗑️</button>`;
            li.onclick = () => openRecipe(recipe.id);
            addSwipeToDelete(li, recipe.id);
        }
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
        </div>
        ${recipe.description ? `<p class="rm-detail-description">${recipe.description}</p>` : ''}
        <div class="rm-portion-label">${portionLabel(familySize)}</div>
        <table class="rm-ingredient-table">
            <thead><tr><th>Zutat</th><th>Menge <span class="rm-portion-hint">(${portionLabel(familySize)})</span></th><th>Einheit</th></tr></thead>
            <tbody>
                ${renderIngredientRows(recipe.ingredients.filter(i => !i.is_staple))}
                ${recipe.ingredients.some(i => i.is_staple) ? `
                <tr class="rm-ing-section-row"><td colspan="3">Vorrat</td></tr>
                ${renderIngredientRows(recipe.ingredients.filter(i => i.is_staple), 'rm-ing-vorrat')}` : ''}
            </tbody>
        </table>
    `;
    const footer = document.getElementById('rm-detail-footer');
    footer.innerHTML = `
        <button class="rm-btn rm-btn-save" style="flex:1" data-rid="${recipe.id}" data-rname="${escHtml(recipe.name)}" onclick="openCartSheet(parseInt(this.dataset.rid), this.dataset.rname)">🛒</button>
        <button class="rm-btn rm-btn-edit" style="flex:1" onclick="openEditForm(${recipe.id})">Bearbeiten</button>
        <button class="rm-btn rm-btn-delete" style="flex:1" onclick="deleteRecipe(${recipe.id})">Löschen</button>
    `;
    footer.style.display = 'flex';
    document.getElementById('rm-container').classList.add('detail-open');
}

function closeDetail() {
    activeRecipeId = null;
    document.getElementById('rm-detail-content').innerHTML = '<div class="rm-detail-empty">Wähle ein Rezept oder füge ein neues hinzu.</div>';
    const footer = document.getElementById('rm-detail-footer');
    if (footer) { footer.style.display = 'none'; footer.innerHTML = ''; }
    document.getElementById('rm-container').classList.remove('detail-open');
    renderList(allRecipes);
}

// ── Delete ───────────────────────────────────────────
async function deleteRecipe(recipeId) {
    const ok = await showConfirmModal(
        'Rezept löschen?',
        'Das Rezept wird in den Papierkorb verschoben und kann dort wiederhergestellt werden.',
        'Löschen', 'rm-btn-delete'
    );
    if (!ok) return;
    await fetch(`/api/recipe/${recipeId}`, { method: 'DELETE' });
    activeRecipeId = null;
    await loadRecipeList();
    closeDetail();
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
            <label>Zutaten <span style="font-size:0.75rem;font-weight:normal;color:var(--app-muted,#888);">(Mengen für 1 Person)</span></label>
            <div class="rm-ingredient-rows" id="ingredient-rows"></div>
            <button class="rm-add-ingredient-btn" onclick="addIngredientRow()">+ Zutat hinzufügen</button>
        </div>
    `;
    const footer = document.getElementById('rm-detail-footer');
    footer.innerHTML = `
        <button class="rm-btn rm-btn-cancel" style="flex:1" onclick="${isEdit ? `openRecipe(${recipe.id})` : 'closeDetail()'}">Abbrechen</button>
        <button class="rm-btn rm-btn-save" style="flex:1" onclick="saveRecipe(${isEdit ? recipe.id : 'null'})">Speichern</button>
    `;
    footer.style.display = 'flex';

    if (isEdit) {
        recipe.ingredients.forEach(i => addIngredientRow(i));
    } else {
        addIngredientRow();
    }
    setupIngredientDrag();
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
        <span class="rm-drag-handle" title="Ziehen zum Sortieren">⠿</span>
        <div class="rm-row-move-btns">
            <button class="rm-move-btn" title="Nach oben" onclick="moveIngRow(this.closest('.rm-ingredient-row'), -1)">▲</button>
            <button class="rm-move-btn" title="Nach unten" onclick="moveIngRow(this.closest('.rm-ingredient-row'), 1)">▼</button>
        </div>
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

// ── Ingredient drag-and-drop reorder ─────────────────
function setupIngredientDrag() {
    const container = document.getElementById('ingredient-rows');
    if (!container) return;
    let dragSrc = null;

    container.addEventListener('dragstart', e => {
        const row = e.target.closest('.rm-ingredient-row');
        if (!row) return;
        dragSrc = row;
        setTimeout(() => row.classList.add('dragging'), 0);
        e.dataTransfer.effectAllowed = 'move';
    });

    container.addEventListener('dragover', e => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const row = e.target.closest('.rm-ingredient-row');
        if (!row || row === dragSrc) return;
        const rect = row.getBoundingClientRect();
        if (e.clientY < rect.top + rect.height / 2) {
            container.insertBefore(dragSrc, row);
        } else {
            container.insertBefore(dragSrc, row.nextSibling);
        }
    });

    container.addEventListener('dragend', e => {
        const row = e.target.closest('.rm-ingredient-row');
        if (row) row.classList.remove('dragging');
        dragSrc = null;
    });

    // Activate draggable only when drag starts on the handle
    container.addEventListener('mousedown', e => {
        if (e.target.classList.contains('rm-drag-handle')) {
            const row = e.target.closest('.rm-ingredient-row');
            if (row) row.setAttribute('draggable', 'true');
        }
    });
    container.addEventListener('mouseup', () => {
        container.querySelectorAll('.rm-ingredient-row[draggable]').forEach(r => r.removeAttribute('draggable'));
    });
}

function moveIngRow(row, direction) {
    const container = row.parentElement;
    if (direction === -1 && row.previousElementSibling) {
        container.insertBefore(row, row.previousElementSibling);
    } else if (direction === 1 && row.nextElementSibling) {
        container.insertBefore(row.nextElementSibling, row);
    }
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

// ── Select mode ──────────────────────────────────────
function toggleSelectMode() {
    selectMode = !selectMode;
    selectedIds.clear();
    const btn = document.getElementById('select-mode-btn');
    btn.textContent = selectMode ? 'Abbrechen' : 'Auswählen';
    btn.classList.toggle('active', selectMode);
    updateBulkBar();
    if (selectMode) closeDetail();
    renderList(getFilteredRecipes());
}

function toggleSelect(id) {
    if (selectedIds.has(id)) selectedIds.delete(id);
    else selectedIds.add(id);
    updateBulkBar();
    renderList(getFilteredRecipes());
}

function updateBulkBar() {
    const bar = document.getElementById('bulk-bar');
    bar.style.display = selectMode ? 'flex' : 'none';
    const count = selectedIds.size;
    const total = getFilteredRecipes().length;
    document.getElementById('bulk-count').textContent = count > 0 ? `${count} ausgewählt` : 'Alle';
    const cb = document.getElementById('select-all-cb');
    if (cb) {
        cb.checked = count > 0 && count === total;
        cb.indeterminate = count > 0 && count < total;
    }
}

function toggleSelectAll(checked) {
    const filtered = getFilteredRecipes();
    if (checked) filtered.forEach(r => selectedIds.add(r.id));
    else selectedIds.clear();
    renderList(filtered);
    updateBulkBar();
}

async function bulkDelete() {
    const ids = [...selectedIds];
    await fetch('/api/recipes/bulk-delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids })
    });
    toggleSelectMode();
    await loadRecipeList();
    showToast(`${ids.length} Rezept${ids.length === 1 ? '' : 'e'} in den Papierkorb verschoben`);
}

// ── Quick delete (trash button / swipe) ──────────────
async function quickDelete(event, recipeId) {
    event.stopPropagation();
    await fetch(`/api/recipe/${recipeId}`, { method: 'DELETE' });
    if (activeRecipeId === recipeId) closeDetail();
    allRecipes = allRecipes.filter(r => r.id !== recipeId);
    renderList(getFilteredRecipes());
    showToast('In den Papierkorb verschoben');
}

function addSwipeToDelete(li, recipeId) {
    let startX = 0, currentX = 0, swiping = false;
    const THRESHOLD = 80;

    li.addEventListener('touchstart', e => {
        startX = e.touches[0].clientX;
        currentX = 0;
        swiping = true;
        li.style.transition = 'none';
    }, { passive: true });

    li.addEventListener('touchmove', e => {
        if (!swiping) return;
        const dx = e.touches[0].clientX - startX;
        if (dx < 0) {
            currentX = dx;
            li.style.transform = `translateX(${Math.max(dx, -THRESHOLD * 1.5)}px)`;
            li.style.background = Math.abs(dx) > THRESHOLD ? '#ffebee' : '';
        }
    }, { passive: true });

    li.addEventListener('touchend', async () => {
        swiping = false;
        li.style.transition = 'transform 0.2s, background 0.2s';
        if (currentX < -THRESHOLD) {
            li.style.transform = `translateX(-100%)`;
            li.style.opacity = '0';
            await quickDelete({ stopPropagation: () => {} }, recipeId);
        } else {
            li.style.transform = '';
            li.style.background = '';
        }
    });
}

// ── Toast ─────────────────────────────────────────────
function showToast(msg) {
    let t = document.getElementById('rm-toast');
    if (!t) {
        t = document.createElement('div');
        t.id = 'rm-toast';
        t.style.cssText = 'display:none;position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:10px 20px;border-radius:20px;font-size:0.9rem;z-index:800;white-space:nowrap;';
        document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.display = 'block';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.style.display = 'none', 2500);
}

// ── Cart (quick-add to shopping list) ────────────────
let cartRecipeId = null;
let cartServings  = 1.0;

function fmtSrv(n) {
    const v = Math.round(n * 10) / 10;
    return `${Number.isInteger(v) ? v : v.toFixed(1)} Personen`;
}

function openCartSheet(recipeId, recipeName) {
    cartRecipeId = recipeId;
    cartServings  = familySize;
    document.getElementById('rm-cart-recipe-name').textContent = recipeName;
    document.getElementById('rm-cart-servings').textContent = fmtSrv(cartServings);
    document.getElementById('rm-cart-backdrop').style.display = 'block';
    document.getElementById('rm-cart-sheet').style.display = 'block';
}

function closeCartSheet() {
    document.getElementById('rm-cart-backdrop').style.display = 'none';
    document.getElementById('rm-cart-sheet').style.display = 'none';
    cartRecipeId = null;
}

function cartDelta(delta) {
    cartServings = Math.max(0.5, Math.round((cartServings + delta) * 10) / 10);
    document.getElementById('rm-cart-servings').textContent = fmtSrv(cartServings);
}

async function confirmAddToCart() {
    if (!cartRecipeId) return;
    closeCartSheet();
    try {
        const res = await fetch('/api/shopping-list/item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: cartRecipeId, servings: cartServings })
        });
        if (res.ok) showToast('Zur Einkaufsliste hinzugefügt ✓');
        else showToast('Fehler beim Hinzufügen');
    } catch(e) {
        showToast('Netzwerkfehler');
    }
}

// ── Ingredient quick-edit sheet ───────────────────────
const SHOP_CATS = ['Obst & Gemüse','Fleisch & Fisch','Milch & Käse','Brot & Backwaren','Tiefkühl','Konserven & Fertiggerichte','Nudeln, Reis & Hülsenfrüchte','Öle & Gewürze','Getränke','Sonstiges'];
let ingEditId = null;

function openIngEdit(id, name, defaultUnit, isStaple, shopCat) {
    ingEditId = id;
    document.getElementById('ing-edit-name').value = name;
    document.getElementById('ing-edit-unit').value = defaultUnit;
    document.getElementById('ing-edit-staple').checked = isStaple;
    document.getElementById('ing-edit-cat').value = shopCat;
    document.getElementById('ing-edit-backdrop').style.display = 'block';
    document.getElementById('ing-edit-sheet').style.display = 'block';
}


function closeIngEdit() {
    document.getElementById('ing-edit-backdrop').style.display = 'none';
    document.getElementById('ing-edit-sheet').style.display = 'none';
    ingEditId = null;
}

async function saveIngEdit() {
    if (!ingEditId) return;
    const name = document.getElementById('ing-edit-name').value.trim();
    if (!name) return;
    const ok = await showConfirmModal(
        'Zutat global ändern?',
        'Diese Änderungen wirken sich auf alle Rezepte aus, die diese Zutat verwenden.',
        'Fortfahren', 'rm-btn-edit'
    );
    if (!ok) return;
    const res = await fetch(`/api/ingredients/${ingEditId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name,
            default_unit: document.getElementById('ing-edit-unit').value.trim(),
            is_staple: document.getElementById('ing-edit-staple').checked,
            shop_category: document.getElementById('ing-edit-cat').value
        })
    });
    if (res.ok) {
        closeIngEdit();
        showToast('Zutat gespeichert');
        // Refresh detail view if open so name change is visible
        if (activeRecipeId) openRecipe(activeRecipeId);
    } else {
        showToast('Fehler beim Speichern');
    }
}

function escHtml(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function renderIngredientRows(ingredients, extraClass = '') {
    return ingredients.map(i => `
        <tr${extraClass ? ` class="${extraClass}"` : ''}>
            <td>
                ${i.name}
                <button class="rm-ing-edit-btn" title="Zutat bearbeiten"
                    onclick="openIngEdit(${i.ingredient_id}, '${escHtml(i.name)}', '${escHtml(i.default_unit)}', ${i.is_staple}, '${escHtml(i.shop_category)}')">✏️</button>
            </td>
            <td>${fmtAmt(i.amount * familySize)}</td>
            <td>${i.unit}</td>
        </tr>`).join('');
}

function fmtAmt(n) {
    // Up to 2 decimal places, no trailing zeros
    return parseFloat(n.toFixed(2));
}

function portionLabel(n) {
    const s = parseFloat(n.toFixed(2));
    return `für ${s} ${s === 1 ? 'Person' : 'Personen'}`;
}

// ── Generic confirm modal ─────────────────────────────
function showConfirmModal(title, message, confirmText, confirmClass) {
    return new Promise(resolve => {
        const modal = document.getElementById('rm-confirm-modal');
        document.getElementById('rm-confirm-title').textContent = title;
        document.getElementById('rm-confirm-message').textContent = message;
        const okBtn = document.getElementById('rm-confirm-ok');
        okBtn.textContent = confirmText;
        okBtn.className = `rm-btn ${confirmClass}`;
        okBtn.style.flex = '1';
        modal.style.display = 'flex';

        const cleanup = val => {
            modal.style.display = 'none';
            okBtn.onclick = null;
            document.getElementById('rm-confirm-cancel').onclick = null;
            modal.onclick = null;
            resolve(val);
        };
        okBtn.onclick = () => cleanup(true);
        document.getElementById('rm-confirm-cancel').onclick = () => cleanup(false);
        modal.onclick = e => { if (e.target === modal) cleanup(false); };
    });
}

window.onload = init;
