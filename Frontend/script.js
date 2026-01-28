// ==================== API CONFIGURATION ====================
const BASE_URL = "https://smsalon-ehqso.ondigitalocean.app/api";

const API_CONFIG = {
    BASE_URL,
    DEBUG: false
};

const API_ENDPOINTS = {
    bookings: `${BASE_URL}/bookings/`,
    contacts: `${BASE_URL}/contacts/`,
    services: `${BASE_URL}/services/`,
    settings: `${BASE_URL}/settings/current/`,
    health: `${BASE_URL}/health/`,
    authLogin: `${BASE_URL}/auth/login/`
};

// ==================== SALON CONFIGURATION ====================
const SALON_INFO = {
    name: "SM Salon Barbershop",
    phone: "+254741464762",
    whatsapp: "+254741464762",
    email: "info@sm-salon.com",
    address: "Homeland, Nairobi, Kenya"
};

// ==================== GLOBAL FLAGS ====================
window.IS_OFFLINE = false;

// ==================== DOM CONTENT LOADED ====================
document.addEventListener("DOMContentLoaded", () => {
    setupMobileMenu();
    checkBackendConnection();
    loadServices();
    
    // setupBookingForm();
    // setupContactForm();
    setMinDate();
    formatPhoneNumber("phone");
    validateTimeSlot();
    autoSaveForm();
    setupSmoothScroll();
    highlightActiveNav();
});

// ==================== BACKEND HEALTH CHECK ====================
async function checkBackendConnection() {
    try {
        const res = await fetch(API_ENDPOINTS.health);
        if (!res.ok) throw new Error(res.status);
        const data = await res.json();
        console.log("✅ Backend connected:", data);
    } catch {
        console.warn("⚠️ Backend not reachable. Offline mode enabled.");
        window.IS_OFFLINE = true;
    }
}

// ==================== LOAD SERVICES ====================
async function loadServices() {
    const serviceSelect = document.getElementById("service");
    if (!serviceSelect) return;

    if (window.IS_OFFLINE) {
        displayServices(getOfflineServices());
        return;
    }

    try {
        const res = await fetch(API_ENDPOINTS.services);
        if (!res.ok) throw new Error();
        const data = await res.json();
        displayServices(data.results || data);
    } catch {
        displayServices(getOfflineServices());
    }
}

// ==================== BOOKING SUBMIT ====================
async function submitBooking(data) {
    if (window.IS_OFFLINE) {
        alert("Backend unavailable. Booking saved locally.");
        return;
    }

    try {
        const res = await fetch(API_ENDPOINTS.bookings, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error();
        document.getElementById("bookingForm").reset();
        alert("✅ Booking successful!");
    } catch {
        alert("❌ Booking failed. Try again.");
    }
}

// ==================== CONTACT SUBMIT ====================
async function submitContact(data) {
    try {
        const res = await fetch(API_ENDPOINTS.contacts, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error();
        alert("✅ Message sent!");
    } catch {
        alert("❌ Failed to send message.");
    }
}
// ==================== UI HELPERS ====================
function setupMobileMenu() {
    const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");
    if (!hamburger || !navLinks) return;

    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });

    navLinks.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("active");
        });
    });
}

function setMinDate() {
    const dateInput = document.getElementById("date");
    if (!dateInput) return;
    dateInput.min = new Date().toISOString().split("T")[0];
}

function formatPhoneNumber(id) {
    const input = document.getElementById(id);
    if (!input) return;

    input.addEventListener("input", () => {
        input.value = input.value.replace(/[^\d+]/g, "");
    });
}

function validateTimeSlot() {
    const time = document.getElementById("time");
    if (!time) return;

    time.addEventListener("change", () => {
        const hour = parseInt(time.value.split(":")[0]);
        if (hour < 9 || hour >= 20) {
            alert("Please choose a time between 9am and 8pm");
            time.value = "";
        }
    });
}

function autoSaveForm() {}
function setupSmoothScroll() {}
function highlightActiveNav() {}
