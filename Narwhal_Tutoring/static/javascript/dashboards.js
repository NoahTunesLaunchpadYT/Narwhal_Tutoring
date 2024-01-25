document.addEventListener('DOMContentLoaded', function() {
    var tabLinks = document.querySelectorAll('.list-group-item');

    tabLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            var targetTab = this.getAttribute('href').substr(1);
            history.pushState({ tab: targetTab }, null, this.getAttribute('href'));
        });
    });

    window.onpopstate = function(event) {
        console.log(event.state.tab)
        showTab(event.state.tab);
    };

    var initialTab = window.location.hash.substr(1);
    if (initialTab) {
        showTab(initialTab);
    }

    function showTab(tabId) {
        tabLinks.forEach(function (link) {
            link.classList.remove('active');
        });

        var tabContent = document.querySelector('.tab-pane');
        tabContent.classList.remove('show', 'active');

        var activeLink = document.querySelector(`.list-group-item[href="#${tabId}"]`);
        var activeTab = document.querySelector(`#${tabId}`);

        activeLink.classList.add('active');
        activeTab.classList.add('show', 'active');
    }

    var timetableCells = document.querySelectorAll('.timetable-cell');
    var isDragging = false;
    var isSelecting = true;  // Initial state is selecting
    var selectedCells = [];

    timetableCells.forEach(function(cell) {
        var hiddenInput = cell.querySelector('.timeslot');
        cell.addEventListener('mousedown', function(event) {
            isDragging = true;
            selectedCells.push(cell);

            if (cell.classList.contains('selected')) {
                isSelecting = false;
                cell.classList.remove('selected');
                hiddenInput.value = 'false'
            } else {
                isSelecting = true;
                cell.classList.add('selected');
                hiddenInput.value = 'true'
            }
        });

        cell.addEventListener('mouseover', function() {
            if (isDragging) {
                selectedCells.push(cell);

                if (isSelecting) {
                    cell.classList.add('selected');
                    hiddenInput.value = 'true'
                } else {
                    cell.classList.remove('selected');
                    hiddenInput.value = 'false'
                }
            }
        });

        cell.addEventListener('mouseup', function() {
            isDragging = false;
            selectedCells = [];
        });
    });
});