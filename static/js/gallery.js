document.addEventListener("DOMContentLoaded", function () {
  const eventDialog = document.getElementById("eventDialog");
  const title = document.getElementById("dialogTitle");
  const location = document.getElementById("dialogLocation");
  const date = document.getElementById("dialogDate");
  const time = document.getElementById("dialogTime");
  const description = document.getElementById("dialogDescription");
  const closeBtn = document.querySelector("#eventDialog .close");

  // Show dialog when event is clicked
  window.openModal = function (eventName, eventDate, eventTime, eventLocation, eventDescription) {
      title.innerText = eventName;
      date.innerText = eventDate;
      time.innerText = eventTime;
      location.innerText = eventLocation;
      description.innerText = eventDescription;
      eventDialog.showModal();
  };

  // Close the dialog box
  if (closeBtn) {
      closeBtn.addEventListener("click", function () {
          eventDialog.close();
      });
  }
});
