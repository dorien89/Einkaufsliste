document.addEventListener("DOMContentLoaded", () => {
    const selectedRecipes = [];
    const availableRecipesList = document.getElementById("available-recipes-list");
    const selectedRecipesList = document.getElementById("selected-recipes-list");

    // Rezepte abrufen und anzeigen
    fetch('/api/rezepte')
        .then(response => response.json())
        .then(data => {
            data.forEach(rezept => {
                const li = document.createElement("li");
                li.className = "recipe-item";
                li.innerHTML = `
                    <span>${rezept.name}</span>
                    <button onclick="addToSelected(${rezept.id}, '${rezept.name}')">Hinzufügen</button>
                `;
                availableRecipesList.appendChild(li);
            });
        });

    // Rezept hinzufügen
    window.addToSelected = (id, name) => {
        if (selectedRecipes.find(r => r.id === id)) return; // Verhindern von Duplikaten
        const recipe = { id, name, portionen: 1 };
        selectedRecipes.push(recipe);
        renderSelectedRecipes();
    };

    // Ausgewählte Rezepte anzeigen
    function renderSelectedRecipes() {
        selectedRecipesList.innerHTML = "";
        selectedRecipes.forEach(recipe => {
            const li = document.createElement("li");
            li.className = "recipe-item";
            li.innerHTML = `
                <span>${recipe.name}</span>
                <div class="controls">
                    <button onclick="updatePortion(${recipe.id}, -1)">-</button>
                    <span>${recipe.portionen}</span>
                    <button onclick="updatePortion(${recipe.id}, 1)">+</button>
                </div>
            `;
            selectedRecipesList.appendChild(li);
        });
    }

    // Portionsanzahl ändern
    window.updatePortion = (id, delta) => {
        const recipe = selectedRecipes.find(r => r.id === id);
        if (recipe) {
            recipe.portionen = Math.max(1, recipe.portionen + delta);
            renderSelectedRecipes();
        }
    };

    // Daten senden
    document.getElementById("send-button").addEventListener("click", () => {
        fetch('/api/einkaufsliste', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items: selectedRecipes })
        }).then(() => alert("Einkaufsliste aktualisiert!"));
    });
});
