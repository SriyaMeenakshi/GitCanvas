// ========== GitCanvas Web App Builder ==========
const API_BASE_URL = 'http://127.0.0.1:8000';
const DEFAULT_USERNAME = 'torvalds';

// ========== DOM Elements ==========
const htmlElement = document.documentElement;

// Inputs
const usernameInput = document.getElementById('username');
const authTokenInput = document.getElementById('authToken');
const loadProfileBtn = document.getElementById('loadProfileBtn');
const themeSelect = document.getElementById('themeSelect');
const fontSelect = document.getElementById('fontSelect');
const animationsToggle = document.getElementById('animationsToggle');
const compactToggle = document.getElementById('compactToggle');

// Colors
const bgColorInput = document.getElementById('bgColor');
const titleColorInput = document.getElementById('titleColor');
const textColorInput = document.getElementById('textColor');
const borderColorInput = document.getElementById('borderColor');
const resetColorsBtn = document.getElementById('resetColorsBtn');

// UI state
const themeToggleSidebar = document.getElementById('themeToggleSidebar');
const previewStatus = document.getElementById('previewStatus');
const refreshPreviewBtn = document.getElementById('refreshPreviewBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');

// Tabs
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// AI Buttons
const generateRoastBtn = document.getElementById('generateRoastBtn');
const generateDescriptionBtn = document.getElementById('generateDescriptionBtn');
const roastOutput = document.getElementById('roastOutput');
const descriptionOutput = document.getElementById('descriptionOutput');

// ========== State ==========
let currentUsername = DEFAULT_USERNAME;
let isProfileLoaded = false;

// ========== Theme Management ==========
function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  htmlElement.setAttribute('data-theme', savedTheme);
}
function toggleTheme() {
  const currentTheme = htmlElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  htmlElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}
if (themeToggleSidebar) {
  themeToggleSidebar.addEventListener('click', toggleTheme);
}
initTheme();

// ========== Tab Navigation ==========
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // Remove active from all
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    // Add active to clicked
    btn.classList.add('active');
    const targetId = btn.getAttribute('data-target');
    const targetContent = document.getElementById(targetId);
    if (targetContent) {
      targetContent.classList.add('active');
    }
  });
});

// ========== API Functions ==========
function getCustomColors() {
  const colors = {};
  if (bgColorInput.value !== '#000000') colors.bg_color = bgColorInput.value.replace('#', '');
  if (titleColorInput.value !== '#2F80ED') colors.title_color = titleColorInput.value.replace('#', '');
  if (textColorInput.value !== '#434D56') colors.text_color = textColorInput.value.replace('#', '');
  if (borderColorInput.value !== '#E4E2E2') colors.border_color = borderColorInput.value.replace('#', '');
  return colors;
}

function buildApiUrl(endpoint, extraParams = {}) {
  const params = new URLSearchParams({
    username: currentUsername,
    theme: themeSelect.value,
    animations_enabled: animationsToggle.checked,
    ...getCustomColors(),
    ...extraParams
  });
  if (fontSelect.value !== 'Theme Default') {
    params.set('font', fontSelect.value);
  }
  if (authTokenInput.value.trim()) {
    params.set('token', authTokenInput.value.trim());
  }
  return `${API_BASE_URL}${endpoint}?${params.toString()}`;
}

async function loadProfile() {
  const username = usernameInput.value.trim();
  if (!username) {
    showError('Please enter a GitHub username');
    return;
  }
  currentUsername = username;
  isProfileLoaded = true;
  previewStatus.textContent = `Profile loaded: @${currentUsername}`;
  errorMessage.style.display = 'none';
  
  // Refresh all previews
  refreshAllCards();
}

function showError(msg) {
  errorMessage.textContent = msg;
  errorMessage.style.display = 'block';
  setTimeout(() => { errorMessage.style.display = 'none'; }, 5000);
}

// ========== Card Rendering ==========
const cardMap = [
  { id: 'stats', endpoint: '/api/stats' },
  { id: 'languages', endpoint: '/api/languages' },
  { id: 'repos', endpoint: '/api/repos' },
  { id: 'contributions', endpoint: '/api/contributions' },
  { id: 'streak', endpoint: '/api/streak' },
  { id: 'calendar-heatmap', endpoint: '/api/calendar-heatmap' },
  { id: 'actions', endpoint: '/api/actions' },
  { id: 'badges', endpoint: '/api/badges' },
  { id: 'social', endpoint: '/api/social_card' },
  { id: 'trophy', endpoint: '/api/trophy' }
];

