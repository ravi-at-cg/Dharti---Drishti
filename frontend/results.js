// Load results from sessionStorage
window.addEventListener('DOMContentLoaded', () => {
    const resultsData = sessionStorage.getItem('analysisResults');
    
    if (!resultsData) {
        document.getElementById('resultsContainer').innerHTML = `
            <div style="text-align: center; padding: 60px 20px;">
                <h2 style="color: #666;">No Results Found</h2>
                <p style="color: #999; margin: 20px 0;">Please perform an analysis first.</p>
                <button onclick="window.location.href='index.html'" style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer;">Go to Analysis</button>
            </div>
        `;
        return;
    }
    
    try {
        const data = JSON.parse(resultsData);
        displayResults(data);
    } catch (error) {
        console.error('Error parsing results:', error);
        document.getElementById('resultsContainer').innerHTML = `
            <div style="text-align: center; padding: 60px 20px;">
                <h2 style="color: #d32f2f;">Error Loading Results</h2>
                <p style="color: #999;">${error.message}</p>
            </div>
        `;
    }
});

// Back button handler
document.getElementById('backBtn').addEventListener('click', () => {
    window.location.href = 'index.html';
});

function displayResults(data) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = renderAnalysisResults(data);
}

function renderAnalysisResults(data) {
    if (!data) return '<p>No data received</p>';
    
    const parts = [];
    
    if (data.summary) parts.push(renderSummary(data.summary));
    if (data.general_land_preparation) parts.push(renderLandPreparation(data.general_land_preparation));
    if (data.crop_recommendations && data.crop_recommendations.length > 0) parts.push(renderCropRecommendations(data.crop_recommendations));
    if (data.general_tips) parts.push(renderGeneralTips(data.general_tips));
    if (data.rotation_plan) parts.push(renderRotationPlan(data.rotation_plan));
    
    const result = parts.filter(p => p).join('');
    return result ? `<div class="analysis-container">${result}</div>` : '<p>No displayable data</p>';
}

function renderSummary(summary) {
    return summary ? `<div class="card summary-card"><div class="card-header"><span class="icon">📋</span><h3>Summary</h3></div><p class="summary-text">${summary}</p></div>` : '';
}

function renderLandPreparation(landPrep) {
    if (!landPrep || !landPrep.before_any_crop || landPrep.before_any_crop.length === 0) return '';
    const items = landPrep.before_any_crop.map(item => `<div class="prep-item"><div class="prep-header"><span class="product-name">${item.product || 'N/A'}</span><span class="amount-badge">${item.amount || 'N/A'}</span></div><p class="prep-reason">${item.why || ''}</p></div>`).join('');
    return `<div class="card"><div class="card-header"><span class="icon">🚜</span><h3>General Land Preparation</h3></div><div class="prep-list">${items}</div></div>`;
}

function renderCropRecommendations(crops) {
    if (!crops || crops.length === 0) return '';
    return crops.map(crop => {
        const whatToAddHtml = crop.what_to_add ? renderWhatToAdd(crop.what_to_add) : '';
        const wateringHtml = crop.watering_guide ? renderWateringGuide(crop.watering_guide) : '';
        const monthlyHtml = crop.month_by_month_plan ? renderMonthlyPlan(crop.month_by_month_plan) : '';
        const problemsHtml = crop.common_problems ? renderCommonProblems(crop.common_problems) : '';
        const tipsHtml = crop.harvest_tips ? renderHarvestTips(crop.harvest_tips) : '';
        return `<div class="card crop-card"><div class="card-header crop-header"><span class="icon">🌾</span><h3>${crop.crop_name || 'Unknown'}</h3></div><div class="crop-overview"><div class="info-grid">${crop.expected_harvest ? `<div class="info-item"><span class="label">Expected Harvest</span><span class="value">${crop.expected_harvest}</span></div>` : ''}${crop.total_growing_days ? `<div class="info-item"><span class="label">Growing Days</span><span class="value">${crop.total_growing_days} days</span></div>` : ''}${crop.planting_time ? `<div class="info-item"><span class="label">Planting Time</span><span class="value">${crop.planting_time}</span></div>` : ''}${crop.harvest_time ? `<div class="info-item"><span class="label">Harvest Time</span><span class="value">${crop.harvest_time}</span></div>` : ''}</div>${crop.why_good ? `<div class="why-good"><strong>Why this crop?</strong> ${crop.why_good}</div>` : ''}</div>${whatToAddHtml}${wateringHtml}${monthlyHtml}${problemsHtml}${tipsHtml}</div>`;
    }).join('');
}

function renderWhatToAdd(whatToAdd) {
    if (!whatToAdd) return '';
    const beforePlanting = (whatToAdd.before_planting || []).map(item => `<div class="fertilizer-item"><div class="fert-header"><span class="fert-name">${item.product || 'N/A'}</span><span class="fert-amount">${item.amount || 'N/A'}</span></div>${item.why ? `<p class="fert-reason">${item.why}</p>` : ''}</div>`).join('');
    const duringGrowing = (whatToAdd.during_growing || []).map(item => `<div class="fertilizer-item"><div class="fert-header"><span class="fert-name">${item.product || 'N/A'}</span><span class="fert-amount">${item.amount || 'N/A'}</span></div>${item.when ? `<p class="fert-when">⏰ ${item.when}</p>` : ''}${item.why ? `<p class="fert-reason">${item.why}</p>` : ''}</div>`).join('');
    if (!beforePlanting && !duringGrowing) return '';
    return `<div class="section"><h4>🧪 What to Add</h4>${beforePlanting ? `<div class="subsection"><h5>Before Planting</h5>${beforePlanting}</div>` : ''}${duringGrowing ? `<div class="subsection"><h5>During Growing</h5>${duringGrowing}</div>` : ''}</div>`;
}

