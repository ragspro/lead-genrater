"""
Dark mode CSS generator
"""

DARK_MODE_CSS = """
/* Dark Mode Styles */
body.dark-mode {
    background: #0F0F14;
    color: #E5E7EB;
}

body.dark-mode::before {
    background: 
        radial-gradient(circle at 20% 30%, rgba(124, 58, 237, 0.2) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(79, 70, 229, 0.2) 0%, transparent 50%);
}

body.dark-mode .glass-card {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.12);
}

body.dark-mode .glass-card:hover {
    border-color: rgba(124, 58, 237, 0.4);
}

body.dark-mode .lead-card {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.1);
}

body.dark-mode .lead-card:hover {
    border-color: rgba(124, 58, 237, 0.4);
}

body.dark-mode .form-input,
body.dark-mode .form-select,
body.dark-mode .search-box,
body.dark-mode .filter-select {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
    color: #E5E7EB;
}

body.dark-mode .content-body {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);
    color: #D1D5DB;
}

/* Light Mode Styles */
body.light-mode {
    background: #FFFFFF;
    color: #1F2937;
}

body.light-mode::before {
    background: 
        radial-gradient(circle at 20% 30%, rgba(124, 58, 237, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(79, 70, 229, 0.05) 0%, transparent 50%);
}

body.light-mode .glass-card {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(0, 0, 0, 0.1);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

body.light-mode .lead-card {
    background: rgba(255, 255, 255, 0.98);
    border-color: rgba(0, 0, 0, 0.08);
}

body.light-mode .form-input,
body.light-mode .form-select,
body.light-mode .search-box,
body.light-mode .filter-select {
    background: #F9FAFB;
    border-color: #D1D5DB;
    color: #1F2937;
}

body.light-mode .content-body {
    background: #F9FAFB;
    border-color: #E5E7EB;
    color: #374151;
}

body.light-mode .hero-subtitle,
body.light-mode .stat-label,
body.light-mode .detail-item {
    color: #6B7280;
}

body.light-mode .lead-title p {
    color: #6B7280;
}

/* Dark Mode Toggle Button */
.dark-mode-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    padding: 12px 20px;
    background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%);
    border: none;
    border-radius: 25px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
    transition: all 0.3s ease;
}

.dark-mode-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.6);
}

.dark-mode-toggle:active {
    transform: translateY(0);
}
"""

DARK_MODE_JS = """
// Dark Mode Toggle
function initDarkMode() {
    // Check saved preference
    const savedMode = localStorage.getItem('darkMode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial mode
    if (savedMode === 'dark' || (!savedMode && prefersDark)) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
    } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
    }
    
    // Update button text
    updateToggleButton();
}

function toggleDarkMode() {
    const isDark = document.body.classList.contains('dark-mode');
    
    if (isDark) {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('light-mode');
        localStorage.setItem('darkMode', 'light');
    } else {
        document.body.classList.remove('light-mode');
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'dark');
    }
    
    updateToggleButton();
}

function updateToggleButton() {
    const button = document.getElementById('darkModeToggle');
    if (button) {
        const isDark = document.body.classList.contains('dark-mode');
        button.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initDarkMode);
"""

def get_dark_mode_css():
    """Get dark mode CSS"""
    return DARK_MODE_CSS

def get_dark_mode_js():
    """Get dark mode JavaScript"""
    return DARK_MODE_JS
