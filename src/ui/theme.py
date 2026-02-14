"""
Centralized theme and styling configuration for the QR Generator UI.
Provides consistent colors, fonts, and styling across all UI components.
"""

# Color Palette - Flat, Modern Design
COLORS = {
    'primary': '#2563eb',           # Blue accent
    'primary_hover': '#1d4ed8',     # Darker blue for hover
    'background': '#ffffff',         # White background (light mode)
    'background_dark': '#1e1e1e',    # Dark background (dark mode)
    'surface': '#f8fafc',            # Light gray surface
    'surface_dark': '#2d2d2d',       # Dark surface
    'border': '#e2e8f0',             # Subtle border
    'border_dark': '#404040',        # Dark border
    'text': '#1e293b',               # Primary text
    'text_dark': '#e5e7eb',          # Dark mode text
    'text_secondary': '#64748b',     # Secondary text
    'disabled': '#cbd5e1',           # Disabled state
    'success': '#10b981',            # Success green
    'error': '#ef4444',              # Error red
}

# Typography
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 20, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11),
    'small': ('Segoe UI', 10),
    'button': ('Segoe UI', 11),
}

# Spacing System (8px base)
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 20,
    'xxl': 24,
}

# Widget Configurations
WIDGET_STYLE = {
    'button_height': 40,
    'button_padding': (16, 8),
    'input_height': 36,
    'border_width': 1,
    'border_radius': 4,  # Subtle, not exaggerated
}

# ttkbootstrap theme name
TTK_THEME = 'flatly'  # Modern flat theme
TTK_THEME_DARK = 'darkly'  # Dark mode equivalent