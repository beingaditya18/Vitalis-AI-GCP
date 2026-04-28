// Core API Wrapper
class DoctorDashboardAPI {
    async get(endpoint) {
        try {
            const res = await fetch(`/api/doctor${endpoint}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return { success: true, data: await res.json() };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async post(endpoint, payload) {
        try {
            const res = await fetch(`/api/doctor${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return { success: true, data: await res.json() };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Error & Toast Management
class ErrorHandler {
    constructor() {
        this.container = document.getElementById('toast-container');
    }

    show(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        this.container.appendChild(toast);
        setTimeout(() => toast.remove(), 4500);
    }

    showSuccess(msg) { this.show(msg, 'success'); }
    showError(msg) { this.show(msg, 'error'); }
    showWarning(msg) { this.show(msg, 'warning'); }
    handleApiError(error, context) {
        console.error(context, error);
        this.showError(`${context}: ${error}`);
    }
}

// Notifications
class NotificationManager {
    constructor(api) {
        this.api = api;
        this.badge = document.getElementById('notification-badge');
        this.dropdown = document.getElementById('notification-dropdown');
        this.list = document.getElementById('notification-list');
        
        document.getElementById('notification-bell').addEventListener('click', () => {
            this.dropdown.style.display = this.dropdown.style.display === 'none' ? 'block' : 'none';
        });
    }

    async loadNotifications() {
        // Mock notification logic
        const count = Math.floor(Math.random() * 3);
        if (count > 0) {
            this.badge.style.display = 'flex';
            this.badge.textContent = count;
            this.list.innerHTML = `<p style="padding:10px;">You have ${count} new critical alerts.</p>`;
        } else {
            this.badge.style.display = 'none';
        }
    }
}

// Polling
class PollingManager {
    constructor(callback, interval) {
        this.callback = callback;
        this.interval = interval;
        this.timer = null;
    }
    start() {
        this.callback();
        this.timer = setInterval(this.callback, this.interval);
    }
    stop() {
        clearInterval(this.timer);
    }
}

// Initial Data Loaders
async function loadDashboardStats() {
    const res = await window.api.get('/stats');
    if (res.success) {
        document.getElementById('new-cases-value').textContent = res.data.new_cases;
        document.getElementById('total-assessments-value').textContent = res.data.total_assessments;
        document.getElementById('high-risk-alerts-value').textContent = res.data.high_risk_alerts;
        document.getElementById('critical-risk-value').textContent = res.data.critical_risk;
    }
}

async function loadPendingSummaries() {
    const container = document.getElementById('pending-summaries-list');
    const res = await window.api.get('/patients/queue/today');
    if (res.success && res.data.queue) {
        if(res.data.queue.length === 0) {
            container.innerHTML = '<p class="empty-state">No pending summaries</p>';
            return;
        }
        container.innerHTML = res.data.queue.map(q => `
            <div class="patient-card" style="display:flex; justify-content:space-between;">
                <div><strong>Case #${q.id}</strong> - ${q.severity}</div>
                <button class="btn btn-primary" onclick="alert('Reviewing ${q.id}')">Review</button>
            </div>
        `).join('');
    }
}

async function loadActivityFeed() {
    const container = document.getElementById('activity-feed-list');
    container.innerHTML = `
        <div style="margin-bottom:10px;">
            <i class="fas fa-check text-success"></i> Review completed for Case #102
        </div>
        <div style="margin-bottom:10px;">
            <i class="fas fa-exclamation text-danger"></i> High risk alert: Patient ID 45
        </div>
    `;
}

async function loadPatientList() {
    const container = document.getElementById('patient-list');
    container.innerHTML = `
        <div class="patient-card"><strong>John Doe</strong> - ID: 1001 <br> <small>Status: Stable</small></div>
        <div class="patient-card high-risk"><strong>Jane Smith</strong> - ID: 1002 <br> <small>Status: Critical</small></div>
    `;
}

function initializePatientFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            window.errorHandler.showSuccess(`Filtered by ${e.target.dataset.filter}`);
        });
    });
}
