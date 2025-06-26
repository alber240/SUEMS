// 🔐 API Endpoints
const API_URL = "http://127.0.0.1:8000/api/events/";
const LOGIN_URL = "http://127.0.0.1:8000/api/login/";
const REGISTER_URL = "http://127.0.0.1:8000/api/register/";

// ✅ When the page loads
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (token) {
        document.getElementById("login-box").style.display = "none";
        fetchEvents();
    }
});

// ✅ Login and save token
function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    fetch(LOGIN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
        if (status === 200) {
            localStorage.setItem("token", body.token);
            localStorage.setItem("user_id", body.user_id);
            localStorage.setItem("username", body.username);
            document.getElementById("login-box").style.display = "none";
            showNotification("Login successful!", false);
            fetchEvents();
        } else {
            showNotification(body.non_field_errors?.[0] || "Login failed", true);
        }
    })
    .catch(() => showNotification("Network error during login", true));
}

// ✅ Fetch and render events
function fetchEvents() {
    fetch(API_URL)
        .then(response => response.json())
        .then(events => renderEvents(events))
        .catch(() => showNotification("Failed to load events", true));
}

function renderEvents(events) {
    const container = document.getElementById("events-container");
    container.innerHTML = "";

    events.forEach(event => {
        const div = document.createElement("div");
        div.className = "event-card";
        div.innerHTML = `
            <h3>${event.title}</h3>
            <p>${event.description}</p>
            <p><strong>Date:</strong> ${event.date}</p>
            <button onclick="registerForEvent(${event.id})">Register</button>
        `;
        container.appendChild(div);
    });
}

// ✅ Register for an event with token
function registerForEvent(eventId) {
    const token = localStorage.getItem("token");
    if (!token) return showNotification("You must be logged in to register.", true);

    fetch(REGISTER_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`
        },
        body: JSON.stringify({ event_id: eventId })
    })
    .then(res => res.json().then(data => ({ status: res.status, body: data })))
    .then(({ status, body }) => {
        if (status === 200) {
            showNotification(body.message, false);
        } else {
            showNotification(body.message || "You are not eligible", true);
        }
    })
    .catch(() => showNotification("Network error. Please try again.", true));
}

// ✅ Notification display
function showNotification(message, isError = false) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.style.color = isError ? "red" : "green";
    notification.style.display = "block";
    setTimeout(() => notification.style.display = "none", 5000);
}
