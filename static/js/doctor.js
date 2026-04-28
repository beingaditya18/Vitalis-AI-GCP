document.addEventListener('DOMContentLoaded', () => {

    // Load Stats
    fetchAPI('/doctor/stats').then(data => {
        const statsHtml = `
            <div class="glass-panel">
                <h4>New Cases</h4><h2>${data.new_cases}</h2>
            </div>
            <div class="glass-panel">
                <h4>Total Assessments</h4><h2>${data.total_assessments}</h2>
            </div>
            <div class="glass-panel">
                <h4 style="color: var(--accent);">High-Risk Alerts</h4><h2>${data.high_risk_alerts}</h2>
            </div>
            <div class="glass-panel">
                <h4 style="color: var(--danger);">Critical</h4><h2>${data.critical_risk}</h2>
            </div>
        `;
        document.getElementById('doctorStats').innerHTML = statsHtml;
    });

    // Load Queue
    function loadQueue() {
        fetchAPI('/doctor/patients/queue/today').then(data => {
            const container = document.getElementById('queueContainer');
            if(data.queue.length === 0) {
                container.innerHTML = '<p>No pending summaries.</p>';
                return;
            }
            
            let html = '';
            data.queue.forEach(q => {
                const isHighRisk = q.severity === 'High' ? 'high-risk' : '';
                html += `
                    <div class="queue-item ${isHighRisk}">
                        <div>
                            <strong>Case #${q.id}</strong> - ${q.severity} Severity
                            <br>
                            <small>${q.symptoms.substring(0, 50)}...</small>
                        </div>
                        <button class="btn-glass btn-review" data-id="${q.id}">Review</button>
                    </div>
                `;
            });
            container.innerHTML = html;

            document.querySelectorAll('.btn-review').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    openReviewModal(e.target.dataset.id);
                });
            });
        });
    }

    loadQueue();

    // Modal Logic
    const overlay = document.getElementById('overlay');
    const modal = document.getElementById('reviewPanel');
    let currentCaseId = null;

    window.openReviewModal = (id) => {
        currentCaseId = id;
        fetchAPI(`/doctor/review/${id}`).then(data => {
            document.getElementById('modalPatientInput').textContent = data.symptoms;
            document.getElementById('modalAiSummary').value = data.ai_summary;
            document.getElementById('modalRiskScore').textContent = data.risk_score || 'N/A';
            
            // Mock citations
            document.getElementById('modalInsights').innerHTML = '<ul><li>Clinical Guideline 2024 - Section 4</li><li>Similar case history matches: 85%</li></ul>';
            
            overlay.style.display = 'block';
            modal.style.display = 'block';
        });
    };

    const closeModal = () => {
        overlay.style.display = 'none';
        modal.style.display = 'none';
        currentCaseId = null;
    };

    document.getElementById('btnCloseModal').addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    document.getElementById('btnAccept').addEventListener('click', () => {
        const finalSummary = document.getElementById('modalAiSummary').value;
        fetchAPI(`/doctor/decision/${currentCaseId}`, {
            method: 'POST',
            body: JSON.stringify({ decision: 'Accepted', final_summary: finalSummary })
        }).then(() => {
            showToast('Summary accepted and saved.');
            closeModal();
            loadQueue();
        });
    });

    document.getElementById('btnReject').addEventListener('click', () => {
        const finalSummary = document.getElementById('modalAiSummary').value;
        fetchAPI(`/doctor/decision/${currentCaseId}`, {
            method: 'POST',
            body: JSON.stringify({ decision: 'Rejected', notes: finalSummary })
        }).then(() => {
            showToast('Summary rejected. Note saved.', 'error');
            closeModal();
            loadQueue();
        });
    });

    // Clinical Tools
    document.getElementById('btnRiskAssessment').addEventListener('click', () => {
        fetchAPI('/doctor/risk-assessment', { method: 'POST' }).then(res => showToast(`Calculated Risk Score: ${res.score}`));
    });

    document.getElementById('btnShap').addEventListener('click', () => {
        fetchAPI('/doctor/shap').then(res => showToast(`SHAP Analysis: ${res.explainability}`));
    });

    document.getElementById('btnRag').addEventListener('click', () => {
        fetchAPI('/doctor/rag-query', { method: 'POST' }).then(res => showToast(`RAG Citations Loaded. Check console.`));
    });

});
