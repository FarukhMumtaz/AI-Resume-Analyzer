"""
app.py — AI Resume Analyzer — Premium AI SaaS Dashboard
Handcrafted UI/UX with glassmorphism, animations, and modern design
Backend functionality fully preserved
"""

import os
import streamlit as st
from datetime import datetime

from resume_parser import parse_resume
from ai_utils import analyze_resume, get_api_status
from scoring import (
    extract_skills, calculate_ats_score, calculate_job_match,
    get_ats_feedback, ROLE_SKILLS, extract_job_skills
)
from ui_components import (
    render_navbar, render_metrics_grid, render_section_header,
    render_skill_section, render_progress_bar, render_info_card,
    render_interview_question, render_recommendation_card
)

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Resume Analyzer — Premium AI SaaS Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# PREMIUM CSS DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════════
   IMPORTS & VARIABLES
   ═══════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    /* Color System */
    --bg-primary: #0a0a14;
    --bg-secondary: #0f0f1e;
    --bg-tertiary: #1a1a2e;
    
    --surface-1: rgba(255, 255, 255, 0.03);
    --surface-2: rgba(255, 255, 255, 0.05);
    --surface-3: rgba(255, 255, 255, 0.08);
    
    --border-subtle: rgba(255, 255, 255, 0.06);
    --border-medium: rgba(255, 255, 255, 0.1);
    --border-strong: rgba(255, 255, 255, 0.15);
    
    --text-primary: #ffffff;
    --text-secondary: #e0e0f0;
    --text-muted: #a0a0c0;
    --text-subtle: #707088;
    
    --accent-primary: #667eea;
    --accent-secondary: #764ba2;
    --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    
    --success: #10b981;
    --success-bg: rgba(16, 185, 129, 0.1);
    --warning: #f59e0b;
    --warning-bg: rgba(245, 158, 11, 0.1);
    --danger: #ef4444;
    --danger-bg: rgba(239, 68, 68, 0.1);
    --info: #3b82f6;
    --info-bg: rgba(59, 130, 246, 0.1);
    
    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;
    --space-2xl: 3rem;
    
    /* Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --radius-full: 9999px;
    
    /* Shadows */
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
    --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.3);
    
    /* Transitions */
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ═══════════════════════════════════════════════════════════════
   GLOBAL RESETS & BASE STYLES
   ═══════════════════════════════════════════════════════════════ */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-tertiary) 100%) !important;
    color: var(--text-secondary);
}

.main {
    background: transparent !important;
    padding: 0 !important;
}

