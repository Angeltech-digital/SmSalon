// ==================== API CONFIGURATION ====================
// Default to local backend
let BASE_URL = 'http://127.0.0.1:8000/api';
const PROD_API_URL = 'https://your-production-domain.com/api';

// Override if user explicitly wants production
if (localStorage.getItem('apiEnvironment') === 'production') {
    BASE_URL = PROD_API_URL;
}

// Save preference for future visits
localStorage.setItem('useLocalApi', BASE_URL === 'http://127.0.0.1:8000/api' ? 'true' : 'false');

// Unified API_CONFIG object for all scripts
const API_CONFIG = {
    BASE_URL,
    DEBUG: true
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
    name: 'SM Salon Barbershop',
    phone: '+254 741 464 762',
    whatsapp: '+254 741 464 762',
    email: 'info@sm-salon.com',
    address: 'Homeland, Nairobi, Kenya'
};

// ==================== GLOBAL FLAGS ====================
window.IS_OFFLINE = false;

// ==================== DOM CONTENT LOADED ====================
document.addEventListener('DOMContentLoaded', () => {
    setupMobileMenu();
    checkBackendConnection();
    loadServices();
    setupBookingForm();
    setupContactForm();
    setMinDate();
    formatPhoneNumber('phone');
    validateTimeSlot();
    autoSaveForm();
    setupSmoothScroll();
    highlightActiveNav();
});

// ==================== MOBILE MENU ====================
function setupMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));
    navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => navLinks.classList.remove('active')));
}

// ==================== BACKEND HEALTH CHECK ====================
async function checkBackendConnection() {
    try {
        const res = await fetch(API_ENDPOINTS.health, { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        if (!res.ok) throw new Error(`Status ${res.status}`);
        const data = await res.json();
        if (API_CONFIG.DEBUG) console.log('✅ Backend connected:', data);
    } catch (err) {
        console.warn('⚠️ Backend not available. Running in offline mode.');
        console.warn('API Base URL:', BASE_URL);
        window.IS_OFFLINE = true;
    }
}

// ==================== LOAD SERVICES ====================
async function loadServices() {
    const serviceSelect = document.getElementById('service');
    if (!serviceSelect) return;

    if (window.IS_OFFLINE) {
        displayServices(getOfflineServices());
        return;
    }

    try {
        const res = await fetch(`${API_ENDPOINTS.services}?limit=100`, { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        if (!res.ok) throw new Error(`Status ${res.status}`);
        const data = await res.json();
        const allServices = data.results || (Array.isArray(data) ? data : []);
        displayServices(allServices);
    } catch (err) {
        console.warn('⚠️ Could not load services, using offline fallback.', err);
        displayServices(getOfflineServices());
    }
}

function getOfflineServices() {
    return [
        { id: 1, name: 'Haircut & Styling', category: 'hair', price: 500 },
        { id: 2, name: 'Hair Coloring', category: 'hair', price: 2000 },
        { id: 3, name: 'Manicure', category: 'nails', price: 300 },
        { id: 4, name: 'Pedicure', category: 'nails', price: 400 },
        { id: 5, name: 'Full Makeup', category: 'makeup', price: 1500 },
        { id: 6, name: 'Braiding', category: 'braiding', price: 1000 },
        { id: 7, name: 'Weave Installation', category: 'braiding', price: 2500 },
        { id: 8, name: 'Facial Treatment', category: 'hair', price: 800 },
    ];
}

function displayServices(services) {
    const serviceSelect = document.getElementById('service');
    if (!serviceSelect) return;

    const grouped = {};
    services.forEach(service => {
        const category = service.category || 'general';
        if (!grouped[category]) grouped[category] = [];
        grouped[category].push(service);
    });

    serviceSelect.innerHTML = '<option value="">-- Choose Service --</option>';
    Object.keys(grouped).sort().forEach(cat => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = cat.charAt(0).toUpperCase() + cat.slice(1) + ' Services';
        grouped[cat].forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = `${service.name}${service.price ? ` – KES ${service.price}` : ''}`;
            optgroup.appendChild(option);
        });
        serviceSelect.appendChild(optgroup);
    });
}

// ==================== BOOKING FORM ====================
function setupBookingForm() {
    const form = document.getElementById('bookingForm');
    if (!form) return;

    form.addEventListener('submit', e => {
        e.preventDefault();
        const fullname = document.getElementById('fullname')?.value || '';
        const phone = document.getElementById('phone')?.value.replace(/\D/g, '') || '';
        const email = document.getElementById('email')?.value || '';
        const service = parseInt(document.getElementById('service')?.value) || null;
        const date = document.getElementById('date')?.value || '';
        const time = document.getElementById('time')?.value + ':00' || '';
        const stylist = parseInt(document.getElementById('stylist')?.value) || null;
        const notes = document.getElementById('notes')?.value || '';
        const send_email = document.getElementById('sendEmail')?.checked ?? true;

        if (!fullname || !phone || !service || !date || !time) {
            alert('Please fill in all required fields');
            return;
        }

        if (!/^\+?[0-9]{7,}$/.test(phone.replace(/\s/g, ''))) {
            alert('Please enter a valid phone number');
            return;
        }

        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0,0,0,0);
        if (selectedDate < today) {
            alert('Please select a future date');
            return;
        }

        submitBooking({ fullname, phone, email, service, date, time, stylist, notes, send_email });
    });
}

