document.addEventListener('DOMContentLoaded', () => {

    // Load Overview Stats
    fetchAPI('/asha/overview').then(data => {
        const statsHtml = `
            <div class="glass-panel">
                <h4>Total Patients</h4><h2>${data.total_patients}</h2>
            </div>
            <div class="glass-panel">
                <h4 style="color: var(--danger);">High-Risk Patients</h4><h2>${data.high_risk_patients}</h2>
            </div>
            <div class="glass-panel">
                <h4 style="color: var(--secondary);">Tasks Completed</h4><h2>${data.tasks_completed}</h2>
            </div>
            <div class="glass-panel">
                <h4 style="color: var(--primary);">Status</h4><h2>${data.work_status}</h2>
            </div>
        `;
        document.getElementById('ashaStats').innerHTML = statsHtml;
    });

    // Load Tasks
    function loadTasks() {
        fetchAPI('/asha/tasks').then(data => {
            const container = document.getElementById('taskList');
            if(data.tasks.length === 0) {
                container.innerHTML = '<p>No tasks for today. Great job!</p>';
                return;
            }
            
            let html = '';
            data.tasks.forEach(t => {
                const checked = t.completed ? 'checked' : '';
                const completedClass = t.completed ? 'completed' : '';
                html += `
                    <li class="task-item ${completedClass}">
                        <input type="checkbox" class="task-check" data-id="${t.id}" ${checked}>
                        <span>${t.desc}</span>
                    </li>
                `;
            });
            container.innerHTML = html;

            document.querySelectorAll('.task-check').forEach(chk => {
                chk.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        const id = e.target.dataset.id;
                        fetchAPI(`/asha/tasks/${id}/complete`, { method: 'POST' }).then(() => {
                            showToast('Task marked as complete!');
                            loadTasks(); // reload
                        });
                    }
                });
            });
        });
    }

    loadTasks();

    // Initialize Charts
    const ctxRisk = document.getElementById('riskChart').getContext('2d');
    new Chart(ctxRisk, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                data: [60, 25, 15],
                backgroundColor: ['#50E3C2', '#F5A623', '#D0021B'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#fff' } }
            }
        }
    });

    const ctxVisits = document.getElementById('visitsChart').getContext('2d');
    new Chart(ctxVisits, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'House Visits',
                data: [12, 19, 15, 8],
                backgroundColor: 'rgba(74, 144, 226, 0.7)',
                borderColor: '#4A90E2',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#ccc' } },
                x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#ccc' } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

});