.stMainBlockContainer {
    padding: 0 !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

.block-container {
    padding: 0 !important;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM NAVBAR
   ═══════════════════════════════════════════════════════════════ */
.premium-navbar {
    background: rgba(10, 10, 20, 0.8);
    backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0.75rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    margin-bottom: var(--space-xl);
}

.navbar-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 var(--space-xl);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.navbar-left {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.navbar-icon {
    font-size: 1.5rem;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.navbar-text {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.navbar-title {
    color: var(--text-primary);
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.navbar-subtitle {
    color: var(--text-subtle);
    font-size: 0.7rem;
    font-weight: 500;
}

.navbar-right {
    display: flex;
    align-items: center;
}

.status-pill {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--surface-2);
    border: 1px solid var(--border-subtle);
    padding: 0.4rem 0.9rem;
    border-radius: var(--radius-full);
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
    transition: all var(--transition-base);
}

.status-pill:hover {
    background: var(--surface-3);
    border-color: var(--border-medium);
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    50% { opacity: 0.8; box-shadow: 0 0 0 4px rgba(16, 185, 129, 0); }
}

/* ═══════════════════════════════════════════════════════════════
   SIDEBAR REDESIGN
   ═══════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 10, 20, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-md) !important;
}

section[data-testid="stSidebar"] p {
    font-size: 0.8rem !important;
    line-height: 1.6 !important;
    color: var(--text-muted) !important;
}

section[data-testid="stSidebar"] hr {
    border: 0 !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: var(--space-lg) 0 !important;
}

/* ═══════════════════════════════════════════════════════════════
   MAIN CONTENT WRAPPER
   ═══════════════════════════════════════════════════════════════ */
.content-wrapper {
    padding: 0 var(--space-xl) var(--space-2xl) var(--space-xl);
    max-width: 1400px;
    margin: 0 auto;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM CARDS & CONTAINERS
   ═══════════════════════════════════════════════════════════════ */
.premium-card {
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: var(--space-xl);
    backdrop-filter: blur(10px);
    transition: all var(--transition-base);
}

.premium-card:hover {
    background: var(--surface-2);
    border-color: var(--border-medium);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.card-compact {
    padding: var(--space-lg);
}

/* ═══════════════════════════════════════════════════════════════
   UPLOAD SECTION
   ═══════════════════════════════════════════════════════════════ */
.upload-grid {
    display: grid;
    grid-template-columns: 1.3fr 0.7fr;
    gap: var(--space-lg);
    margin-bottom: var(--space-lg);
}

@media (max-width: 900px) {
    .upload-grid {
        grid-template-columns: 1fr;
    }
}

.field-label {
    display: block;
    color: var(--text-primary);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: var(--space-sm);
}

/* File Uploader Styling */
.stFileUploadDropzone {
    border: 2px dashed rgba(102, 126, 234, 0.3) !important;
    border-radius: var(--radius-md) !important;
    background: var(--surface-1) !important;
    padding: var(--space-xl) !important;
    transition: all var(--transition-base) !important;
    cursor: pointer !important;
}

.stFileUploadDropzone:hover {
    border-color: rgba(102, 126, 234, 0.6) !important;
    background: var(--surface-2) !important;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.05) !important;
}

/* Selectbox Styling */
.stSelectbox [data-baseweb="select"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-medium) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    transition: all var(--transition-base) !important;
}

.stSelectbox [data-baseweb="select"]:hover {
    border-color: rgba(102, 126, 234, 0.5) !important;
    background: var(--surface-3) !important;
}

.stSelectbox [data-baseweb="select"]:focus-within {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Textarea Styling */
.stTextArea textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-medium) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    padding: var(--space-md) !important;
    min-height: 100px !important;
    max-height: 140px !important;
    transition: all var(--transition-base) !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: var(--surface-3) !important;
}

.stTextArea textarea::placeholder {
    color: var(--text-subtle) !important;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM BUTTON
   ═══════════════════════════════════════════════════════════════ */
.button-container {
    display: flex;
    justify-content: center;
    margin: var(--space-xl) 0;
}

.stButton > button {
    background: var(--accent-gradient) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    min-width: 220px !important;
    transition: all var(--transition-base) !important;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25), 0 0 0 0 rgba(102, 126, 234, 0.4) !important;
    cursor: pointer !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.35), 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    filter: brightness(1.1) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM METRICS GRID
   ═══════════════════════════════════════════════════════════════ */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
    margin: var(--space-xl) 0;
}

@media (max-width: 1200px) {
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .metrics-grid {
        grid-template-columns: 1fr;
    }
}

.premium-metric-card {
    position: relative;
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    overflow: hidden;
    transition: all var(--transition-base);
    cursor: default;
}

.premium-metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--accent-gradient);
    opacity: 0;
    transition: opacity var(--transition-base);
}

.premium-metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--border-medium);
}

.premium-metric-card:hover::before {
    opacity: 1;
}