// ==================== SUBMIT BOOKING ====================
async function submitBooking(data) {
    const submitBtn = document.querySelector('.submit-button');
    if (submitBtn) { submitBtn.textContent = 'Processing...'; submitBtn.disabled = true; }

    if (window.IS_OFFLINE) {
        alert('Booking stored offline. Backend is not connected.');
        if (submitBtn) { submitBtn.textContent = 'Book Now'; submitBtn.disabled = false; }
        return;
    }

    try {
        const res = await fetch(API_ENDPOINTS.bookings, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(await res.text());
        await res.json();
        document.getElementById('bookingForm').style.display = 'none';
        document.getElementById('successMessage').style.display = 'block';
        sendWhatsAppNotification(data);
    } catch (err) {
        console.error(err);
        alert('Booking failed. Please try again.');
        if (submitBtn) { submitBtn.textContent = 'Book Now'; submitBtn.disabled = false; }
    }
}

// ==================== CONTACT FORM ====================
function setupContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', e => {
        e.preventDefault();
        const data = {
            name: document.getElementById('name')?.value || '',
            email: document.getElementById('contact-email')?.value || '',
            subject: document.getElementById('subject')?.value || '',
            message: document.getElementById('message')?.value || ''
        };
        submitContact(data);
    });
}

async function submitContact(data) {
    const submitBtn = document.querySelector('.submit-button');
    if (!submitBtn) return;
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    if (window.IS_OFFLINE) {
        alert('Message stored offline. Backend is not connected.');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        return;
    }

    try {
        const res = await fetch(API_ENDPOINTS.contacts, {
            method:'POST',
            headers:{'Content-Type':'application/json','X-CSRFToken': getCookie('csrftoken')},
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Message failed');
        await res.json();
        alert('Message sent!');
        document.getElementById('contactForm').reset();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    } catch (err) {
        alert('Failed to send message.');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// ==================== HELPER FUNCTIONS ====================
function getCookie(name) {
    const cookies = document.cookie.split(';').map(c => c.trim());
    for (let cookie of cookies) {
        if (cookie.startsWith(name + '=')) return decodeURIComponent(cookie.split('=')[1]);
    }
    return null;
}

function sendWhatsAppNotification(data) {
    const message = encodeURIComponent(
        `Hello! I've booked an appointment:\nName: ${data.fullname}\nService: ${data.service}\nDate: ${data.date}\nTime: ${data.time}\nPhone: ${data.phone}`
    );
    window.open(`https://wa.me/${SALON_INFO.whatsapp}?text=${message}`, '_blank');
}

function setMinDate() {
    const dateInput = document.getElementById('date');
    if (!dateInput) return;
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
}

function formatPhoneNumber(inputId) {
    const phoneInput = document.getElementById(inputId);
    if (!phoneInput) return;
    phoneInput.addEventListener('input', function() {
        let val = this.value.replace(/\D/g,'');
        if (val.length>0){
            if (val.length<=3) val=val;
            else if(val.length<=6) val=val.slice(0,3)+' '+val.slice(3);
            else if(val.length<=9) val=val.slice(0,3)+' '+val.slice(3,6)+' '+val.slice(6);
            else val='+'+val.slice(0,3)+' '+val.slice(3,6)+' '+val.slice(6,9)+' '+val.slice(9,12);
        }
        this.value=val;
    });
}

function validateTimeSlot() {
    const timeInput = document.getElementById('time');
    if (!timeInput) return;
    timeInput.addEventListener('change', function() {
        const hour = parseInt(this.value.split(':')[0]);
        if(hour<9||hour>=20){ alert('Select time 9:00-20:00'); this.value=''; }
    });
}

function autoSaveForm() {
    const form = document.getElementById('bookingForm');
    if(!form) return;
    const inputs = form.querySelectorAll('input, select, textarea');
    const STORAGE_KEY='bookingFormData';
    const saved = localStorage.getItem(STORAGE_KEY);
    if(saved) Object.entries(JSON.parse(saved)).forEach(([k,v])=>{ const f=form.querySelector(`[name="${k}"]`); if(f) f.value=v; });
    inputs.forEach(input => input.addEventListener('input',()=>{ const data=Object.fromEntries(new FormData(form)); localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }));
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',function(e){
        const href=this.getAttribute('href'); 
        if(href!=='#'){e.preventDefault(); const el=document.querySelector(href); if(el) el.scrollIntoView({behavior:'smooth'});}
    }));
}

function highlightActiveNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link=>{
        const href=link.getAttribute('href');
        if(href===currentPage || (currentPage===''&&href==='index.html')) link.classList.add('active');
        else link.classList.remove('active');
    });
}