function renderWateringGuide(watering) {
    if (!watering) return '';
    const criticalStages = (watering.critical_stages || []).map(stage => `<span class="stage-badge">${stage}</span>`).join('');
    const hasContent = watering.method || watering.schedule || watering.total_water_needed || criticalStages;
    if (!hasContent) return '';
    return `<div class="section"><h4>💧 Watering Guide</h4><div class="watering-info">${watering.method ? `<div class="water-item"><strong>Method:</strong> ${watering.method}</div>` : ''}${watering.schedule ? `<div class="water-item"><strong>Schedule:</strong> ${watering.schedule}</div>` : ''}${watering.total_water_needed ? `<div class="water-item"><strong>Total Water Needed:</strong> ${watering.total_water_needed}</div>` : ''}${criticalStages ? `<div class="water-item"><strong>Critical Stages:</strong><div class="stages">${criticalStages}</div></div>` : ''}</div></div>`;
}

function renderMonthlyPlan(plan) {
    if (!plan || typeof plan !== 'object' || Object.keys(plan).length === 0) return '';
    const months = Object.keys(plan).sort().map(monthKey => {
        const monthNum = monthKey.replace('month_', '');
        const tasks = plan[monthKey];
        if (!tasks || !Array.isArray(tasks) || tasks.length === 0) return '';
        const tasksList = tasks.map(task => `<li>${task}</li>`).join('');
        return `<div class="month-card"><div class="month-header">Month ${monthNum}</div><ul class="task-list">${tasksList}</ul></div>`;
    }).filter(m => m).join('');
    return months ? `<div class="section"><h4>📅 Month-by-Month Plan</h4><div class="monthly-grid">${months}</div></div>` : '';
}

function renderCommonProblems(problems) {
    if (!problems) return '';
    const pests = (problems.pests || []).map(p => `<li>${p}</li>`).join('');
    const diseases = (problems.diseases || []).map(d => `<li>${d}</li>`).join('');
    const weather = (problems.weather_issues || []).map(w => `<li>${w}</li>`).join('');
    if (!pests && !diseases && !weather) return '';
    return `<div class="section"><h4>⚠️ Common Problems & Solutions</h4><div class="problems-grid">${pests ? `<div class="problem-category"><h5>🐛 Pests</h5><ul>${pests}</ul></div>` : ''}${diseases ? `<div class="problem-category"><h5>🦠 Diseases</h5><ul>${diseases}</ul></div>` : ''}${weather ? `<div class="problem-category"><h5>🌦️ Weather Issues</h5><ul>${weather}</ul></div>` : ''}</div></div>`;
}

function renderHarvestTips(tips) {
    if (!tips || !Array.isArray(tips) || tips.length === 0) return '';
    const tipsList = tips.map(tip => `<li>${tip}</li>`).join('');
    return `<div class="section"><h4>✂️ Harvest Tips</h4><ul class="harvest-tips">${tipsList}</ul></div>`;
}

function renderGeneralTips(tips) {
    if (!tips) return '';
    const soilProtection = (tips.soil_protection || []).map(t => `<li>${t}</li>`).join('');
    const waterSaving = (tips.water_saving || []).map(t => `<li>${t}</li>`).join('');
    const costSaving = (tips.cost_saving || []).map(t => `<li>${t}</li>`).join('');
    if (!soilProtection && !waterSaving && !costSaving) return '';
    return `<div class="card"><div class="card-header"><span class="icon">💡</span><h3>General Tips</h3></div><div class="tips-grid">${soilProtection ? `<div class="tip-category"><h5>🛡️ Soil Protection</h5><ul>${soilProtection}</ul></div>` : ''}${waterSaving ? `<div class="tip-category"><h5>💧 Water Saving</h5><ul>${waterSaving}</ul></div>` : ''}${costSaving ? `<div class="tip-category"><h5>💰 Cost Saving</h5><ul>${costSaving}</ul></div>` : ''}</div></div>`;
}

function renderRotationPlan(plan) {
    if (!plan || typeof plan !== 'object' || Object.keys(plan).length === 0) return '';
    const years = Object.keys(plan).sort().map(yearKey => {
        const yearNum = yearKey.replace('year_', '');
        const desc = plan[yearKey];
        return desc ? `<div class="rotation-item"><div class="rotation-year">Year ${yearNum}</div><div class="rotation-desc">${desc}</div></div>` : '';
    }).filter(y => y).join('');
    return years ? `<div class="card"><div class="card-header"><span class="icon">🔄</span><h3>Crop Rotation Plan</h3></div><div class="rotation-plan">${years}</div></div>` : '';
}
