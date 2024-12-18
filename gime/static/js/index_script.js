document.getElementById('menu-toggle').addEventListener('click', function() {
    document.getElementById('filter-panel').classList.toggle('open');
});

document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.getElementById('filter-toggle');
    const filterPanel = document.getElementById('filter-panel');

    filterButton.addEventListener('click', () => {
        filterPanel.classList.toggle('visible');
    });
});