async function refreshAllCards() {
  if (!isProfileLoaded) return;
  loadingSpinner.style.display = 'block';
  
  // Get Embed Format
  const embedFormat = document.querySelector('input[name="embedFormat"]:checked')?.value || 'markdown';

  // Load Theme Gallery
  const galleryEl = document.getElementById('themeGalleryPreview');
  if (galleryEl) {
    galleryEl.innerHTML = '';
    const allThemes = [
      'Radical', 'Cyberpunk', 'Stranger Things', 'Space', 'Ocean', 
      'Marvel', 'Pacman', 'Matrix', 'Synthwave', 'Dracula', 
      'Neon', 'Fire', 'Forest', 'Midnight', 'Aurora', 'Default'
    ];
    allThemes.forEach(t => {
      const url = buildApiUrl('/api/stats', { theme: t, hide_stars: true, hide_followers: true });
      const themeItem = document.createElement('div');
      themeItem.className = 'theme-preview-item';
      themeItem.style.cursor = 'pointer';
      themeItem.innerHTML = `
        <h4>${t}</h4>
        <img src="${url}" alt="${t} theme preview" loading="lazy" style="pointer-events:none;" onerror="this.style.display='none'" />
      `;
      themeItem.onclick = () => {
        const themeSelect = document.getElementById('themeSelect');
        if (themeSelect) {
          themeSelect.value = t;
          refreshAllCards(); // Re-render with new theme
        }
      };
      galleryEl.appendChild(themeItem);
    });
  }

  // Load individual cards
  cardMap.forEach(async (card) => {
    const imgEl = document.getElementById(`preview-${card.id}`);
    const emptyState = imgEl?.nextElementSibling;
    const markdownEl = document.getElementById(`markdown-${card.id}`);
    
    if (imgEl || markdownEl) {
      const url = buildApiUrl(card.endpoint);
      
      if (markdownEl) {
        if (embedFormat === 'html') {
          markdownEl.value = `<a href="https://github.com/${currentUsername}">\n  <img src="${url}" alt="${card.id}" />\n</a>`;
        } else {
          markdownEl.value = `[![${card.id}](${url})](https://github.com/${currentUsername})`;
        }
      }

      if (imgEl) {
        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error('Failed');
          const blob = await response.blob();
          imgEl.src = URL.createObjectURL(blob);
          imgEl.style.display = 'block';
          if (emptyState && emptyState.classList.contains('empty-state')) emptyState.style.display = 'none';
        } catch (e) {
          console.error(`Failed to load ${card.id}`, e);
        }
      }
    }
  });
  
  loadingSpinner.style.display = 'none';
}

// ========== AI Functions ==========
async function generateAIRoast() {
  if (!isProfileLoaded) {
    showError('Please load a profile first');
    return;
  }
  generateRoastBtn.disabled = true;
  generateRoastBtn.textContent = 'Generating...';
  roastOutput.textContent = 'Analyzing commits...';
  roastOutput.style.display = 'block';
  roastOutput.classList.remove('filled');

  try {
    const response = await fetch(`${API_BASE_URL}/api/ai/roast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: currentUsername })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    
    if (data.roast) {
      roastOutput.textContent = data.roast;
      roastOutput.classList.add('filled');
    } else {
      throw new Error(data.error || 'Failed to generate');
    }
  } catch (error) {
    roastOutput.textContent = `Error: ${error.message}`;
  } finally {
    generateRoastBtn.disabled = false;
    generateRoastBtn.textContent = 'Generate Roast';
  }
}

async function generateAIDescription() {
  if (!isProfileLoaded) {
    showError('Please load a profile first');
    return;
  }
  generateDescriptionBtn.disabled = true;
  generateDescriptionBtn.textContent = 'Generating...';
  descriptionOutput.textContent = 'Drafting summary...';
  descriptionOutput.style.display = 'block';
  descriptionOutput.classList.remove('filled');

  try {
    const response = await fetch(`${API_BASE_URL}/api/ai/description`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: currentUsername, theme: themeSelect.value })
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    
    if (data.description) {
      descriptionOutput.textContent = data.description;
      descriptionOutput.classList.add('filled');
    } else {
      throw new Error(data.error || 'Failed to generate');
    }
  } catch (error) {
    descriptionOutput.textContent = `Error: ${error.message}`;
  } finally {
    generateDescriptionBtn.disabled = false;
    generateDescriptionBtn.textContent = 'Generate Description';
  }
}

// ========== Event Listeners ==========
loadProfileBtn.addEventListener('click', loadProfile);
refreshPreviewBtn.addEventListener('click', refreshAllCards);
resetColorsBtn.addEventListener('click', () => {
  bgColorInput.value = '#000000';
  titleColorInput.value = '#2F80ED';
  textColorInput.value = '#434D56';
  borderColorInput.value = '#E4E2E2';
  refreshAllCards();
});

document.querySelectorAll('input[name="embedFormat"]').forEach(radio => {
  radio.addEventListener('change', () => {
    if (isProfileLoaded) refreshAllCards();
  });
});

// Auto-refresh when core settings change
[themeSelect, fontSelect, animationsToggle, compactToggle].forEach(el => {
  el.addEventListener('change', () => {
    if (isProfileLoaded) refreshAllCards();
  });
});

generateRoastBtn?.addEventListener('click', generateAIRoast);
generateDescriptionBtn?.addEventListener('click', generateAIDescription);

// ========== Initialization ==========
document.addEventListener('DOMContentLoaded', () => {
  // Pre-load default profile
  setTimeout(() => {
    loadProfile();
  }, 500);

  // Fetch initial API Limit
  fetch('https://api.github.com/rate_limit')
    .then(r => r.json())
    .then(data => {
      const remaining = data.resources.core.remaining;
      const limit = data.resources.core.limit;
      const textEl = document.getElementById('apiLimitText');
      if (textEl) textEl.textContent = `${remaining}/${limit}`;
    })
    .catch(() => {});
});