.premium-metric-card.success::before {
    background: linear-gradient(90deg, #10b981, #34d399);
}

.premium-metric-card.warning::before {
    background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.premium-metric-card.danger::before {
    background: linear-gradient(90deg, #ef4444, #f87171);
}

.premium-metric-card.info::before {
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.metric-icon {
    font-size: 1.5rem;
    margin-bottom: var(--space-sm);
    opacity: 0.8;
}

.metric-content {
    position: relative;
    z-index: 1;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: var(--space-xs);
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.premium-metric-card.success .metric-value {
    background: linear-gradient(135deg, #10b981, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.premium-metric-card.warning .metric-value {
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.premium-metric-card.danger .metric-value {
    background: linear-gradient(135deg, #ef4444, #f87171);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.premium-metric-card.info .metric-value {
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}

.metric-glow {
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.1), transparent);
    pointer-events: none;
    opacity: 0;
    transition: opacity var(--transition-slow);
}

.premium-metric-card:hover .metric-glow {
    opacity: 1;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM PROGRESS BARS
   ═══════════════════════════════════════════════════════════════ */
.premium-progress-container {
    margin: var(--space-md) 0;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-sm);
}

.progress-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.progress-value {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--accent-primary);
}

.progress-track {
    height: 8px;
    background: var(--surface-2);
    border-radius: var(--radius-full);
    overflow: hidden;
    position: relative;
}

.progress-fill {
    height: 100%;
    background: var(--accent-gradient);
    border-radius: var(--radius-full);
    position: relative;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    animation: slideIn 1s ease-out;
}

@keyframes slideIn {
    from { width: 0; }
}

.progress-fill.success {
    background: linear-gradient(90deg, #10b981, #34d399);
}

.progress-fill.warning {
    background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.progress-fill.danger {
    background: linear-gradient(90deg, #ef4444, #f87171);
}

.progress-fill.info {
    background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.progress-shine {
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shine 2s infinite;
}

@keyframes shine {
    to { left: 100%; }
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM TABS
   ═══════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--space-xs);
    background: var(--surface-1);
    border-radius: var(--radius-md);
    padding: var(--space-xs);
    border: 1px solid var(--border-subtle);
    backdrop-filter: blur(10px);
    margin-bottom: var(--space-xl);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.75rem;
    color: var(--text-muted) !important;
    padding: 0.6rem 1rem !important;
    border: none !important;
    transition: all var(--transition-base) !important;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--accent-gradient) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--surface-2) !important;
    color: var(--text-secondary) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"]:hover {
    background: var(--accent-gradient) !important;
    color: white !important;
}

/* ═══════════════════════════════════════════════════════════════
   SKILL PILLS
   ═══════════════════════════════════════════════════════════════ */
.skill-section {
    margin: var(--space-lg) 0;
}

.skill-section-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-primary);
    margin-bottom: var(--space-md);
}

.skill-pills-container {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-sm);
}

.skill-pill {
    display: inline-flex;
    align-items: center;
    background: var(--surface-2);
    border: 1px solid var(--border-medium);
    color: var(--text-secondary);
    padding: 0.5rem 0.9rem;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
    transition: all var(--transition-base);
    cursor: default;
}

.skill-pill:hover {
    background: var(--surface-3);
    border-color: var(--accent-primary);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.skill-pill.matched {
    background: var(--success-bg);
    border-color: var(--success);
    color: var(--success);
}

.skill-pill.matched:hover {
    background: rgba(16, 185, 129, 0.2);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.skill-pill.missing {
    background: var(--danger-bg);
    border-color: var(--danger);
    color: var(--danger);
}

.skill-pill.missing:hover {
    background: rgba(239, 68, 68, 0.2);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM INFO CARDS
   ═══════════════════════════════════════════════════════════════ */
.premium-info-card {
    display: flex;
    align-items: flex-start;
    gap: var(--space-md);
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-primary);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin: var(--space-md) 0;
    backdrop-filter: blur(10px);
}

.premium-info-card.success {
    border-left-color: var(--success);
    background: var(--success-bg);
}

.premium-info-card.warning {
    border-left-color: var(--warning);
    background: var(--warning-bg);
}

.premium-info-card.danger {
    border-left-color: var(--danger);
    background: var(--danger-bg);
}

.info-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
}

.info-content {
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-secondary);
}

/* ═══════════════════════════════════════════════════════════════
   INTERVIEW QUESTION CARDS
   ═══════════════════════════════════════════════════════════════ */
.interview-question-card {
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    transition: all var(--transition-base);
}

.interview-question-card:hover {
    background: var(--surface-2);
    border-color: var(--border-medium);
    transform: translateX(4px);
}

.question-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}

.question-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: var(--accent-gradient);
    color: white;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 700;
}

.question-type {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-primary);
}

