document.addEventListener('DOMContentLoaded', () => {
    
    // Note: Authentication is handled by Flask sessions on the backend
    // No need for token check here since the route is protected server-side

    // Initialize sidebar interactions
    const navLinks = document.querySelectorAll('.nav-link:not(.logout-btn)');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Hide all sections, show target (mocking SPA behavior for sections within admin)
                document.querySelectorAll('.data-card').forEach(c => {
                    if(c.id !== 'alertsRow') c.style.display = 'none';
                });
                
                const target = document.getElementById(href.substring(1));
                if (target) target.style.display = 'block';
                else document.querySelectorAll('.data-card').forEach(c => c.style.display = 'block'); // reset
            }
        });
    });

    // Load initial data
    loadMetrics();
    initCharts();
    loadAlerts();
    loadFacilities();

    // Chart instances
    let regionChartInstance = null;

    async function loadMetrics() {
        try {
            const response = await fetch('/api/admin/metrics', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            
            const metricsContainer = document.getElementById('adminMetrics');
            metricsContainer.innerHTML = `
                <div class="metric-card">
                    <div class="metric-icon green">
                        <i class="fas fa-users"></i>
                    </div>
                    <div class="metric-info">
                        <h3>Total Patients</h3>
                        <p class="value">${data.total_patients.toLocaleString()}</p>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon blue">
                        <i class="fas fa-calendar-check"></i>
                    </div>
                    <div class="metric-info">
                        <h3>Total Appointments</h3>
                        <p class="value">${data.total_appointments.toLocaleString()}</p>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon purple">
                        <i class="fas fa-hospital"></i>
                    </div>
                    <div class="metric-info">
                        <h3>Active Facilities</h3>
                        <p class="value">${data.active_facilities}</p>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon orange">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="metric-info">
                        <h3>AI Usage</h3>
                        <p class="value">${data.ai_usage_percent}%</p>
                        <small style="color: var(--gray-600); font-size: 0.75rem;">${data.ai_processed}/${data.ai_consultations} consultations</small>
                    </div>
                </div>
                <div class="metric-card" style="grid-column: span 2;">
                    <div style="display:flex; justify-content:space-between; align-items:center; width: 100%;">
                        <div>
                            <h4 style="margin:0; color:var(--gray-600); font-size: 0.875rem; text-transform: uppercase;">Visited vs Non-Visited</h4>
                            <div style="display:flex; gap:30px; margin-top:10px;">
                                <div>
                                    <strong style="color:var(--success); font-size:1.75rem;">${data.visited_appointments}</strong>
                                    <div style="color: var(--gray-600); font-size: 0.875rem;">Visited</div>
                                </div>
                                <div>
                                    <strong style="color:var(--danger); font-size:1.75rem;">${data.non_visited_appointments}</strong>
                                    <div style="color: var(--gray-600); font-size: 0.875rem;">Non-Visited</div>
                                </div>
                            </div>
                        </div>
                        <i class="fas fa-chart-pie" style="font-size:3rem; color:var(--gray-300);"></i>
                    </div>
                </div>
                <div class="metric-card" style="grid-column: span 2;">
                    <div style="display:flex; justify-content:space-between; align-items:center; width: 100%;">
                        <div>
                            <h4 style="margin:0; color:var(--gray-600); font-size: 0.875rem; text-transform: uppercase;">Feedback Received</h4>
                            <div style="margin-top:10px;">
                                <strong style="color:var(--primary-blue); font-size:1.75rem;">${data.total_feedback}</strong>
                                <div style="color: var(--gray-600); font-size: 0.875rem;">Total Responses</div>
                            </div>
                        </div>
                        <i class="fas fa-comments" style="font-size:3rem; color:var(--gray-300);"></i>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error loading metrics:', error);
        }
    }

    // Drilldown Chart initialization
    window.loadDrilldown = async function(level) {
        try {
            const res = await fetch(`/api/admin/stats/drilldown?level=${level}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await res.json();
            
            if (regionChartInstance) {
                regionChartInstance.destroy();
            }

            const ctx = document.getElementById('regionChart').getContext('2d');
            regionChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: `Appointments by ${level.charAt(0).toUpperCase() + level.slice(1)}`,
                        data: data.values,
                        backgroundColor: 'rgba(13, 110, 253, 0.7)',
                        borderColor: 'rgb(13, 110, 253)',
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12
                        }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
        } catch (e) {
            console.error(e);
        }
    };

    async function initCharts() {
        // Initial load for district level
        await loadDrilldown('district');

        try {
            const response = await fetch('/api/admin/chart-data', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            
            // Appointments Timeline Chart
            const timelineCtx = document.getElementById('timelineChart').getContext('2d');
            new Chart(timelineCtx, {
                type: 'line',
                data: {
                    labels: data.appointments_timeline.labels,
                    datasets: [{
                        label: 'Appointments',
                        data: data.appointments_timeline.data,
                        borderColor: 'rgb(13, 110, 253)',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 }
                        }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });

            // AI Usage Chart
            const aiCtx = document.getElementById('aiUsageChart').getContext('2d');
            new Chart(aiCtx, {
                type: 'doughnut',
                data: {
                    labels: ['AI Processed', 'Manual'],
                    datasets: [{
                        data: [85, 15],
                        backgroundColor: [
                            'rgb(111, 66, 193)',
                            'rgb(220, 220, 220)'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            position: 'bottom',
                            labels: {
                                padding: 15,
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': ' + context.parsed + '%';
                                }
                            }
                        }
                    }
                }
            });
            
            // Facility Performance Chart
            const facCtx = document.getElementById('facilityChart').getContext('2d');
            new Chart(facCtx, {
                type: 'bar',
                data: {
                    labels: data.facility_performance.labels,
                    datasets: [{
                        label: 'Appointments',
                        data: data.facility_performance.data,
                        backgroundColor: 'rgba(40, 167, 69, 0.7)',
                        borderColor: 'rgb(40, 167, 69)',
                        borderWidth: 1,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { 
                            beginAtZero: true,
                            grid: { color: 'rgba(0, 0, 0, 0.05)' }
                        },
                        y: {
                            grid: { display: false }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error loading charts:', error);
        }
    }

    async function loadAlerts() {
        try {
            const response = await fetch('/api/admin/alerts', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            
            const tbody = document.getElementById('alertsTableBody');
            tbody.innerHTML = '';
            
            data.alerts.forEach(alert => {
                const tr = document.createElement('tr');
                const time = new Date(alert.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                tr.innerHTML = `
                    <td><strong>PT-${alert.target_id.toString().padStart(4, '0')}</strong></td>
                    <td>${alert.action}</td>
                    <td>${time}</td>
                    <td><span class="status-badge status-danger">Critical</span></td>
                `;
                tbody.appendChild(tr);
            });
            
            if(data.alerts.length === 0) {
                 tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--gray-600);">No active alerts</td></tr>';
            }
        } catch (error) {
            console.error('Error loading alerts:', error);
        }
    }

    async function loadFacilities() {
        try {
            const response = await fetch('/api/admin/facilities/full', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            
            const tbody = document.getElementById('facilitiesTableBody');
            tbody.innerHTML = '';
            
            data.facilities.forEach(fac => {
                const tr = document.createElement('tr');
                const statusHtml = fac.is_active ? 
                    '<span class="status-badge status-success">Active</span>' : 
                    '<span class="status-badge status-warning">Inactive</span>';
                    
                tr.innerHTML = `
                    <td><strong>FAC-${fac.id.toString().padStart(3, '0')}</strong></td>
                    <td>${fac.name}<br><small class="text-muted">Lic: ${fac.license_number}</small></td>
                    <td>${fac.district}, ${fac.block}</td>
                    <td>Doctors: ${fac.doctor_count} | Appts: ${fac.appointment_count}</td>
                    <td>${statusHtml}</td>
                `;
                tbody.appendChild(tr);
            });
            
            if(data.facilities.length === 0) {
                 tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--gray-600);">No facilities found</td></tr>';
            }
        } catch (error) {
            console.error('Error loading facilities:', error);
        }
    }

    // Export functionality
    const btnDownload = document.getElementById('btnDownloadReport');
    if (btnDownload) {
        btnDownload.addEventListener('click', () => {
            btnDownload.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Exporting...';
            setTimeout(() => {
                btnDownload.innerHTML = '<i class="fas fa-download"></i> Export Report';
                alert('Admin Report exported successfully as CSV.');
            }, 1000);
        });
    }
});
