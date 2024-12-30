document.addEventListener("DOMContentLoaded", () => {
  const datetimeInput = document.getElementById("datetime");

  const dateInput = document.getElementById("date");
  const timeDropdown = document.getElementById("time");

  // Set the date input to only allow dates for the next week
  window.onload = () => {
    const now = new Date();
    const nextWeek = new Date();
    nextWeek.setDate(now.getDate() + 7);

    // Set the min and max attributes for the date picker
    const minDate = now.toISOString().split("T")[0]; // Format YYYY-MM-DD
    const maxDate = nextWeek.toISOString().split("T")[0];

    dateInput.setAttribute("min", minDate);
    dateInput.setAttribute("max", maxDate);

    // Populate the time dropdown with options
    populateTimeDropdown();
  };

  // Populate the time dropdown with time slots between 10:00 AM and 6:00 PM
  function populateTimeDropdown() {
    for (let hour = 10; hour <= 18; hour++) {
      const period = hour >= 12 ? "PM" : "AM";
      const displayHour = hour > 12 ? hour - 12 : hour;
      const timeOption = `${displayHour}:00 ${period}`;

      const option = document.createElement("option");
      option.value = timeOption;
      option.textContent = timeOption;

      timeDropdown.appendChild(option);
    }
  }

  // Prevent Sunday selection
  dateInput.addEventListener("input", () => {
    const selectedDate = new Date(dateInput.value);
    if (selectedDate.getDay() === 1) {
      alert("Mondays are not allowed. Please select another date.");
      dateInput.value = ""; // Clear invalid selection
    }
  });
});