.question-text {
    font-size: 0.9rem;
    font-weight: 500;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: var(--space-md);
}

.question-hint {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-style: italic;
}

/* ═══════════════════════════════════════════════════════════════
   RECOMMENDATION CARDS
   ═══════════════════════════════════════════════════════════════ */
.recommendation-card {
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin: var(--space-md) 0;
    transition: all var(--transition-base);
}

.recommendation-card:hover {
    background: var(--surface-2);
    border-color: var(--border-medium);
}

.rec-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}

.rec-icon {
    font-size: 1.2rem;
}

.rec-title {
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-primary);
}

.rec-content {
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
}

.rec-item {
    display: flex;
    align-items: flex-start;
    gap: var(--space-sm);
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-secondary);
}

.rec-bullet {
    color: var(--accent-primary);
    font-weight: 700;
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════════════════════════
   PREMIUM SECTION HEADERS
   ═══════════════════════════════════════════════════════════════ */
.premium-section-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin: var(--space-xl) 0 var(--space-lg) 0;
}

.section-icon {
    font-size: 1.2rem;
}

.section-title {
    font-size: 0.9rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-primary);
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section-subtitle {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: var(--space-xs);
}

/* ═══════════════════════════════════════════════════════════════
   TWO COLUMN LAYOUT
   ═══════════════════════════════════════════════════════════════ */
.two-column-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-lg);
    margin: var(--space-lg) 0;
}

@media (max-width: 900px) {
    .two-column-layout {
        grid-template-columns: 1fr;
    }
}

.column-left, .column-right {
    background: var(--surface-1);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
}

/* ═══════════════════════════════════════════════════════════════
   STREAMLIT OVERRIDES
   ═══════════════════════════════════════════════════════════════ */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--surface-1) !important;
    backdrop-filter: blur(10px);
}

.stExpander {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    background: var(--surface-1) !important;
}

.stExpander > summary {
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}

.stDownloadButton > button {
    background: var(--surface-2) !important;
    border: 1px solid var(--border-medium) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    transition: all var(--transition-base) !important;
}

.stDownloadButton > button:hover {
    background: var(--surface-3) !important;
    border-color: var(--accent-primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-md) !important;
}

hr {
    border: 0 !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: var(--space-xl) 0 !important;
}

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE ADJUSTMENTS
   ═══════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .navbar-container {
        padding: 0 var(--space-md);
    }
    
    .content-wrapper {
        padding: 0 var(--space-md) var(--space-xl) var(--space-md);
    }
    
    .upload-grid {
        grid-template-columns: 1fr;
    }
    
    .navbar-subtitle {
        display: none;
    }
}

/* ═══════════════════════════════════════════════════════════════
   UTILITY CLASSES
   ═══════════════════════════════════════════════════════════════ */
.text-center {
    text-align: center;
}

