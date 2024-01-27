document.addEventListener('DOMContentLoaded', () => {

  var timetableCells = document.querySelectorAll('.timetable-cell');
  var timesBookedDiv = document.querySelector('#times-booked');
  var bookedTimes = []; // Array to store booked times

  timetableCells.forEach((cell) => {
    var hiddenInput = cell.querySelector('.timeslot');

    cell.onclick = () => {
      if (cell.classList.contains('available')) {
        if (cell.classList.contains('selected')) {
          cell.classList.remove('selected');
          hiddenInput.value = 'false';

          // Remove the booked time from the array
          const index = bookedTimes.indexOf(hiddenInput.name);
          if (index !== -1) {
            bookedTimes.splice(index, 1);
          }
        } else {
          cell.classList.add('selected');
          hiddenInput.value = 'true';

          // Add the booked time to the array
          bookedTimes.push(hiddenInput.name);
        }

        // Update the list of booked times
        updateBookedTimesList();
      }
    };
  });

  function updateBookedTimesList() {
    // Clear the current list
    timesBookedDiv.innerHTML = '';

    let priceCards = document.querySelectorAll(".price-tag")
      priceCards.forEach((card) => {
        card.style.backgroundColor = 'white';
    })
    
    if (bookedTimes.length > 0){
      // Create a new list based on the bookedTimes array
      bookedTimes.forEach((time) => {
        var listItem = document.createElement('li');
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