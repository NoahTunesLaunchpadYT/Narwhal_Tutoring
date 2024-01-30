document.addEventListener('DOMContentLoaded', function() {

    // Calendar
    
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'en-AU',
        slotMinTime: '08:00:00',
        slotMaxTime: '22:00:00',
        selectable: true,
        selectMirror: true,
        eventOverlap: false,
        events: {
            url: '/get_availability/',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
        },
        eventClick: handleEventClick,
        select: handleSelect,
    });
    
    setTimeout(function() {
        calendar.render();
    });
    
    function handleSelect(arg) {
        // Check if the selected time range overlaps with existing events
        var isOverlapping = calendar.getEvents().some(function (existingEvent) {
            return (
                arg.start < existingEvent.end && arg.end > existingEvent.start &&
                existingEvent.groupId === 'availabilityGroup'
            );
        });
    
        if (!isOverlapping) {
            // Create a new FullCalendar event with a default title and the selected time range
            var uniqueId = new Date().getTime();
            var newEvent = {
                title: 'Availability',
                start: arg.start,  // Ensure ISO string format with time zone
                end: arg.end,
                allDay: arg.allDay,
                groupId: 'availabilityGroup', // Set a common groupId for all availability events
                id: uniqueId,
                editable: true,
            };
    
            console.log(`Start (raw): ${arg.start}`);
            console.log(`End (raw): ${arg.end}`);
            // Add the event to the calendar
            calendar.addEvent(newEvent);

             // Save the event to the database (you need to implement this part)
            saveEventToDatabase(newEvent);
    
            // Unselect the currently selected time range
            calendar.unselect();
        } else {
            alert('Overlapping events are not allowed.');
            calendar.unselect();
        }
    }
    
    function handleEventClick(arg) {
        if (confirm('Do you want to delete this availability?')) {
            // Remove the event from the calendar
            arg.event.remove();

            deleteEventFromDatabase(arg.event);
        }
    }

    function saveEventToDatabase(event) {
        fetch('/save_availability/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(event),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Event saved to the database:', data);
        })
        .catch(error => {
            console.error('Error saving event to the database:', error);
        });
        console.log('Event ID:', event.id);
    }
    
    function deleteEventFromDatabase(event) {
        // Check if event.id is defined before making the DELETE request
        if (event.id !== undefined) {
            console.log('Event ID:', event.id);
            fetch(`/delete_availability/${event.id}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log('Event deleted from the database:', data);
            })
            .catch(error => {
                console.error('Error deleting event from the database:', error);
            });
        } else {
            console.error('Event ID is undefined.');
        }
    }
    
    
    function getCSRFToken() {
        // Retrieve CSRF token from the HTML DOM or any other method you use
        return document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }


    // Navbar

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

    var timetableCells = document.querySelectorAll('.dashboard-timetable-cell');
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