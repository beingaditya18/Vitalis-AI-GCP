document.addEventListener('DOMContentLoaded', () => {
    
    // Simple mock navigation
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section-container');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.classList.contains('logout-btn')) return;
            e.preventDefault();
            
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            link.classList.add('active');
            const target = document.querySelector(link.getAttribute('href'));
            if (target) target.classList.add('active');
        });
    });

    // Mock API Loading
    loadDoctors();
    loadServices();
    loadAppointments();

    function loadDoctors() {
        const tbody = document.getElementById('doctorsTableBody');
        if (!tbody) return;
        tbody.innerHTML = `
            <tr>
                <td>Dr. Rakesh Sharma</td>
                <td>General Medicine</td>
                <td>MBBS, MD</td>
                <td>Mon-Fri 9AM-5PM</td>
                <td><span class="status-badge success">Available</span></td>
                <td><button class="btn-sm" onclick="alert('Toggle availability mock')">Toggle</button></td>
            </tr>
            <tr>
                <td>Dr. Sunita Patel</td>
                <td>Gynaecology</td>
                <td>MBBS, MS</td>
                <td>Mon-Wed-Fri 10AM-2PM</td>
                <td><span class="status-badge warning">Unavailable</span></td>
                <td><button class="btn-sm" onclick="alert('Toggle availability mock')">Toggle</button></td>
            </tr>
        `;
    }

    function loadServices() {
        const tbody = document.getElementById('servicesTableBody');
        if (!tbody) return;
        tbody.innerHTML = `
            <tr>
                <td>Blood Test (CBC)</td>
                <td>Diagnostic</td>
                <td>₹ 500</td>
                <td><span class="status-badge success">Active</span></td>
            </tr>
            <tr>
                <td>X-Ray Chest</td>
                <td>Diagnostic</td>
                <td>₹ 800</td>
                <td><span class="status-badge success">Active</span></td>
            </tr>
        `;
    }

    function loadAppointments() {
        const tbody = document.getElementById('appointmentsTableBody');
        if (!tbody) return;
        tbody.innerHTML = `
            <tr>
                <td>APP-1001</td>
                <td>Radha Sharma</td>
                <td>09:00 AM</td>
                <td>OPD - Dr. Rakesh Sharma</td>
                <td><span class="status-badge info">Scheduled</span></td>
                <td>
                    <button class="btn-sm" style="background:#28a745;color:white;border:none;padding:5px 10px;border-radius:4px;cursor:pointer;">Mark Visited</button>
                </td>
            </tr>
        `;
    }

    // Modal Logic
    const docModal = document.getElementById('doctorModal');
    const svcModal = document.getElementById('serviceModal');
    
    const docBtn = document.getElementById('btnAddDoctor');
    const svcBtn = document.getElementById('btnAddService');
    const closes = document.querySelectorAll('.close-btn');

    if (docBtn) docBtn.onclick = () => docModal.classList.add('active');
    if (svcBtn) svcBtn.onclick = () => svcModal.classList.add('active');

    closes.forEach(c => {
        c.onclick = () => {
            if(docModal) docModal.classList.remove('active');
            if(svcModal) svcModal.classList.remove('active');
        }
    });

    const docForm = document.getElementById('doctorForm');
    if(docForm) {
        docForm.onsubmit = (e) => {
            e.preventDefault();
            alert('Mock: Doctor added successfully');
            docModal.classList.remove('active');
        }
    }

    // OTP Logic for Registration
    const btnSendOtp = document.getElementById('btnSendOtp');
    if (btnSendOtp) {
        btnSendOtp.addEventListener('click', async () => {
            const mobile = document.getElementById('pocMobile').value;
            if (!mobile) {
                alert('Please enter a mobile number first.');
                return;
            }
            try {
                const res = await fetch('/api/cis/facility/register/otp/send', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ poc_mobile: mobile })
                });
                const data = await res.json();
                document.getElementById('otpSection').style.display = 'block';
                btnSendOtp.style.display = 'none';
                alert(`MOCK SMS DELIVERED\nOTP is: ${data.mock_otp_for_testing}`);
            } catch (err) {
                console.error(err);
                alert('Error sending OTP');
            }
        });
    }

    // Geolocation mapping mock
    const btnGeo = document.getElementById('btnGetGeo');
    if (btnGeo) {
        btnGeo.addEventListener('click', () => {
            btnGeo.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Locating...';
            setTimeout(() => {
                document.getElementById('lat').value = '18.5204';
                document.getElementById('lng').value = '73.8567';
                btnGeo.innerHTML = '<i class="fas fa-check"></i> Located';
                btnGeo.classList.add('success');
            }, 1000);
        });
    }
});
