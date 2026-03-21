let shoppingList = [];
let carouselIndex = 0;

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

function renderCarousel() {
    const card = document.getElementById('carousel-card');
    const counter = document.getElementById('carousel-counter');
    const prev = document.getElementById('carousel-prev');
    const next = document.getElementById('carousel-next');

    if (shoppingList.length === 0) {
        card.innerHTML = '<div class="carousel-empty">Keine Rezepte gewählt</div>';
        counter.textContent = '';
        prev.disabled = true;
        next.disabled = true;
        return;
    }

    if (carouselIndex >= shoppingList.length) carouselIndex = shoppingList.length - 1;
    if (carouselIndex < 0) carouselIndex = 0;

    const item = shoppingList[carouselIndex];
    card.innerHTML = `
        <span class="item-name">${item.name}</span>
        <div class="item-controls">
            <button class="stepper-btn" onclick="changeServings(${item.id}, -1)">−</button>
            <span class="item-servings">${item.servings}</span>
            <button class="stepper-btn" onclick="changeServings(${item.id}, 1)">+</button>
            <button class="remove-btn" onclick="removeFromShoppingList(${item.id})">✕</button>
        </div>
    `;
    counter.textContent = `${carouselIndex + 1} / ${shoppingList.length}`;
    prev.disabled = carouselIndex === 0;
    next.disabled = carouselIndex === shoppingList.length - 1;
}

function carouselPrev() {
    if (carouselIndex > 0) { carouselIndex--; renderCarousel(); }
}

function carouselNext() {
    if (carouselIndex < shoppingList.length - 1) { carouselIndex++; renderCarousel(); }
}

function renderShoppingList() {
    renderCarousel();

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
