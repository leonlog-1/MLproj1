/**
 * script.js
 * Frontend controller for SymptomAI Disease Prediction
 * Features:
 * - Real-time symptom search & autocomplete
 * - Multi-symptom chip management
 * - Visual Figure 1: Circular SVG Confidence Gauge with dynamic color
 * - Visual Figure 2: Differential Diagnosis Probability Distribution Chart
 * - Clinical Explanation & Pathophysiological Overview
 * - Visual Figure 3: Recommended Precautions & Action Cards
 */

// Application State
const state = {
  allSymptoms: [],             // Array of { id: string, name: string }
  selectedSymptoms: new Set(), // Set of active symptom id strings
  isLoading: false,
  focusedDropdownIndex: -1
};

// DOM Elements
const elements = {
  searchInput: document.getElementById('symptomSearchInput'),
  clearSearchBtn: document.getElementById('clearSearchBtn'),
  dropdownList: document.getElementById('dropdownList'),
  dropdownItems: document.getElementById('dropdownItems'),
  dropdownEmpty: document.getElementById('dropdownEmpty'),
  chipsContainer: document.getElementById('chipsContainer'),
  emptyChipsHint: document.getElementById('emptyChipsHint'),
  selectedCount: document.getElementById('selectedCount'),
  clearAllBtn: document.getElementById('clearAllBtn'),
  predictBtn: document.getElementById('predictBtn'),
  btnSpinner: document.getElementById('btnSpinner'),
  errorAlert: document.getElementById('errorAlert'),
  errorMessage: document.getElementById('errorMessage'),
  resultCard: document.getElementById('resultCard'),
  
  // Clinical Header & Badges
  resultDiseaseName: document.getElementById('resultDiseaseName'),
  resultCategoryBadge: document.getElementById('resultCategoryBadge'),
  resultSystemBadge: document.getElementById('resultSystemBadge'),
  resultModelName: document.getElementById('resultModelName'),
  resultSeverity: document.getElementById('resultSeverity'),
  severityDot: document.getElementById('severityDot'),
  resultSpecialist: document.getElementById('resultSpecialist'),

  // Figure 1: Radial Gauge
  gaugeProgressCircle: document.getElementById('gaugeProgressCircle'),
  gaugePercentText: document.getElementById('gaugePercentText'),
  gaugeAssessmentText: document.getElementById('gaugeAssessmentText'),

  // Clinical Explanation
  resultExplanation: document.getElementById('resultExplanation'),

  // Figure 2: Differential Probability Chart
  differentialChartCard: document.getElementById('differentialChartCard'),
  distributionBarsList: document.getElementById('distributionBarsList'),

  // Figure 3: Precautions Grid
  precautionsGrid: document.getElementById('precautionsGrid'),

  // Evaluated Symptoms
  resultSymptomCount: document.getElementById('resultSymptomCount'),
  resultChips: document.getElementById('resultChips'),
  modifyBtn: document.getElementById('modifyBtn'),

  // Figure 4: SHAP Chart
  shapChartCard: document.getElementById('shapChartCard'),
  shapBarsList: document.getElementById('shapBarsList'),

  // Calibration badge
  resultCalibratedBadge: document.getElementById('resultCalibratedBadge')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  await fetchSymptoms();
  setupEventListeners();
});

/**
 * Fetches supported symptoms list from backend API.
 */
