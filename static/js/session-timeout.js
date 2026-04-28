// Session Timeout Management
class SessionManager {
    constructor(timeoutMinutes = 30) {
        this.timeoutMs = timeoutMinutes * 60 * 1000;
        this.warningMs = 5 * 60 * 1000; // Warn 5 mins before
        this.lastActivity = Date.now();
        this.init();
    }

    init() {
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
        events.forEach(e => document.addEventListener(e, () => this.resetTimer(), { passive: true }));
        
        setInterval(() => this.checkSession(), 60000); // Check every minute
    }

    resetTimer() {
        this.lastActivity = Date.now();
    }

    checkSession() {
        const now = Date.now();
        const timeIdle = now - this.lastActivity;

        if (timeIdle >= this.timeoutMs) {
            this.logout();
        } else if (timeIdle >= (this.timeoutMs - this.warningMs)) {
            console.warn("Session expiring soon.");
        }
    }

    logout() {
        window.location.href = '/api/auth/logout';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.sessionManager = new SessionManager();
});
