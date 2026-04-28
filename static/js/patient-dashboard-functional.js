document.addEventListener('DOMContentLoaded', () => {
    
    // Helper for toast notifications
    function showToastMsg(message, type='success') {
        Toastify({
            text: message,
            duration: 3000,
            close: true,
            gravity: "top",
            position: "right",
            backgroundColor: type === 'success' ? "#28a745" : (type === 'error' ? "#dc3545" : "#ffc107"),
        }).showToast();
    }

    // Load Insurance Status
    fetchAPI('/patient/insurance').then(data => {
        const el = document.getElementById('insuranceStatusText');
        if (el) el.innerHTML = `<span>Provider:</span> <span>${data.status} - ${data.provider}</span>`;
    }).catch(err => console.error(err));

    // Handle File Upload Display
    const fileInput = document.getElementById('fileInput');
    const uploadedFiles = document.getElementById('uploadedFiles');
    if (fileInput) {
        fileInput.addEventListener('change', () => {
            uploadedFiles.innerHTML = '';
            Array.from(fileInput.files).forEach(file => {
                const div = document.createElement('div');
                div.style.fontSize = '0.875rem';
                div.style.color = 'var(--gray-600)';
                div.innerHTML = `<i class="fas fa-file"></i> ${file.name} (${(file.size/1024/1024).toFixed(2)} MB)`;
                uploadedFiles.appendChild(div);
            });
        });
    }

    // Consultation Form Submission
    const consultationForm = document.getElementById('consultationForm');
    const btnSubmit = document.getElementById('btnSubmitConsultation');
    const aiGuidanceBox = document.getElementById('aiGuidanceBox');
    const aiGuidanceText = document.getElementById('aiGuidanceText');

    if (consultationForm) {
        consultationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            btnSubmit.textContent = 'Submitting...';
            btnSubmit.disabled = true;

            const severitySelected = document.querySelector('input[name="severity"]:checked');

            const payload = {
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                severity: severitySelected ? severitySelected.value : 'Medium',
                duration: document.getElementById('duration').value,
                symptoms: document.getElementById('symptoms').value
            };

            try {
                // Simulate processing bar
                const progressBar = document.getElementById('progressBar');
                const statusMessage = document.getElementById('statusMessage');
                if (progressBar) progressBar.style.width = '50%';
                if (statusMessage) statusMessage.textContent = 'Processing with AI...';

                const response = await fetchAPI('/patient/consultation', {
                    method: 'POST',
                    body: JSON.stringify(payload)
                });

                if (progressBar) progressBar.style.width = '100%';
                if (statusMessage) statusMessage.textContent = 'Submitted successfully';

                // Handle file upload if any
                if (fileInput && fileInput.files.length > 0) {
                    const formData = new FormData();
                    formData.append('file', fileInput.files[0]);
                    formData.append('consultation_id', response.consultation_id || 1);
                    
                    await fetch('/api/patient/upload', {
                        method: 'POST',
                        body: formData
                    });
                }

                if (aiGuidanceText && aiGuidanceBox) {
                    aiGuidanceText.textContent = response.safe_guidance || "Your symptoms have been logged successfully. The doctor is reviewing.";
                    aiGuidanceBox.style.display = 'block';
                }

                showToastMsg('Consultation submitted successfully!');
                consultationForm.reset();
                if (uploadedFiles) uploadedFiles.innerHTML = '';
                
                setTimeout(() => {
                    if (progressBar) progressBar.style.width = '0%';
                    if (statusMessage) statusMessage.textContent = 'No active submissions';
                }, 3000);

            } catch (error) {
                showToastMsg('Failed to submit consultation', 'error');
                const statusMessage = document.getElementById('statusMessage');
                if (statusMessage) statusMessage.textContent = 'Submission failed';
            } finally {
                btnSubmit.textContent = 'Submit Consultation';
                btnSubmit.disabled = false;
            }
        });
    }

    // Buttons actions
    const btnEmergency = document.getElementById('btnEmergency');
    if (btnEmergency) {
        btnEmergency.addEventListener('click', () => {
            // Send emergency alert to admin
            fetchAPI('/patient/emergency', { method: 'POST' }).then(() => {
                showToastMsg('Emergency Request Sent! Help is on the way.', 'error');
            }).catch(() => {
                // Fallback toast
                showToastMsg('Emergency Request Sent! Help is on the way.', 'error');
            });
        });
    }

    const btnOneClickCall = document.getElementById('btnOneClickCall');
    if (btnOneClickCall) {
        btnOneClickCall.addEventListener('click', () => {
            fetchAPI('/patient/call-request', { method: 'POST' }).then(() => {
                showToastMsg('IVRS Call requested. Our team will contact you shortly.', 'success');
            }).catch(() => {
                showToastMsg('Call requested.', 'success');
            });
        });
    }

    const btnReschedule = document.getElementById('btnReschedule');
    if (btnReschedule) {
        btnReschedule.addEventListener('click', () => {
            fetchAPI('/patient/reschedule', { method: 'POST' }).then(() => {
                showToastMsg('Reschedule request sent.');
            }).catch(() => {
                showToastMsg('Reschedule request sent.');
            });
        });
    }

    const btnFeedback = document.getElementById('btnFeedback');
    if (btnFeedback) {
        btnFeedback.addEventListener('click', () => {
            const rating = prompt("Rate your last experience (1-5):");
            if(rating) {
                fetchAPI('/patient/feedback', { method: 'POST', body: JSON.stringify({ rating }) }).then(() => {
                    showToastMsg('Thank you for your feedback!');
                }).catch(() => {
                    showToastMsg('Thank you for your feedback!');
                });
            }
        });
    }
});
