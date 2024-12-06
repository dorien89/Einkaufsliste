let shoppingList = [];

function toggleShoppingList() {
    const overlay = document.getElementById('shopping-list-overlay');
    overlay.classList.toggle('hidden');
}

function addToShoppingList(recipeId, recipeName) {
    if (shoppingList.length >= 20) {
        alert('Die Einkaufsliste ist voll. Es können keine weiteren Rezepte hinzugefügt werden.');
        return;
    }

    const existingItem = shoppingList.find(item => item.id === recipeId);

    if (!existingItem) {
        shoppingList.push({ id: recipeId, name: recipeName, servings: 1 });
        console.log(`Rezept hinzugefügt: ${recipeName} (1 Portion)`);
    } else {
        existingItem.servings += 1;
        console.log(`Portionen erhöht für: ${recipeName} (jetzt ${existingItem.servings} Portionen)`);
    }

    renderShoppingList();
}


function renderShoppingList() {
    const listElement = document.getElementById('shopping-list-items');
    listElement.innerHTML = '';
    shoppingList.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.servings} Portion(en)`;
        listElement.appendChild(li);
    });
}

function clearShoppingList() {
    shoppingList = [];
    renderShoppingList();
    console.log('Einkaufsliste geleert.');
}

async function exportShoppingList() {
    if (shoppingList.length === 0) {
        console.log('Einkaufsliste ist leer. Nichts zu exportieren.');
        return;
    }

    console.log('About to send:', { items: shoppingList });

    const isValid = shoppingList.every(item => item.id && item.servings !== undefined);
    if (!isValid) {
        alert('Die Einkaufsliste enthält ungültige Daten.');
        return;
    }

    try {
        const response = await fetch('/api/shopping-list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ items: shoppingList }),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Backend error:', data.error || response.statusText);
            alert(`Fehler vom Server: ${data.error || response.statusText}`);
            return;
        }

        console.log('Einkaufsliste erfolgreich exportiert:', data);
        alert('Einkaufsliste wurde erfolgreich exportiert.');

        shoppingList = [];
        renderShoppingList();
    } catch (error) {
        console.error('Fehler beim Exportieren der Einkaufsliste:', error);
        alert('Fehler beim Exportieren der Einkaufsliste.');
    }
}


async function loadRecipes() {
    try {
        const randomParam = `?nocache=${Date.now()}`;
        const response = await fetch('/api/recipes' + randomParam);
        const recipes = await response.json();
        const container = document.querySelector('.grid-container');
        container.innerHTML = '';

        recipes.forEach(recipe => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.textContent = recipe.name;
            div.dataset.recipeId = recipe.id;

            div.addEventListener('click', () => {
                console.log('Rezept geklickt:', recipe.name);
                addToShoppingList(recipe.id, recipe.name);
                div.classList.add('clicked');
                setTimeout(() => div.classList.remove('clicked'), 500);
            });

            container.appendChild(div);
        });
    } catch (error) {
        console.error('Fehler beim Laden der Rezepte:', error);
    }
}

async function loadNewRecipes() {
    try {
        const randomParam = `?nocache=${Date.now()}`;
        const response = await fetch('/api/recipes' + randomParam);
        const recipes = await response.json();
        const container = document.querySelector('.grid-container');
        container.innerHTML = '';

        recipes.forEach(recipe => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.textContent = recipe.name;
            div.dataset.recipeId = recipe.id;

            div.addEventListener('click', () => {
                console.log('Rezept geklickt:', recipe.name);
                addToShoppingList(recipe.id, recipe.name);
                div.classList.add('clicked');
                setTimeout(() => div.classList.remove('clicked'), 500);
            });

            container.appendChild(div);
        });
    } catch (error) {
        console.error('Fehler beim Laden der Rezepte:', error);
    }
}

window.onload = loadRecipes;