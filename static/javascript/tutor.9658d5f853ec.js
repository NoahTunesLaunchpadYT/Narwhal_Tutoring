document.addEventListener('DOMContentLoaded', () => {

  var timesBookedDiv = document.querySelector('#times-booked');
  var bookedTimes = []; // Array to store booked times

  // Calendar
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        start: 'dayGridYear,dayGridMonth,timeGridWeek',
        center: 'title',
        end: 'today prev,next',
      },
      initialView: 'timeGridWeek',
      timeZone: 'Asia/Singapore',
      locale: 'en-AU',
      slotMinTime: '08:00:00',
      slotMaxTime: '22:00:00',
      selectable: true,
      selectMirror: true,
      eventOverlap: true,
      events: {
          url: `/get_calendar/${tutorId}`,
          headers: {
              'X-CSRFToken': csrfToken
          },
      },
      eventClick: handleEventClick,
      select: handleSelect,
      editable: function(event) {
        return event.title != "Booked";
      },
      eventStartEditable: true,
      eventResizableFromStart: true,
      eventDurationEditable: true,
      eventAllow: eventAllow,
      selectAllow: eventAllow,
      selectOverlap: function(event) {
        if (event.display === 'background'){
          console.log("intersecting")
        }
        return event.display === 'background';
      }
  });

  function eventAllow(dropInfo) {
    var allEvents = calendar.getEvents();
    var currentDate = new Date();
    var allow = false;
  
    if (dropInfo.end >= currentDate) {
      for (var i = 0; i < allEvents.length; i++) {
        var event = allEvents[i];
    
        // Check if the new event overlaps with an existing event
        if (event.start <= dropInfo.start && event.end >= dropInfo.end) {
          allow = true;
        } else {
          console.log(`${dropInfo.start}-${dropInfo.end} not in availability ${event.start}-${event.end}\n`)
        }
      }
    } else {
      console.log("Can't select time in past.")
    }

    if (allow == false){
      console.log("Not in availability")
    }
  
    return allow;
  }
  

  function handleEventClick(arg) {
    var currentDate = new Date();

    console.log(arg.event.groupId);
    if (arg.event.groupId == 'availabilityGroup') {
        if (arg.event.end < currentDate) {
            alert("You can not book lessons in the past");
        }
    } else {
        if (confirm('Do you want to delete this event (and any ascociated recurring events)?')) {
            // Get all events with the same groupId
            var eventsToDelete = calendar.getEvents().filter(event => event.groupId === arg.event.groupId);

            // Remove each event from the calendar
            eventsToDelete.forEach(event => event.remove());

            updateBookedTimesList();
        }
    }
  }

  function handleSelect(arg) {
    var weeks = parseInt(prompt("For how many weeks do you want this lesson to occur?\n('1' means no repetition).\n Please enter an integer."));

    // Check if the conversion was successful and weeks is greater than 0
    if (!isNaN(weeks) && weeks > 0) {
        console.log("You entered: " + weeks);

        // Get the start date of the selected event
        var startDate = new Date(arg.start);
        var endDate = new Date(arg.end);

        // Loop to create events for the specified number of weeks
        for (var i = 0; i < weeks; i++) {
            // Calculate the start and end dates for each week
            var newStart = new Date(startDate.getTime() + i * 7 * 24 * 60 * 60 * 1000);
            var newEnd = new Date(endDate.getTime() + i * 7 * 24 * 60 * 60 * 1000);

            // Create an event object with the same properties as the original event
            var newEvent = {
                ...arg,
                groupId: arg.start,
                start: newStart,
                end: newEnd
            };

            // Add the new event to the calendar
            calendar.addEvent(newEvent);
        }

        updateBookedTimesList();
    } else {
        console.log("Invalid input. Please enter a valid integer greater than 0.");
    }
    calendar.unselect()
  }

  setTimeout(function() {
      calendar.render();
  });

  function updateBookedTimesList() {
    allEvents = calendar.getEvents();
    
    var duration = 0;

    allEvents.forEach((event) => {
      if(event.groupId != "availabilityGroup"){
        duration += event.end - event.start;
      }
    })

    // Clear the current list
    timesBookedDiv.innerHTML = '';

    let priceCards = document.querySelectorAll(".price-tag")
      priceCards.forEach((card) => {
        card.style.backgroundColor = 'white';
    })
    
    if (duration/1000/60/60 > 0){
      // Create a new list based on the bookedTimes array
      let selectedMessage = document.createElement('p');
      selectedMessage.textContent = "Selected times: "
      timesBookedDiv.appendChild(selectedMessage);

      allEvents.forEach((event) => {
        if(event.groupId != "availabilityGroup"){
          var listItem = document.createElement('li');
          var time = event.start.toISOString();
          var date = new Date(time);

          var options = {
            weekday: 'short', // Abbreviated day name (e.g., Mon)
            hour: 'numeric',  // Numeric hour (e.g., 14)
            minute: 'numeric', // Numeric minute (e.g., 00)
            day: 'numeric',    // Numeric day of the month (e.g., 05)
            month: 'numeric',  // Numeric month (e.g., 02)
            year: 'numeric'    // Numeric year (e.g., 2024)
          };
          
          // Format the date according to the options
          var formattedTime = date.toLocaleString('en-AU', options);

          listItem.textContent = formattedTime;
          timesBookedDiv.appendChild(listItem);
          console.log(event);
        }
      })

      hours = parseInt(duration/1000/60/60);

      var bundle = 1;
      var totalCost = 0;

      if(hours < 5){
        bundle = 1;
        totalCost = (duration/1000/60/60) * 70
      } else if (hours < 10){
        bundle = 2;
        totalCost = 315 + ((duration/1000/60/60)-5) * 63
        console.log(hours);
        console.log(bundle);
        console.log(totalCost);
      } else {
        bundle = 3;
        totalCost = 600 + ((duration/1000/60/60)-10) * 60
      }
      

      let hoursMessage = document.createElement('p');
      hoursMessage.textContent = "You are making a booking for: " + duration/1000/60/60 + " hrs";
      timesBookedDiv.appendChild(hoursMessage);
      let costMessage = document.createElement('p');
      costMessage.textContent = "Total Cost: $" + totalCost;
      timesBookedDiv.appendChild(costMessage);

      let priceCardId = "#hr-" + bundle;
      let priceCard = document.querySelector(priceCardId);
      priceCard.style.backgroundColor = 'lightblue';

      var checkoutButton = document.getElementById('checkout-button');
      checkoutButton.style.display = 'block';  // Set the display property to 'block' or 'inline' as needed
      checkoutButton.disabled = false;  // Enable the button
    } else {

      message = document.createElement('p');
      message.textContent = "You have no times selected."
      timesBookedDiv.appendChild(message);
    }
  }

  var form = document.getElementById('checkout-form');
  form.addEventListener('submit', function (event) {
      event.preventDefault();

      const cart = calendar.getEvents();
      console.log(cart)

      fetch('/save-lessons-to-cart/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ 
            'lessons_data': cart,
            'tutorId': tutorId, 
          }),
      })
      .then(response => response.json())
      .then(data => {
          console.log(data.message); // You can handle success here
          form.action = `${checkOutUrl}`

          // Submit the form
          form.submit();
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });

});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}