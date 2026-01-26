// ==================== API CONFIGURATION ====================
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000/api', // Change to your backend URL
    TIMEOUT: 10000,
    DEBUG: true
};

const API_ENDPOINTS = {
    bookings: `${API_CONFIG.BASE_URL}/bookings/`,
    contacts: `${API_CONFIG.BASE_URL}/contacts/`,
    services: `${API_CONFIG.BASE_URL}/services/`,
    settings: `${API_CONFIG.BASE_URL}/settings/current/`,
    health: `${API_CONFIG.BASE_URL}/health/`,
};

// ==================== SALON CONFIGURATION ====================
const SALON_INFO = {
    name: 'Salon',
    phone: '+254712345678',
    whatsapp: '254712345678',
    email: 'info@salon.com',
    address: '123 Beauty Lane, Nairobi, Kenya'
};

// ==================== MOBILE MENU TOGGLE ====================
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });

        // Close menu when a link is clicked
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
            });
        });
    }
    
    // Check backend connectivity
    checkBackendConnection();

    // ==================== LOAD SERVICES ====================
    loadServices();

    // ==================== BOOKING FORM SUBMISSION ====================
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form data with null safety checks
            const fullnameEl = document.getElementById('fullname');
            const phoneEl = document.getElementById('phone');
            const emailEl = document.getElementById('email');
            const serviceEl = document.getElementById('service');
            const dateEl = document.getElementById('date');
            const timeEl = document.getElementById('time');
            const stylistEl = document.getElementById('stylist');
            const notesEl = document.getElementById('notes');
            const sendEmailEl = document.getElementById('sendEmail');

            // Validate all elements exist before accessing
            if (!fullnameEl || !phoneEl || !serviceEl || !dateEl || !timeEl) {
                console.error('Form elements not found');
                return;
            }

            const formData = {
                fullname: fullnameEl.value,
                phone: phoneEl.value,
                email: emailEl ? emailEl.value || '' : '',
                service: serviceEl.value,
                date: dateEl.value,
                time: timeEl.value,
                stylist: stylistEl ? stylistEl.value || null : null,
                notes: notesEl ? notesEl.value : '',
                send_email: sendEmailEl ? sendEmailEl.checked : true
            };

            // Validate form
            if (!formData.fullname || !formData.phone || !formData.service || !formData.date || !formData.time) {
                alert('Please fill in all required fields');
                return;
            }

            // Validate phone number (basic check)
            if (!/^\+?[0-9]{7,}$/.test(formData.phone.replace(/\s/g, ''))) {
                alert('Please enter a valid phone number');
                return;
            }

            // Validate date is not in the past
            const selectedDate = new Date(formData.date);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            if (selectedDate < today) {
                alert('Please select a future date');
                return;
            }

                    // Send booking data to backend
            submitBooking(formData);
        });
    }

    // ==================== CONTACT FORM SUBMISSION ====================
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const nameEl = document.getElementById('name');
            const emailEl = document.getElementById('contact-email');
            const subjectEl = document.getElementById('subject');
            const messageEl = document.getElementById('message');

            // Validate elements exist
            if (!nameEl || !emailEl || !subjectEl || !messageEl) {
                console.error('Contact form elements not found');
                return;
            }

            const formData = {
                name: nameEl.value,
                email: emailEl.value,
                subject: subjectEl.value,
                message: messageEl.value
            };

            // Send contact message
            submitContact(formData);
        });
    }

    // ==================== SET MINIMUM DATE FOR BOOKING ====================
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
});

// ==================== SUBMIT BOOKING ====================
function submitBooking(data) {
    // Show loading state
    const submitBtn = document.querySelector('.submit-button');
    if (submitBtn) {
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Processing...';
        submitBtn.disabled = true;
    }

    // Send to backend
    fetch(API_ENDPOINTS.bookings, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Booking failed');
        }
        return response.json();
    })
    .then(result => {
        console.log('Booking successful:', result);
        
        // Hide form and show success message
        const bookingForm = document.getElementById('bookingForm');
        const successMessage = document.getElementById('successMessage');
        
        if (bookingForm) {
            bookingForm.style.display = 'none';
        }
        
        if (successMessage) {
            successMessage.style.display = 'block';
            // Scroll to success message
            successMessage.scrollIntoView({ behavior: 'smooth' });
        }

        // Send WhatsApp notification
        sendWhatsAppNotification(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Booking failed. Please try again or contact us directly.');
        
        const submitBtn = document.querySelector('.submit-button');
        if (submitBtn) {
            submitBtn.textContent = 'Book Now';
            submitBtn.disabled = false;
        }
    });
}

