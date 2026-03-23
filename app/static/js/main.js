// Apply saved kiosk theme to all pages
(function() {
    const theme = localStorage.getItem('kiosk-theme') || 'küche';
    document.documentElement.setAttribute('data-theme', theme);
})();

// Zutaten eines Rezepts anzeigen
async function showIngredients(recipeId) {
    const ingredientsDiv = document.getElementById(`ingredients-${recipeId}`);
    
    // Toggle Anzeige
    if (ingredientsDiv.innerHTML !== '') {
        ingredientsDiv.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/recipe/ingredients/${recipeId}`);
        const ingredientsHtml = await response.text();
        ingredientsDiv.innerHTML = ingredientsHtml;
    } catch (error) {
        console.error('Fehler beim Laden der Zutaten:', error);
        ingredientsDiv.innerHTML = '<p>Fehler beim Laden der Zutaten.</p>';
    }
}

// Dynamisches Hinzufügen von Zutateneingabefeldern
function addIngredient() {
    const container = document.getElementById('ingredients-container');
    const newRow = document.createElement('div');
    newRow.className = 'ingredient-row';
    
    // Kopiere die erste Zeile und leere die Eingabefelder
    const firstRow = container.querySelector('.ingredient-row');
    newRow.innerHTML = firstRow.innerHTML;
    newRow.querySelectorAll('input').forEach(input => input.value = '');
    
    container.appendChild(newRow);
}

// Entfernen einer Zutateneingabezeile
function removeIngredient(button) {
    const container = document.getElementById('ingredients-container');
    if (container.querySelectorAll('.ingredient-row').length > 1) {
        button.closest('.ingredient-row').remove();
    }
}

// Zufällige Rezepte auf der Startseite laden
async function loadRandomRecipes() {
    const recipesContainer = document.getElementById('random-recipes');
    if (!recipesContainer) return;

    try {
        const response = await fetch('/api/recipes');
        const recipes = await response.json();
        
        let html = '<h2>Zufällige Rezeptvorschläge</h2><div class="recipes-grid">';
        recipes.forEach(recipe => {
            html += `
                <div class="recipe-card">
                    <h3>${recipe.name}</h3>
                    <a href="/recipe/calculate/${recipe.id}" class="btn">Portionen berechnen</a>
                </div>
            `;
        });
        html += '</div>';
        
        recipesContainer.innerHTML = html;
    } catch (error) {
        console.error('Fehler beim Laden der Rezepte:', error);
        recipesContainer.innerHTML = '<p>Fehler beim Laden der Rezeptvorschläge.</p>';
    }
}

// Event Listener für die Startseite
document.addEventListener('DOMContentLoaded', () => {
    loadRandomRecipes();
});

// Shopping List Funktionalität
async function addToShoppingList(recipeId, servings) {
    try {
        const response = await fetch('/api/shopping-list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                items: [{
                    id: recipeId,
                    servings: servings
                }]
            })
        });
        
        if (response.ok) {
            alert('Zur Einkaufsliste hinzugefügt!');
        } else {
            throw new Error('Fehler beim Speichern');
        }
    } catch (error) {
        console.error('Fehler:', error);
        alert('Fehler beim Hinzufügen zur Einkaufsliste');
    }
}