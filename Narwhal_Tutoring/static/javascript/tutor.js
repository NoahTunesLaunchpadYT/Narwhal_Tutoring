document.addEventListener('DOMContentLoaded', () => {

  var timesBookedDiv = document.querySelector('#times-booked');
  var bookedTimes = []; // Array to store booked times

  // Calendar
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      timeZone: 'Asia/Singapore',
      locale: 'en-AU',
      slotMinTime: '08:00:00',
      slotMaxTime: '22:00:00',
      selectable: true,
      selectMirror: true,
      eventOverlap: true,
      events: {
          url: `/get_availability/${tutorId}`,
          headers: {
              'X-CSRFToken': csrfToken
          },
          // Default properties for events
          display: 'background', // or any other default property
      },
      eventClick: handleEventClick,
      select: handleSelect,
      editable: true,
      eventStartEditable: true,
      eventResizableFromStart: true,
      eventDurationEditable: true,
  });

  function handleEventClick(arg) {
    if (confirm('Do you want to delete this selection?')) {
        // Remove the event from the calendar
        arg.event.remove();
    }
  }

  function handleSelect(arg) {
    calendar.addEvent(arg);
  }


  
  setTimeout(function() {
      calendar.render();
  });

  function updateBookedTimesList() {
    calendar.getEvents()
    // Clear the current list
    timesBookedDiv.innerHTML = '';

    let priceCards = document.querySelectorAll(".price-tag")
      priceCards.forEach((card) => {
        card.style.backgroundColor = 'white';
    })
    
    if (bookedTimes.length > 0){
      // Create a new list based on the bookedTimes array
      let selectedMessage = document.createElement('p');
      selectedMessage.textContent = "Selected times: "
      timesBookedDiv.appendChild(selectedMessage);
      
      bookedTimes.forEach((time) => {
        var listItem = document.createElement('li');
        time = time.replace('-', ' ');
        listItem.textContent = capitalizeFirstLetter(time);
        timesBookedDiv.appendChild(listItem);
      });

      costsIndex = bookedTimes.length

      if (costsIndex > 4) {
        costsIndex = 4;
      }

      let costs = [0, 70, 63, 60, 58, 58]

      let hoursMessage = document.createElement('p');
      hoursMessage.textContent = "You are making a booking for: " + bookedTimes.length + " hr/week";
      timesBookedDiv.appendChild(hoursMessage);
      let costMessage = document.createElement('p');
      costMessage.textContent = "Rate: $" + costs[costsIndex] + "/hr";
      timesBookedDiv.appendChild(costMessage);

      let priceCardId = "#hr-" + costsIndex;
      let priceCard = document.querySelector(priceCardId);
      priceCard.style.backgroundColor = 'lightblue';
    } else {

      message = document.createElement('p');
      message.textContent = "You have no times selected."
      timesBookedDiv.appendChild(message);
    }
  }
});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}