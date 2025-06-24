document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:8000/api/events/")
    .then(response => response.json())
    .then(events => {
      const eventList = document.getElementById("event-list");
      eventList.innerHTML = "";

      events.forEach(event => {
        const card = document.createElement("div");
        card.className = "event-card";

        card.innerHTML = `
          <h2>${event.title}</h2>
          <p>${event.description}</p>
          <p><strong>Date:</strong> ${event.date}</p>
          <button onclick="registerEvent(${event.id})">Register</button>
        `;

        eventList.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Error loading events:", err);
      document.getElementById("event-list").innerHTML = "Failed to load events.";
    });
});
