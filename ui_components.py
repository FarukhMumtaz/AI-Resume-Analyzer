"""
ui_components.py — Premium UI Components for AI Resume Analyzer
Modular, reusable components for a handcrafted SaaS dashboard experience
"""

import streamlit as st
from typing import List, Dict, Any


def render_navbar():
    """Render premium top navbar with glassmorphism"""
    st.markdown("""
    <div class="premium-navbar">
        <div class="navbar-container">
            <div class="navbar-left">
                <div class="navbar-icon">✨</div>
                <div class="navbar-text">
                    <div class="navbar-title">AI Resume Analyzer</div>
                    <div class="navbar-subtitle">Smart ATS & Job Match Assistant</div>
                </div>
            </div>
            <div class="navbar-right">
                <div class="status-pill">
                    <span class="status-dot"></span>
                    <span>Ready to Analyze</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(value: Any, label: str, card_type: str = "primary", icon: str = "📊"):
    """Render a single premium metric card with glassmorphism"""
    return f"""
    <div class="premium-metric-card {card_type}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-content">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        <div class="metric-glow"></div>
    </div>
    """


def render_metrics_grid(metrics: List[Dict[str, Any]]):
    """Render grid of premium metric cards"""
    cards_html = ""
    for metric in metrics:
        cards_html += render_metric_card(
            value=metric.get("value", "—"),
            label=metric.get("label", ""),
            card_type=metric.get("type", "primary"),
            icon=metric.get("icon", "📊")
        )
    
    st.markdown(f"""
    <div class="metrics-grid">
        {cards_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "", icon: str = ""):
    """Render premium section header"""
    subtitle_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    icon_html = f'<span class="section-icon">{icon}</span>' if icon else ""
    
    st.markdown(f"""
    <div class="premium-section-header">
        {icon_html}
        <div>
            <div class="section-title">{title}</div>
            {subtitle_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_skill_badge(skill: str, badge_type: str = "default"):
    """Render a single skill badge"""
    return f'<span class="skill-pill {badge_type}">{skill}</span>'


def render_skill_section(skills: List[str], title: str = "", badge_type: str = "default"):
    """Render a section of skill badges"""
    if not skills:
        return
    
    badges_html = "".join([render_skill_badge(skill, badge_type) for skill in skills])
    
    title_html = f'<div class="skill-section-title">{title}</div>' if title else ""
    
    st.markdown(f"""
    <div class="skill-section">
        {title_html}
        <div class="skill-pills-container">
            {badges_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(label: str, value: int, max_value: int = 100, color: str = "primary"):
    """Render premium animated progress bar"""
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    st.markdown(f"""
    <div class="premium-progress-container">
        <div class="progress-header">
            <span class="progress-label">{label}</span>
            <span class="progress-value">{value}/{max_value}</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill {color}" style="width: {percentage}%">
                <div class="progress-shine"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_info_card(content: str, card_type: str = "info", icon: str = "ℹ️"):
    """Render premium info/feedback card"""
    st.markdown(f"""
    <div class="premium-info-card {card_type}">
        <div class="info-icon">{icon}</div>
        <div class="info-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_interview_question(question: str, index: int, question_type: str = ""):
    """Render premium interview question card"""
    type_label = f'<span class="question-type">{question_type}</span>' if question_type else ""
    
    return f"""
    <div class="interview-question-card">
        <div class="question-header">
            <span class="question-number">Q{index + 1}</span>
            {type_label}
        </div>
        <div class="question-text">{question}</div>
        <div class="question-hint">💡 Use STAR method: Situation → Task → Action → Result</div>
    </div>
    """


def render_recommendation_card(title: str, items: List[str], icon: str = "✨"):
    """Render premium recommendation card"""
    items_html = "".join([f'<div class="rec-item"><span class="rec-bullet">•</span>{item}</div>' for item in items])
    
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="rec-header">
            <span class="rec-icon">{icon}</span>
            <span class="rec-title">{title}</span>
        </div>
        <div class="rec-content">
            {items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_two_column_layout(left_content: str, right_content: str):
    """Render premium two-column responsive layout"""
    st.markdown(f"""
    <div class="two-column-layout">
        <div class="column-left">
            {left_content}
        </div>
        <div class="column-right">
            {right_content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_upload_success(filename: str, filesize: float):
    """Render premium upload success state"""
    st.markdown(f"""
    <div class="upload-success">
        <div class="success-icon">✓</div>
        <div class="success-content">
            <div class="success-filename">{filename}</div>
            <div class="success-size">{filesize} KB</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(message: str, icon: str = "📄"):
    """Render premium empty state"""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">{icon}</div>
        <div class="empty-message">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(label: str, value: str, trend: str = "", icon: str = ""):
    """Render premium stat card for dashboard"""
    trend_html = f'<div class="stat-trend">{trend}</div>' if trend else ""
    icon_html = f'<div class="stat-icon">{icon}</div>' if icon else ""
    
    return f"""
    <div class="stat-card">
        {icon_html}
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
        {trend_html}
    </div>
    """
