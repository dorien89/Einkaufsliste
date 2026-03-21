let shoppingList = [];

function toggleShoppingList() {
    const overlay = document.getElementById('shopping-list-overlay');
    overlay.classList.toggle('hidden');
}

async function addToShoppingList(recipeId, recipeName) {
    const existingItem = shoppingList.find(item => item.id === recipeId);
    if (existingItem) {
        existingItem.servings += 1;
    } else {
        shoppingList.push({ id: recipeId, name: recipeName, servings: 1 });
    }
    renderShoppingList();

    await fetch('/api/shopping-list/item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: recipeId }),
    });
}

async function removeFromShoppingList(recipeId) {
    shoppingList = shoppingList.filter(item => item.id !== recipeId);
    renderShoppingList();

    await fetch(`/api/shopping-list/item/${recipeId}`, { method: 'DELETE' });
}

async function changeServings(recipeId, delta) {
    const item = shoppingList.find(i => i.id === recipeId);
    if (!item) return;

    if (item.servings + delta <= 0) {
        await removeFromShoppingList(recipeId);
        return;
    }

    item.servings += delta;
    renderShoppingList();

    await fetch(`/api/shopping-list/item/${recipeId}/servings`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ servings: item.servings }),
    });
}

function renderShoppingList() {
    const listElement = document.getElementById('shopping-list-items');
    listElement.innerHTML = '';
    shoppingList.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="item-name">${item.name}</span>
            <div class="item-controls">
                <button class="stepper-btn" onclick="changeServings(${item.id}, -1)">−</button>
                <span class="item-servings">${item.servings}</span>
                <button class="stepper-btn" onclick="changeServings(${item.id}, 1)">+</button>
                <button class="remove-btn" onclick="removeFromShoppingList(${item.id})">✕</button>
            </div>
        `;
        listElement.appendChild(li);
    });

    const badge = document.getElementById('list-badge');
    const total = shoppingList.reduce((sum, item) => sum + item.servings, 0);
    if (total > 0) {
        badge.textContent = total;
        badge.classList.remove('hidden');
    } else {
        badge.classList.add('hidden');
    }

    document.querySelectorAll('.grid-item').forEach(tile => {
        const id = parseInt(tile.dataset.recipeId);
        const item = shoppingList.find(i => i.id === id);
        if (item) {
            tile.classList.add('in-list');
            tile.dataset.portions = item.servings;
        } else {
            tile.classList.remove('in-list');
            delete tile.dataset.portions;
        }
    });
}

async function clearShoppingList() {
    for (const item of shoppingList) {
        await fetch(`/api/shopping-list/item/${item.id}`, { method: 'DELETE' });
    }
    shoppingList = [];
    renderShoppingList();
}

function goToShoppingList() {
    if (shoppingList.length === 0) return;
    window.location.href = '/shopping-list/';
}

async function loadRecipes() {
    try {
        const response = await fetch(`/api/recipes?nocache=${Date.now()}`);
        const recipes = await response.json();
        const container = document.querySelector('.grid-container');
        container.innerHTML = '';

        recipes.forEach(recipe => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.textContent = recipe.name;
            div.dataset.recipeId = recipe.id;

            div.addEventListener('click', () => {
                addToShoppingList(recipe.id, recipe.name);
                div.classList.add('clicked');
                setTimeout(() => div.classList.remove('clicked'), 500);
            });

            container.appendChild(div);
        });

        renderShoppingList();
    } catch (error) {
        console.error('Fehler beim Laden der Rezepte:', error);
    }
}

async function loadDraft() {
    try {
        const response = await fetch('/api/shopping-list/draft');
        const data = await response.json();
        if (data.success) {
            shoppingList = data.items;
        }
    } catch (error) {
        console.error('Fehler beim Laden der Einkaufsliste:', error);
    }
}

window.onload = async () => {
    await loadDraft();
    await loadRecipes();
};