// ==================== SUBMIT CONTACT ====================
function submitContact(data) {
    const submitBtn = document.querySelector('.submit-button');
    if (!submitBtn) return;
    
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    fetch(API_ENDPOINTS.contacts, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Message failed');
        }
        return response.json();
    })
    .then(result => {
        console.log('Message sent:', result);
        alert('Thank you! We received your message. We\'ll be in touch soon.');
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            contactForm.reset();
        }
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send message. Please try again.');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

// ==================== GET CSRF TOKEN ====================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==================== SEND WHATSAPP NOTIFICATION ====================
function sendWhatsAppNotification(bookingData) {
    // This sends a booking confirmation message via WhatsApp
    // WhatsApp click-to-chat link (to the salon)
    
    const message = encodeURIComponent(
        `Hello! I've booked an appointment:\n\n` +
        `Name: ${bookingData.fullname}\n` +
        `Service: ${bookingData.service}\n` +
        `Date: ${bookingData.date}\n` +
        `Time: ${bookingData.time}\n` +
        `Phone: ${bookingData.phone}`
    );

    // Send to salon WhatsApp
    window.open(`https://wa.me/${SALON_INFO.whatsapp}?text=${message}`, '_blank');
}

// ==================== CHECK BACKEND CONNECTION ====================
function checkBackendConnection() {
    fetch(API_ENDPOINTS.health, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (API_CONFIG.DEBUG) {
            console.log('✅ Backend connected:', data);
        }
    })
    .catch(error => {
        console.warn('⚠️ Backend not available. Running in offline mode.');
        console.warn('API Base URL:', API_CONFIG.BASE_URL);
    });
}
// ==================== LOAD SERVICES ====================
function loadServices() {
    const serviceSelect = document.getElementById('service');
    if (!serviceSelect) return;

    // Fetch all services by requesting with a high limit
    fetch(API_ENDPOINTS.services + '?limit=100', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        // Handle paginated response
        let allServices = data.results || (Array.isArray(data) ? data : []);
        
        // If there are more pages, fetch them recursively
        if (data.next) {
            const fetchNextPage = (nextUrl) => {
                return fetch(nextUrl)
                    .then(r => r.json())
                    .then(pageData => {
                        allServices = allServices.concat(pageData.results || []);
                        if (pageData.next) {
                            return fetchNextPage(pageData.next);
                        }
                        return allServices;
                    });
            };
            return fetchNextPage(data.next);
        }
        return allServices;
    })
    .then(services => {
        // Group services by category
        const grouped = {};
        services.forEach(service => {
            if (!grouped[service.category]) {
                grouped[service.category] = [];
            }
            grouped[service.category].push(service);
        });

        // Clear existing options except the first one
        serviceSelect.innerHTML = '<option value="">-- Choose Service --</option>';

        // Add grouped options
        Object.keys(grouped).sort().forEach(category => {
            const optgroup = document.createElement('optgroup');
            optgroup.label = category.charAt(0).toUpperCase() + category.slice(1) + ' Services';
            
            grouped[category].forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = `${service.name} – KES ${service.price}`;
                optgroup.appendChild(option);
            });
            
            serviceSelect.appendChild(optgroup);
        });
    })
    .catch(error => {
        console.error('Error loading services:', error);
        serviceSelect.innerHTML = '<option value="">Error loading services</option>';
    });
}

// ==================== SMOOTH SCROLL ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const element = document.querySelector(href);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// ==================== ACTIVE NAVIGATION LINK ====================
window.addEventListener('load', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// ==================== FORMAT PHONE NUMBER ====================
function formatPhoneNumber(input) {
    const phoneInput = document.getElementById(input);
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Remove non-digits
            let value = this.value.replace(/\D/g, '');
            
            // Format as you type (basic Kenyan format)
            if (value.length > 0) {
                if (value.length <= 3) {
                    value = value;
                } else if (value.length <= 6) {
                    value = value.slice(0, 3) + ' ' + value.slice(3);
                } else if (value.length <= 9) {
                    value = value.slice(0, 3) + ' ' + value.slice(3, 6) + ' ' + value.slice(6);
                } else {
                    value = '+' + value.slice(0, 3) + ' ' + value.slice(3, 6) + ' ' + value.slice(6, 9) + ' ' + value.slice(9, 12);
                }
            }
            this.value = value;
        });
    }
}

formatPhoneNumber('phone');

// ==================== TIME PICKER VALIDATION ====================
function validateTimeSlot() {
    const timeInput = document.getElementById('time');
    if (timeInput) {
        timeInput.addEventListener('change', function() {
            const selectedTime = this.value;
            const [hours] = selectedTime.split(':');
            const hour = parseInt(hours);

            // Salon hours: 9 AM - 8 PM (09:00 - 20:00)
            if (hour < 9 || hour >= 20) {
                alert('Please select a time between 9:00 AM and 8:00 PM');
                this.value = '';
            }
        });
    }
}

validateTimeSlot();

// ==================== FORM AUTOSAVE ====================
function autoSaveForm() {
    const form = document.getElementById('bookingForm');
    if (form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        const STORAGE_KEY = 'bookingFormData';

        // Load saved data
        const savedData = localStorage.getItem(STORAGE_KEY);
        if (savedData) {
            const data = JSON.parse(savedData);
            for (const [key, value] of Object.entries(data)) {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = value;
                }
            }
        }

        // Save data on input
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
            });
        });
    }
}

// Call autosave on page load
if (document.getElementById('bookingForm')) {
    autoSaveForm();
}

// ==================== ANALYTICS TRACKING ====================
function trackEvent(eventName, eventData = {}) {
    // Simple analytics tracking - you can integrate with Google Analytics
    if (API_CONFIG.DEBUG) {
        console.log(`Event: ${eventName}`, eventData);
    }
}
