document.addEventListener('DOMContentLoaded', () => {
    
    const leadForm = document.getElementById('leadForm');
    const recoSection = document.getElementById('recommendationSection');
    const recoList = document.getElementById('recommendationList');

    if (leadForm) {
        leadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btn = leadForm.querySelector('button');
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            btn.disabled = true;

            const payload = {
                patient_name: document.getElementById('patientName').value,
                phone: document.getElementById('phone').value,
                district: document.getElementById('district').value,
                block: document.getElementById('block').value,
                village: document.getElementById('village').value,
                health_issue: document.getElementById('healthIssue').value
            };

            try {
                const res = await fetch('/api/cis/call-center/lead', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                
                const data = await res.json();
                
                // Show recommendations
                recoSection.style.display = 'block';
                recoList.innerHTML = '';
                
                data.recommendations.forEach(rec => {
                    recoList.innerHTML += `
                        <div class="facility-card" style="border:1px solid #ddd; padding:15px; border-radius:8px; margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between;">
                                <h4>${rec.name}</h4>
                                <span style="background:#28a745; color:white; padding:3px 8px; border-radius:12px; font-size:12px;">★ ${rec.rating}</span>
                            </div>
                            <p style="color:#666; margin:5px 0;">${rec.specialties}</p>
                            <p style="font-size:12px; color:#888;">Distance: ${rec.distance}</p>
                            <button onclick="bookAppointment(${rec.id}, ${data.case_id}, '${payload.patient_name}', '${payload.phone}')" style="margin-top:10px; background:#2b7a78; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">
                                Book Appointment & Gen ABHA
                            </button>
                        </div>
                    `;
                });
                
            } catch (err) {
                console.error(err);
                alert("Error processing lead");
            } finally {
                btn.innerHTML = 'Submit & Get Recommendations';
                btn.disabled = false;
            }
        });
    }

    // Load active cases
    loadCases();
});

async function bookAppointment(facilityId, caseId, pName, pPhone) {
    alert(`MOCK: Initiating booking for ${pName} at Facility ID ${facilityId}...\nGenerating ABHA card...`);
    
    // First generate ABHA
    try {
        const abhaRes = await fetch('/api/cis/abha/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name: pName, phone: pPhone, case_id: caseId })
        });
        const abhaData = await abhaRes.json();
        
        // Then book appointment
        const apptRes = await fetch('/api/cis/appointment/book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                case_id: caseId,
                facility_id: facilityId,
                date: new Date().toISOString(),
                phone: pPhone,
                patient_name: pName
            })
        });
        const apptData = await apptRes.json();
        
        alert(`SUCCESS!\n\nAppointment Booked.\nSMS Status: ${apptData.sms_status}\n\nGenerated ABHA: ${abhaData.abha_data.abha_number}`);
        location.reload();
    } catch (e) {
        console.error(e);
        alert('Error in booking flow');
    }
}

async function loadCases() {
    const tbody = document.getElementById('casesTableBody');
    if (!tbody) return;
    
    try {
        const res = await fetch('/api/admin/crm/cases');
        const data = await res.json();
        
        if (data.cases.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No active cases found</td></tr>';
            return;
        }
        
        tbody.innerHTML = '';
        data.cases.forEach(c => {
            const statusClass = c.status === 'booked' ? 'success' : (c.status === 'open' ? 'warning' : 'info');
            tbody.innerHTML += `
                <tr>
                    <td>#${c.id}</td>
                    <td>${c.patient_name}</td>
                    <td>${c.phone}</td>
                    <td><span class="status-badge ${statusClass}">${c.status.toUpperCase()}</span></td>
                    <td>
                        <button class="btn-sm" style="background:#17a2b8;color:white;border:none;padding:5px 10px;border-radius:4px;cursor:pointer;">
                            View Details
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch(e) {
        console.error(e);
    }
}
