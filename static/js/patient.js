document.addEventListener('DOMContentLoaded', () => {
    
    // Load Insurance Status
    fetchAPI('/patient/insurance').then(data => {
        document.getElementById('insuranceStatusText').textContent = `${data.status} - ${data.provider}`;
    }).catch(err => console.error(err));

    // Consultation Form Submission
    const consultationForm = document.getElementById('consultationForm');
    const btnSubmit = document.getElementById('btnSubmitConsultation');
    const aiResponseBox = document.getElementById('aiResponseBox');
    const aiGuidanceText = document.getElementById('aiGuidanceText');

    consultationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        btnSubmit.textContent = 'Submitting...';
        btnSubmit.disabled = true;

        const payload = {
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            severity: document.getElementById('severity').value,
            duration: document.getElementById('duration').value,
            symptoms: document.getElementById('symptoms').value
        };

        try {
            const response = await fetchAPI('/patient/consultation', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            // Handle file upload if any
            const fileInput = document.getElementById('fileUpload');
            if (fileInput.files.length > 0) {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('consultation_id', response.consultation_id);
                
                await fetch('/api/patient/upload', {
                    method: 'POST',
                    body: formData
                });
            }

            aiGuidanceText.textContent = response.safe_guidance || "Your symptoms have been logged successfully. The doctor is reviewing.";
            aiResponseBox.style.display = 'block';
            showToast('Consultation submitted successfully!');
            consultationForm.reset();

        } catch (error) {
            showToast('Failed to submit consultation', 'error');
        } finally {
            btnSubmit.textContent = 'Submit to Doctor';
            btnSubmit.disabled = false;
        }
    });

    // Buttons actions
    document.getElementById('btnEmergency').addEventListener('click', () => {
        showToast('Emergency Request Sent! Help is on the way.', 'error');
    });

    document.getElementById('btnOneClickCall').addEventListener('click', () => {
        fetchAPI('/patient/call-request', { method: 'POST' }).then(() => {
            showToast('Call requested. Our team will contact you shortly.');
        });
    });

    document.getElementById('btnReschedule').addEventListener('click', () => {
        fetchAPI('/patient/reschedule', { method: 'POST' }).then(() => {
            showToast('Reschedule request sent.');
        });
    });

    document.getElementById('btnFeedback').addEventListener('click', () => {
        const rating = prompt("Rate your last experience (1-5):");
        if(rating) {
            fetchAPI('/patient/feedback', { method: 'POST', body: JSON.stringify({ rating }) }).then(() => {
                showToast('Thank you for your feedback!');
            });
        }
    });
});