async function fetchSymptoms() {
  try {
    const response = await fetch('/api/symptoms');
    if (!response.ok) {
      throw new Error(`Failed to load symptoms: HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data.success && Array.isArray(data.symptoms)) {
      state.allSymptoms = data.symptoms;
      console.log(`Loaded ${state.allSymptoms.length} supported symptoms.`);
    } else {
      throw new Error(data.error || 'Invalid response from symptoms API.');
    }
  } catch (error) {
    console.error('Error fetching symptoms:', error);
    showError('Unable to connect to prediction engine. Please verify the backend server is running.');
  }
}

/**
 * Registers all UI event listeners.
 */
function setupEventListeners() {
  // Search input events
  elements.searchInput.addEventListener('input', handleSearchInput);
  elements.searchInput.addEventListener('keydown', handleSearchKeydown);
  elements.searchInput.addEventListener('focus', () => {
    if (elements.searchInput.value.trim().length > 0) {
      showDropdown();
    }
  });

  // Clear search input button
  elements.clearSearchBtn.addEventListener('click', () => {
    elements.searchInput.value = '';
    elements.clearSearchBtn.style.display = 'none';
    hideDropdown();
    elements.searchInput.focus();
  });

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!elements.searchInput.contains(e.target) && !elements.dropdownList.contains(e.target)) {
      hideDropdown();
    }
  });

  // Clear all selected symptoms
  elements.clearAllBtn.addEventListener('click', clearAllSymptoms);

  // Predict button
  elements.predictBtn.addEventListener('click', handlePredict);

  // Modify symptoms button
  elements.modifyBtn.addEventListener('click', () => {
    elements.searchInput.focus();
    elements.searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}

/**
 * Filters and renders dropdown suggestions based on user search term.
 */
function handleSearchInput(e) {
  const query = e.target.value.trim().toLowerCase();
  elements.clearSearchBtn.style.display = query.length > 0 ? 'block' : 'none';
  hideError();

  if (query.length === 0) {
    hideDropdown();
    return;
  }

  // Filter symptoms matching query
  const matches = state.allSymptoms.filter(item => 
    item.name.toLowerCase().includes(query) || item.id.toLowerCase().includes(query)
  );

  renderDropdownMatches(matches, query);
  showDropdown();
}

/**
 * Handles keyboard navigation within search results.
 */
function handleSearchKeydown(e) {
  const items = elements.dropdownItems.querySelectorAll('.dropdown-item');
  if (items.length === 0 || elements.dropdownList.style.display === 'none') return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    state.focusedDropdownIndex = Math.min(state.focusedDropdownIndex + 1, items.length - 1);
    updateDropdownFocus(items);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    state.focusedDropdownIndex = Math.max(state.focusedDropdownIndex - 1, 0);
    updateDropdownFocus(items);
  } else if (e.key === 'Enter') {
    e.preventDefault();
    if (state.focusedDropdownIndex >= 0 && state.focusedDropdownIndex < items.length) {
      items[state.focusedDropdownIndex].click();
    } else if (items.length > 0) {
      items[0].click();
    }
  } else if (e.key === 'Escape') {
    hideDropdown();
  }
}

function updateDropdownFocus(items) {
  items.forEach((item, index) => {
    if (index === state.focusedDropdownIndex) {
      item.classList.add('focused');
      item.scrollIntoView({ block: 'nearest' });
    } else {
      item.classList.remove('focused');
    }
  });
}

/**
 * Renders matching items into the dropdown list.
 */
function renderDropdownMatches(matches, query) {
  elements.dropdownItems.innerHTML = '';
  state.focusedDropdownIndex = -1;

  if (matches.length === 0) {
    elements.dropdownEmpty.style.display = 'block';
    return;
  }

  elements.dropdownEmpty.style.display = 'none';

  matches.forEach(item => {
    const li = document.createElement('li');
    li.className = 'dropdown-item';
    const isSelected = state.selectedSymptoms.has(item.id);

    if (isSelected) {
      li.classList.add('selected');
    }

    li.innerHTML = `
      <span>${highlightMatch(item.name, query)}</span>
      ${isSelected ? '<span style="font-size: 0.8rem;">✓ Added</span>' : '<span style="color: #94a3b8; font-size: 0.8rem;">+ Add</span>'}
    `;

    li.addEventListener('click', () => {
      toggleSymptom(item.id);
      elements.searchInput.value = '';
      elements.clearSearchBtn.style.display = 'none';
      hideDropdown();
      elements.searchInput.focus();
    });

    elements.dropdownItems.appendChild(li);
  });
}

function highlightMatch(text, query) {
  const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
  return text.replace(regex, '<strong>$1</strong>');
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function showDropdown() {
  elements.dropdownList.style.display = 'block';
}

function hideDropdown() {
  elements.dropdownList.style.display = 'none';
  state.focusedDropdownIndex = -1;
}

/**
 * Toggles a symptom in the active selection set.
 */
function toggleSymptom(symptomId) {
  if (state.selectedSymptoms.has(symptomId)) {
    state.selectedSymptoms.delete(symptomId);
  } else {
    state.selectedSymptoms.add(symptomId);
  }
  updateChipsDisplay();
  hideError();
}

/**
 * Re-renders the active selected symptom chips.
 */
function updateChipsDisplay() {
  const count = state.selectedSymptoms.size;
  elements.selectedCount.textContent = count;
  elements.clearAllBtn.style.display = count > 0 ? 'inline-block' : 'none';

  if (count === 0) {
    elements.chipsContainer.innerHTML = '';
    elements.chipsContainer.appendChild(elements.emptyChipsHint);
    elements.emptyChipsHint.style.display = 'block';
    return;
  }

  elements.emptyChipsHint.style.display = 'none';
  elements.chipsContainer.innerHTML = '';

  state.selectedSymptoms.forEach(symptomId => {
    const symptomObj = state.allSymptoms.find(s => s.id === symptomId);
    const displayName = symptomObj ? symptomObj.name : symptomId.replace(/_/g, ' ');

    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.innerHTML = `
      <span>${displayName}</span>
      <button type="button" class="chip-remove-btn" title="Remove symptom" aria-label="Remove ${displayName}">&times;</button>
    `;

    chip.querySelector('.chip-remove-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      state.selectedSymptoms.delete(symptomId);
      updateChipsDisplay();
    });

    elements.chipsContainer.appendChild(chip);
  });
}

/**
 * Clears all active symptoms.
 */
function clearAllSymptoms() {
  state.selectedSymptoms.clear();
  updateChipsDisplay();
  hideError();
  elements.resultCard.style.display = 'none';
}

/**
 * Submits active symptoms to the backend ML prediction endpoint.
 */
async function handlePredict() {
  hideError();

  if (state.selectedSymptoms.size === 0) {
    showError('Please select at least one symptom before evaluating.');
    elements.searchInput.focus();
    return;
  }

  if (state.isLoading) return;

  setLoadingState(true);

  try {
    const payload = {
      symptoms: Array.from(state.selectedSymptoms)
    };

    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || 'Failed to obtain disease prediction.');
    }

    renderPredictionResult(data.prediction);

  } catch (error) {
    console.error('Prediction API Error:', error);
    showError(error.message || 'An unexpected error occurred during prediction.');
  } finally {
    setLoadingState(false);
  }
}

/**
 * Displays the comprehensive prediction result card with figures and clinical explanation.
 */
function renderPredictionResult(pred) {
  // Primary Disease & Badges
  elements.resultDiseaseName.textContent = pred.display_name || pred.disease;
  elements.resultCategoryBadge.textContent = pred.category || 'General Medicine';
  elements.resultSystemBadge.textContent = pred.system || 'Systemic Health';
  elements.resultModelName.textContent = `${pred.model_name || 'ML Model'}`;

  // Calibration badge
  if (pred.is_calibrated) {
    elements.resultCalibratedBadge.style.display = 'inline-flex';
  } else {
    elements.resultCalibratedBadge.style.display = 'none';
  }
  elements.severityDot.style.backgroundColor = pred.urgency_color || '#0284c7';
  elements.resultSeverity.textContent = pred.severity || 'Moderate';
  elements.resultSpecialist.textContent = pred.specialist || 'General Physician';

  // Figure 1: Animate Circular Radial Gauge
  const confidence = pred.confidence || 0.0;
  const circumference = 314.159; // 2 * Math.PI * 50
  const offset = circumference * (1 - Math.min(1.0, confidence));
  
  elements.gaugeProgressCircle.style.strokeDashoffset = `${circumference}`;
  elements.gaugePercentText.textContent = pred.confidence_percent;

  // Dynamic color for gauge stroke based on certainty
  let strokeColor = '#0d9488'; // Teal for high
  let assessmentText = 'High Model Certainty';

  if (confidence >= 0.8) {
    strokeColor = '#0d9488';
    assessmentText = 'High Algorithmic Certainty';
  } else if (confidence >= 0.5) {
    strokeColor = '#0284c7';
    assessmentText = 'Moderate Probability';
  } else {
    strokeColor = '#f59e0b';
    assessmentText = 'Distributed Differential Match';
  }

  elements.gaugeProgressCircle.style.stroke = strokeColor;
  elements.gaugeAssessmentText.textContent = assessmentText;

  setTimeout(() => {
    elements.gaugeProgressCircle.style.strokeDashoffset = `${offset}`;
  }, 50);

  // Clinical Explanation
  elements.resultExplanation.textContent = pred.explanation || 'No detailed clinical explanation available.';

  // Figure 2: Differential Diagnosis Chart Bars
  renderDifferentialChart(pred.top_probabilities, strokeColor);

  // Figure 4: SHAP Symptom Contribution Chart
  renderShapChart(pred.shap_explanations);

  // Figure 3: Clinical Precautions Cards
  renderPrecautionsGrid(pred.precautions);

  // Evaluated Symptoms Chips
  elements.resultSymptomCount.textContent = pred.matched_symptoms.length;
  elements.resultChips.innerHTML = '';
  pred.matched_symptoms.forEach(symId => {
    const symObj = state.allSymptoms.find(s => s.id === symId);
    const name = symObj ? symObj.name : symId.replace(/_/g, ' ');
    const span = document.createElement('span');
    span.className = 'result-chip-static';
    span.textContent = name;
    elements.resultChips.appendChild(span);
  });

  // Reveal card and scroll into view smoothly
  elements.resultCard.style.display = 'flex';
  elements.resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Figure 4: Renders SHAP symptom contribution horizontal bar chart.
 */
function renderShapChart(shapData) {
  if (!Array.isArray(shapData) || shapData.length === 0) {
    elements.shapChartCard.style.display = 'none';
    return;
  }

  elements.shapChartCard.style.display = 'block';
  elements.shapBarsList.innerHTML = '';

  const maxContrib = Math.max(...shapData.map(d => d.contribution_pct), 1);

  shapData.forEach((item, index) => {
    const isPositive = item.shap_value >= 0;
    const pct = item.contribution_pct;
    const barWidth = Math.max(4, Math.min(100, (pct / maxContrib) * 100));

    const row = document.createElement('div');
    row.className = 'shap-bar-item';
    row.innerHTML = `
      <div class="shap-bar-label">
        <span class="shap-symptom-name">${item.display_name}</span>
        <span class="shap-pct ${isPositive ? 'shap-pct-pos' : 'shap-pct-neg'}">${isPositive ? '+' : '-'}${pct}%</span>
      </div>
      <div class="shap-bar-track">
        <div class="shap-bar-fill ${isPositive ? 'shap-fill-pos' : 'shap-fill-neg'}" style="width: 0%;"></div>
      </div>
    `;

    elements.shapBarsList.appendChild(row);

    setTimeout(() => {
      const fill = row.querySelector('.shap-bar-fill');
      if (fill) fill.style.width = `${barWidth}%`;
    }, 80 + index * 50);
  });
}

/**
 * Figure 2: Renders comparative horizontal probability distribution bars.
 */
function renderDifferentialChart(probabilities, defaultColor) {
  elements.distributionBarsList.innerHTML = '';

  if (!Array.isArray(probabilities) || probabilities.length === 0) {
    elements.differentialChartCard.style.display = 'none';
    return;
  }

  elements.differentialChartCard.style.display = 'block';

  probabilities.forEach((item, index) => {
    const barItem = document.createElement('div');
    barItem.className = 'dist-bar-item';

    const percent = Math.round(item.confidence * 100);
    const widthVal = Math.max(4, Math.min(100, percent));

    barItem.innerHTML = `
      <div class="dist-bar-header">
        <span class="dist-disease-name">${index === 0 ? '★ ' : ''}${item.disease}</span>
        <span class="dist-percent-badge">${item.confidence_percent}</span>
      </div>
      <div class="dist-bar-track">
        <div class="dist-bar-fill" style="width: 0%;"></div>
      </div>
    `;

    elements.distributionBarsList.appendChild(barItem);

    // Animate fill width
    setTimeout(() => {
      const fillEl = barItem.querySelector('.dist-bar-fill');
      if (fillEl) {
        fillEl.style.width = `${widthVal}%`;
        if (index > 0) {
          fillEl.style.background = '#94a3b8'; // Grey for secondary differentials
        }
      }
    }, 60 + index * 40);
  });
}

/**
 * Figure 3: Renders clinical precautions grid cards.
 */
function renderPrecautionsGrid(precautions) {
  elements.precautionsGrid.innerHTML = '';

  const list = Array.isArray(precautions) && precautions.length > 0 ? precautions : [
    'Monitor symptom progression closely and log occurrences.',
    'Maintain adequate rest and hydration.',
    'Schedule a consultation with a qualified physician.',
    'Seek emergency medical evaluation if acute symptoms escalate.'
  ];

  list.forEach((step, idx) => {
    const card = document.createElement('div');
    card.className = 'precaution-card';
    card.innerHTML = `
      <div class="precaution-num">${idx + 1}</div>
      <div class="precaution-text">${step}</div>
    `;
    elements.precautionsGrid.appendChild(card);
  });
}

function setLoadingState(loading) {
  state.isLoading = loading;
  elements.predictBtn.disabled = loading;
  elements.btnSpinner.style.display = loading ? 'inline-block' : 'none';
  elements.predictBtn.querySelector('.btn-label').textContent = loading ? 'Evaluating Symptoms...' : 'Predict Possible Condition';
}

function showError(msg) {
  elements.errorMessage.textContent = msg;
  elements.errorAlert.style.display = 'flex';
}

function hideError() {
  elements.errorAlert.style.display = 'none';
}
