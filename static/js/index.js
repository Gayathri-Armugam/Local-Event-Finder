document.addEventListener("DOMContentLoaded", function () {
  const eventDialog = document.getElementById("eventDialog");
  const title = document.getElementById("dialogTitle");
  const location = document.getElementById("dialogLocation");
  const date = document.getElementById("dialogDate");
  const time = document.getElementById("dialogTime");
  const description = document.getElementById("dialogDescription");
  const closeBtn = document.querySelector("#eventDialog .close");

  // 1. Show dialog when event is clicked
  window.openModal = function (eventName, eventDate, eventTime, eventLocation, eventDescription) {
    title.innerText = eventName;
    date.innerText = eventDate;
    time.innerText = eventTime;
    location.innerText = eventLocation;
    description.innerText = eventDescription;
    eventDialog.showModal();
  };

  // 2. Close the dialog box
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      eventDialog.close();
    });
  }

  // 3. Search / Filter functionality
  const searchInput = document.getElementById("searchInput");
  const eventCards = document.querySelectorAll(".event-card");

  // Define allowed categories (adjust based on your actual categories)
  const allowedCategories = ["Music", "Sports", "Art", "Tech", "Food", "Education"];

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = searchInput.value.trim();

      if (query === "") {
        // If search is empty, show all events
        eventCards.forEach(card => (card.style.display = "block"));
        return;
      }

      // Validate the input category
      if (!allowedCategories.includes(query)) {
        // Invalid category entered
        eventCards.forEach(card => (card.style.display = "none"));
        alert(`Category "${query}" not found. Please enter one of: ${allowedCategories.join(", ")}`);
        return;
      }

      // Filter and show only matching category events
      let matchesFound = false;
      eventCards.forEach(card => {
        if (card.dataset.category.toLowerCase() === query.toLowerCase()) {
          card.style.display = "block";
          matchesFound = true;
        } else {
          card.style.display = "none";
        }
      });

      if (!matchesFound) {
        alert(`No events found in category "${query}".`);
      }
    });
  }
});
