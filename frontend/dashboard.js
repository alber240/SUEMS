const EVENTS_API = "http://127.0.0.1:8000/api/events/";
const FEEDBACK_API = "http://127.0.0.1:8000/api/feedback/";
const token = localStorage.getItem("token");
const userId = localStorage.getItem("user_id");

// Redirect if not logged in
if (!token) {
    alert("Unauthorized! Please login.");
    window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", () => {
    const feedbackForm = document.getElementById("feedbackForm");
    if (feedbackForm) {
      feedbackForm.addEventListener("submit", submitFeedback);
    }
    loadEvents();
});

// Load and display events with auth token
function loadEvents() {
    fetch(EVENTS_API, {
        headers: { "Authorization": `Token ${token}` }
    })
    .then(res => res.json())
    .then(events => {
        const container = document.getElementById("events-container");
        if (!container) return;
        container.innerHTML = "";
        events.forEach(event => {
            const card = document.createElement("div");
            card.className = "event-card";
            // Use title or name fallback, safely encode event name once
            const eventTitle = event.title || event.name || "Event";
            const encodedName = encodeURIComponent(eventTitle);
            card.innerHTML = `
                <h3>${eventTitle}</h3>
                <p>${event.description || ""}</p>
                <p><strong>Date:</strong> ${event.date || "TBD"}</p>
                <button class="register-button" onclick="registerForEvent(${event.id}, '${encodedName}')">Register</button>
            `;
            container.appendChild(card);
        });
    })
    .catch(() => {
        showNotification("Failed to load events.", true);
    });
}

// Redirect to registration page with URL params
function registerForEvent(eventId, encodedEventName) {
  // encodedEventName is already encoded in loadEvents, no need to encode again
  window.location.href = `register.html?event_id=${eventId}&event_name=${encodedEventName}`;
}

// Show notification messages on UI
function showNotification(message, isError = false) {
    const notification = document.getElementById("notification");
    if (!notification) return;
    notification.textContent = message;
    notification.style.color = isError ? "red" : "green";
    notification.style.display = "block";
    setTimeout(() => {
        notification.style.display = "none";
    }, 5000);
}

// Submit feedback handler
function submitFeedback(e) {
    e.preventDefault();
    const feedbackInput = document.getElementById("feedbackText");
    if (!feedbackInput) return;
    const feedbackText = feedbackInput.value.trim();
    if (!feedbackText) return;

    fetch(FEEDBACK_API, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`
        },
        body: JSON.stringify({ user_id: userId, feedback: feedbackText })
    })
    .then(res => res.json().then(data => ({ status: res.status, body: data })))
    .then(({ status, body }) => {
        if (status === 200 || status === 201) {
            showNotification("Feedback submitted successfully.");
            e.target.reset();
        } else {
            showNotification(body.message || "Failed to submit feedback.", true);
        }
    })
    .catch(() => showNotification("Network error.", true));
}
