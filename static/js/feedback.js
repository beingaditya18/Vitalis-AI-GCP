document.addEventListener('DOMContentLoaded', () => {
    loadFeedbackQueue();

    // Star Rating Logic
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.getElementById('ratingValue');

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const val = parseInt(star.getAttribute('data-val'));
            ratingInput.value = val;
            
            stars.forEach(s => {
                if (parseInt(s.getAttribute('data-val')) <= val) {
                    s.classList.remove('far');
                    s.classList.add('fas');
                    s.style.color = '#ffc107';
                } else {
                    s.classList.remove('fas');
                    s.classList.add('far');
                    s.style.color = '#ccc';
                }
            });
        });
    });

    // Toggle Reschedule Date based on Visit Status
    const visitStatus = document.getElementById('visitStatus');
    const rescheduleGroup = document.getElementById('rescheduleGroup');

    if (visitStatus && rescheduleGroup) {
        visitStatus.addEventListener('change', () => {
            if (visitStatus.value === 'not_visited') {
                rescheduleGroup.style.display = 'block';
            } else {
                rescheduleGroup.style.display = 'none';
            }
        });
    }

    // Form Submission
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = feedbackForm.querySelector('button');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            
            const payload = {
                feedback_id: document.getElementById('currentFeedbackId').value,
                rating: document.getElementById('ratingValue').value,
                comments: document.getElementById('comments').value,
                visit_status: document.getElementById('visitStatus').value,
                new_date: document.getElementById('rescheduleDate').value
            };

            try {
                if (payload.visit_status === 'not_visited' && payload.new_date) {
                    // Hit reschedule endpoint
                    await fetch(`/api/admin/feedback/${payload.feedback_id}/reschedule`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({new_date: payload.new_date})
                    });
                    alert('Feedback recorded.\n\nMOCK: Appointment Rescheduled and SMS Notification Sent to Patient & Facility.');
                } else {
                    alert('Feedback recorded successfully.');
                }
                
                // Reset form and reload list
                feedbackForm.reset();
                stars.forEach(s => { s.classList.remove('fas'); s.classList.add('far'); s.style.color = '#ccc'; });
                ratingInput.value = "0";
                rescheduleGroup.style.display = 'none';
                document.getElementById('feedbackPanel').style.display = 'none';
                
                loadFeedbackQueue();

            } catch (err) {
                console.error(err);
                alert('Error submitting feedback');
            } finally {
                btn.innerHTML = 'Submit Feedback & Action';
            }
        });
    }
});

async function loadFeedbackQueue() {
    const tbody = document.getElementById('feedbackTableBody');
    if (!tbody) return;
    
    try {
        const res = await fetch('/api/admin/feedback');
        const data = await res.json();
        
        tbody.innerHTML = '';
        data.feedback.forEach(f => {
            const vStatus = f.visit_status === 'visited' ? 'success' : 'danger';
            const vText = f.visit_status === 'visited' ? 'Visited' : 'Not Visited';
            const cStatus = f.callback_status === 'pending' ? 'warning' : 'success';
            
            tbody.innerHTML += `
                <tr>
                    <td>#${f.id}</td>
                    <td>${f.patient_name || 'Patient'}</td>
                    <td><span class="status-badge ${vStatus}">${vText}</span></td>
                    <td><span class="status-badge ${cStatus}">${f.callback_status.toUpperCase()}</span></td>
                    <td>
                        <button onclick="initiateCall('${f.phone || '9000000000'}')" class="btn-sm" style="background:#28a745;color:white;border:none;padding:5px 10px;border-radius:4px;cursor:pointer;margin-right:5px;">
                            <i class="fas fa-phone"></i> Call
                        </button>
                        <button onclick="openFeedbackForm(${f.id}, '${f.patient_name || 'Patient'}')" class="btn-sm" style="background:#17a2b8;color:white;border:none;padding:5px 10px;border-radius:4px;cursor:pointer;">
                            Fill Form
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}

function initiateCall(phone) {
    alert(`MOCK IVRS: Initiating one-click call to ${phone}...`);
}

function openFeedbackForm(id, name) {
    document.getElementById('feedbackPanel').style.display = 'block';
    document.getElementById('currentFeedbackId').value = id;
    document.getElementById('feedbackPatientName').innerText = name;
    document.getElementById('feedbackPanel').scrollIntoView({behavior: 'smooth'});
}