.mb-sm { margin-bottom: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.mb-lg { margin-bottom: var(--space-lg); }
.mb-xl { margin-bottom: var(--space-xl); }

.mt-sm { margin-top: var(--space-sm); }
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
.mt-xl { margin-top: var(--space-xl); }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RENDER NAVBAR
# ═══════════════════════════════════════════════════════════════
render_navbar()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🚀 Quick Guide")
    st.markdown("""
    1. **Upload** your resume
    2. **Select** target role
    3. **Paste** job description (optional)
    4. **Click** Analyze
    """)
    
    st.markdown("---")
    
    st.markdown("### 📄 Supported Formats")
    st.markdown("**PDF** • **DOCX** • **TXT**")
    
    st.markdown("---")
    
    st.markdown("### ✨ Features")
    st.markdown("""
    ✓ ATS Score Analysis  
    ✓ Job Match Percentage  
    ✓ Skill Extraction  
    ✓ Missing Skills Detection  
    ✓ Interview Questions  
    ✓ AI-Powered Feedback  
    ✓ Downloadable Report
    """)
    
    st.markdown("---")
    
    with st.expander("⚙️ Developer Status", expanded=False):
        api_status = get_api_status()
        if api_status["api_available"]:
            st.success("✅ Groq AI Connected")
            st.caption(f"Provider: {api_status['provider']}")
        else:
            st.warning("⚠️ Using Fallback Mode")
            st.caption("Dynamic keyword analysis active")

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="premium-card card-compact mb-lg">
    <div style="text-align: center;">
        <h1 style="font-size: 1.8rem; font-weight: 800; margin: 0 0 0.5rem 0; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.02em;">
            Analyze Your Resume
        </h1>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin: 0;">
            Get instant AI-powered insights on ATS compatibility, job matching, and skill analysis
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload + Role Section
st.markdown('<div class="premium-card mb-lg">', unsafe_allow_html=True)
st.markdown('<div class="upload-grid">', unsafe_allow_html=True)

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown('<span class="field-label">📄 Resume Upload</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        file_size = round(uploaded_file.size / 1024, 1)
        st.success(f"✅ {uploaded_file.name} ({file_size} KB)")

with col2:
    st.markdown('<span class="field-label">🎯 Target Role</span>', unsafe_allow_html=True)
    role_options = list(ROLE_SKILLS.keys())
    selected_role = st.selectbox(
        "Select role",
        role_options,
        index=0,
        label_visibility="collapsed",
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Job Description Section
st.markdown('<div class="premium-card mb-lg">', unsafe_allow_html=True)
st.markdown('<span class="field-label">📋 Job Description <span style="color: var(--text-subtle); font-weight: 400; font-size: 0.65rem; margin-left: 0.3rem;">(Optional for better matching)</span></span>', unsafe_allow_html=True)
job_description = st.text_area(
    "Paste job description",
    height=110,
    placeholder="Paste the target job description here for precision AI-powered matching and analysis...",
    label_visibility="collapsed",
)

if not job_description.strip():
    if selected_role != "Custom":
        req_skills = ROLE_SKILLS.get(selected_role, [])
        render_info_card(
            f"ℹ️ Using <strong>{selected_role}</strong> role defaults: {', '.join(req_skills[:4])}...",
            card_type="info",
            icon="ℹ️"
        )
    else:
        render_info_card(
            "⚠️ Custom role selected. Please paste a job description for accurate analysis.",
            card_type="warning",
            icon="⚠️"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Analyze Button
st.markdown('<div class="button-container">', unsafe_allow_html=True)
analyze_btn = st.button("🚀 Run AI Analysis", key="analyze_main")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# RESULTS SECTION
# ═══════════════════════════════════════════════════════════════
if analyze_btn:
    if uploaded_file is None:
        st.error("❌ Please upload a resume (PDF, DOCX, or TXT)")
        st.stop()
    if selected_role == "Custom" and not job_description.strip():
        st.error("❌ For Custom role, please paste a job description")
        st.stop()

    with st.spinner("📄 Extracting resume text..."):
        try:
            resume_text = parse_resume(uploaded_file)
        except RuntimeError as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

    with st.spinner("🤖 Running AI analysis..."):
        result = analyze_resume(resume_text, job_description, selected_role)

    st.success("✅ Analysis complete!")
    st.markdown("---")

    # Get metrics
    match_pct = result.get("job_match_percentage", 0)
    ats_score = result.get("ats_score", 0)
    skills_found = len(result.get("extracted_skills", []))
    missing_count = len(result.get("missing_skills", []))

    def get_metric_type(val):
        if val >= 75:
            return "success"
        elif val >= 50:
            return "warning"
        else:
            return "danger"

    # Render Premium Metrics
    metrics_data = [
        {
            "value": f"{match_pct}%",
            "label": "Job Match",
            "type": get_metric_type(match_pct),
            "icon": "🎯"
        },
        {
            "value": ats_score,
            "label": "ATS Score",
            "type": get_metric_type(ats_score),
            "icon": "📊"
        },
        {
            "value": skills_found,
            "label": "Skills Found",
            "type": "info",
            "icon": "🧠"
        },
        {
            "value": missing_count,
            "label": "Missing Skills",
            "type": "danger" if missing_count > 5 else ("warning" if missing_count > 2 else "success"),
            "icon": "⚠️"
        }
    ]
    
    render_metrics_grid(metrics_data)

    # Progress Bars
    st.markdown('<div class="premium-card mb-lg">', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        render_progress_bar("Job Match", match_pct, 100, get_metric_type(match_pct))
    with col_p2:
        render_progress_bar("ATS Score", ats_score, 100, get_metric_type(ats_score))
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback
    feedback = get_ats_feedback(ats_score)
    render_info_card(feedback, card_type="info", icon="💡")

    st.markdown("---")

    # Premium Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Summary",
        "🧠 Skills",
        "🤖 ATS Report",
        "⚠️ Missing",
        "❓ Interview",
        "📄 Preview",
    ])

    with tab1:
        render_section_header("Candidate Profile", icon="👤")
        st.markdown(f'<div style="font-size: 0.9rem; line-height: 1.7; color: var(--text-secondary); margin-bottom: var(--space-xl);">{result.get("candidate_summary", "—")}</div>', unsafe_allow_html=True)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            strengths = result.get("strengths", [])
            if strengths:
                render_recommendation_card("Strengths", strengths, icon="✅")

        with col_s2:
            weaknesses = result.get("weaknesses", [])
            if weaknesses:
                render_recommendation_card("Areas to Improve", weaknesses, icon="⚠️")

        suggestions = result.get("improvement_suggestions", [])
        if suggestions:
            render_recommendation_card("Recommendations", suggestions, icon="💡")

        voice_text = result.get("voice_feedback_text", "")
        if voice_text:
            render_section_header("AI Feedback", icon="🤖")
            render_info_card(voice_text, card_type="info", icon="💬")

        if result.get("_model_used"):
            st.caption(f"✨ Powered by: `{result['_model_used']}`")

    with tab2:
        extracted_skills = result.get("extracted_skills", [])
        required_skills = ROLE_SKILLS.get(selected_role, [])
        if job_description.strip():
            required_skills = extract_job_skills(job_description) or required_skills

        matched_skills = [s for s in extracted_skills if s.lower() in {r.lower() for r in required_skills}]
        unmatched_skills = [s for s in extracted_skills if s.lower() not in {r.lower() for r in required_skills}]

        if matched_skills:
            render_section_header("Matched Skills", f"{len(matched_skills)} skills match the role", icon="✅")
            render_skill_section(matched_skills, badge_type="matched")
        else:
            render_info_card("No direct skill matches found with the job requirements.", card_type="warning", icon="⚠️")

        if extracted_skills:
            render_section_header("All Extracted Skills", f"{len(extracted_skills)} total skills found", icon="🧠")
            render_skill_section(extracted_skills, badge_type="default")
        else:
            render_info_card("No skills were extracted from the resume.", card_type="danger", icon="❌")

    with tab3:
        render_section_header("ATS Score Breakdown", "Detailed scoring analysis", icon="📊")
        
        req_skills_for_ats = ROLE_SKILLS.get(selected_role, [])
        _, ats_breakdown = calculate_ats_score(resume_text, job_description, req_skills_for_ats)

        max_scores = {
            "Contact Information": 10,
            "Skills Section": 20,
            "Education": 15,
            "Experience/Projects": 20,
            "Keyword Match": 25,
            "Readability/Formatting": 10,
        }

        for category, score in ats_breakdown.items():
            max_s = max_scores.get(category, 10)
            pct = (score / max_s) if max_s > 0 else 0
            color = "success" if pct >= 0.7 else ("warning" if pct >= 0.4 else "danger")
            render_progress_bar(category, score, max_s, color)

        st.markdown("---")
        st.markdown(f'<div style="text-align: center; font-size: 1.2rem; font-weight: 700; color: var(--text-primary);">Total Score: <span style="background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{ats_score}/100</span></div>', unsafe_allow_html=True)

    with tab4:
        missing_skills = result.get("missing_skills", [])
        
        if missing_skills:
            render_section_header("Skills to Add", f"{len(missing_skills)} skills recommended", icon="⚠️")
            render_skill_section(missing_skills, badge_type="missing")
            
            st.markdown("---")
            render_section_header("Learning Resources", "Curated learning paths", icon="📚")
            
            for skill in missing_skills[:5]:
                query = skill.replace(" ", "+")
                st.markdown(f"""
                <div class="premium-card card-compact mb-sm">
                    <div style="font-weight: 700; margin-bottom: 0.5rem; color: var(--text-primary);">{skill}</div>
                    <div style="display: flex; gap: 1rem; font-size: 0.8rem;">
                        <a href="https://youtube.com/results?search_query={query}+tutorial" target="_blank" style="color: var(--accent-primary); text-decoration: none;">📺 YouTube</a>
                        <a href="https://coursera.org/search?query={query}" target="_blank" style="color: var(--accent-primary); text-decoration: none;">🎓 Coursera</a>
                        <a href="https://google.com/search?q={query}+official+docs" target="_blank" style="color: var(--accent-primary); text-decoration: none;">📖 Docs</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            render_info_card("🎉 Excellent! You have all the key skills for this role.", card_type="success", icon="🎉")

    with tab5:
        render_section_header("Interview Preparation", "Practice these questions", icon="❓")
        questions = result.get("interview_questions", [])

        q_types = ["💻 Technical", "🔬 Advanced", "🗂️ Project", "📖 Gap", "🤝 Behavioral"]
        
        questions_html = ""
        for i, question in enumerate(questions):
            q_type = q_types[i] if i < len(q_types) else f"Q{i+1}"
            questions_html += render_interview_question(question, i, q_type)
        
        st.markdown(questions_html, unsafe_allow_html=True)

    with tab6:
        render_section_header("Resume Text Preview", "Extracted content", icon="📄")
        st.caption(f"**{len(resume_text.split())} words** • {len(resume_text)} characters")
        st.text_area(
            "Extracted Text:",
            value=resume_text,
            height=350,
            label_visibility="collapsed",
        )

    # Download Section
    st.markdown("---")
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    render_section_header("Download Report", "Export your analysis", icon="📥")

    report_lines = [
        "=" * 70,
        "AI RESUME ANALYZER — ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Role: {selected_role}",
        "=" * 70,
        "",
        "SUMMARY",
        "-" * 70,
        result.get("candidate_summary", "—"),
        "",
        "METRICS",
        "-" * 70,
        f"Job Match: {match_pct}%",
        f"ATS Score: {ats_score}/100",
        f"Skills Found: {skills_found}",
        f"Missing Skills: {missing_count}",
        "",
        "EXTRACTED SKILLS",
        "-" * 70,
        ", ".join(result.get("extracted_skills", [])) or "None",
        "",
        "STRENGTHS",
        "-" * 70,
        *[f"• {s}" for s in result.get("strengths", [])],
        "",
        "AREAS TO IMPROVE",
        "-" * 70,
        *[f"• {w}" for w in result.get("weaknesses", [])],
        "",
        "MISSING SKILLS",
        "-" * 70,
        ", ".join(result.get("missing_skills", [])) or "None",
        "",
        "RECOMMENDATIONS",
        "-" * 70,
        *[f"{i+1}. {s}" for i, s in enumerate(result.get("improvement_suggestions", []))],
        "",
        "=" * 70,
    ]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="📥 Download Analysis Report",
        data=report_text,
        file_name=f"resume_analysis_{selected_role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    render_info_card(
        "📌 All scores and insights are based on your actual resume content. Results may vary based on resume quality and job description specificity.",
        card_type="info",
        icon="ℹ️"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: var(--text-subtle); font-size: 0.75rem; padding: var(--space-xl) 0; margin-top: var(--space-2xl);">
    ✨ AI Resume Analyzer — Built with Streamlit + Groq AI<br>
    <span style="font-size: 0.7rem; opacity: 0.7;">Premium AI SaaS Dashboard Experience</span>
</div>
""", unsafe_allow_html=True)
