# password_strength_checker.py - Enhanced UI/UX Version
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib
import re
import json
import secrets
import string
from datetime import datetime
import logging
import os

class ModernPasswordChecker:
    def __init__(self, root, role, username, auth_system=None):
        self.root = root
        self.role = role
        self.username = username
        self.auth_system = auth_system
        self.session_start = datetime.now()
        self.passwords_analyzed = 0
        self.setup_modern_gui()
        self.setup_logging()
        self.load_common_passwords()
        
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient_canvas(self, parent, width, height, color1, color2):
        """Create a gradient background canvas"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        
        for i in range(height):
            ratio = i / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)
        
        return canvas
    
    def create_glass_frame(self, parent, **kwargs):
        """Create a glassmorphism-style frame"""
        frame = tk.Frame(parent, bg='#ffffff', **kwargs)
        frame.configure(highlightbackground='#e0e7ff', highlightthickness=2)
        return frame
    
    def create_hover_button(self, parent, text, command, bg_color, hover_color, **kwargs):
        """Create a button with smooth hover effect"""
        btn = tk.Button(parent, text=text, command=command, bg=bg_color, 
                       relief='flat', cursor='hand2', **kwargs)
        
        def on_enter(e):
            btn.configure(bg=hover_color)
        
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
        
    def setup_modern_gui(self):
        """Setup ultra-modern GUI with glassmorphism and animations"""
        self.root.title(f"🔐 Password Analyzer Pro - {self.role.title()} Mode")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        self.center_window(1000, 800)
        
        # Gradient background
        bg_canvas = self.create_gradient_canvas(self.root, 1000, 800, '#667eea', '#764ba2')
        bg_canvas.place(x=0, y=0)
        
        # Main container with glass effect
        main_container = tk.Frame(self.root, bg='white')
        main_container.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.95, relheight=0.95)
        
        # Header Section with modern design
        header_frame = tk.Frame(main_container, bg='white', height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Create gradient header background
        header_canvas = self.create_gradient_canvas(header_frame, 1000, 100, '#667eea', '#764ba2')
        header_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#667eea')
        header_content.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.95)
        
        # Left side - App branding
        left_header = tk.Frame(header_content, bg='#667eea')
        left_header.pack(side=tk.LEFT)
        
        # Logo
        logo_canvas = tk.Canvas(left_header, width=50, height=50, bg='#667eea', highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
        logo_canvas.create_oval(2, 2, 48, 48, fill='#ffffff', outline='#ffd700', width=3)
        logo_canvas.create_text(25, 25, text="🔒", font=('Arial', 20))
        
        title_frame = tk.Frame(left_header, bg='#667eea')
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="Password Analyzer Pro", 
                font=('Segoe UI', 18, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        
        tk.Label(title_frame, text="Enterprise Security Suite", 
                font=('Segoe UI', 9), bg='#667eea', fg='#e0e7ff').pack(anchor='w')
        
        # Right side - User info card with modern design
        right_header = tk.Frame(header_content, bg='#667eea')
        right_header.pack(side=tk.RIGHT)
        
        user_card = tk.Frame(right_header, bg='white', 
                           highlightbackground='white', highlightthickness=2)
        user_card.pack(side=tk.LEFT, padx=(0, 10))
        
        user_inner = tk.Frame(user_card, bg='#667eea', padx=15, pady=8)
        user_inner.pack()
        
        # User icon
        user_icon_canvas = tk.Canvas(user_inner, width=30, height=30, bg='#667eea', highlightthickness=0)
        user_icon_canvas.pack(side=tk.LEFT, padx=(0, 10))
        user_icon_canvas.create_oval(2, 2, 28, 28, fill='#ffd700', outline='white', width=2)
        user_icon_canvas.create_text(15, 15, text="👤", font=('Arial', 12))
        
        user_info_frame = tk.Frame(user_inner, bg='#667eea')
        user_info_frame.pack(side=tk.LEFT)
        
        tk.Label(user_info_frame, text=f"{self.username}", 
                font=('Segoe UI', 10, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        
        role_color = '#ffd700' if self.role == 'admin' else '#90EE90'
        tk.Label(user_info_frame, text=f"● {self.role.upper()}", 
                font=('Segoe UI', 8, 'bold'), bg='#667eea', fg=role_color).pack(anchor='w')
        
        # Logout button with modern styling
        logout_btn = self.create_hover_button(
            right_header, "🚪 Logout", self.logout,
            '#e53e3e', '#c53030', font=('Segoe UI', 9, 'bold'),
            fg='white', padx=20, pady=8
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Content area with tabs
        content_frame = tk.Frame(main_container, bg='#f7fafc')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create modern notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TNotebook', background='#f7fafc', borderwidth=0)
        style.configure('Modern.TNotebook.Tab', padding=[20, 10], 
                       font=('Segoe UI', 10, 'bold'), background='#e2e8f0')
        style.map('Modern.TNotebook.Tab', 
                 background=[('selected', '#667eea')],
                 foreground=[('selected', 'white'), ('!selected', '#2d3748')])
        
        self.notebook = ttk.Notebook(content_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Setup tabs
        self.setup_analysis_tab()
        self.setup_dashboard_tab()
        self.setup_profile_tab()
        
        # Modern status bar
        self.setup_status_bar(main_container)
        
    def setup_analysis_tab(self):
        """Setup password analysis tab with stunning UI"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="🔍 Password Analysis")
        
        # Scrollable canvas for content
        canvas = tk.Canvas(analysis_frame, bg='#f7fafc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f7fafc')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main content container
        content = tk.Frame(scrollable_frame, bg='#f7fafc', padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Password Input Card with premium design
        input_card = self.create_glass_frame(content)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        input_inner = tk.Frame(input_card, bg='white', padx=30, pady=25)
        input_inner.pack(fill=tk.BOTH)
        
        # Card header
        card_header = tk.Frame(input_inner, bg='white')
        card_header.pack(fill=tk.X, pady=(0, 20))
        
        header_icon_canvas = tk.Canvas(card_header, width=40, height=40, bg='white', highlightthickness=0)
        header_icon_canvas.pack(side=tk.LEFT)
        header_icon_canvas.create_oval(2, 2, 38, 38, fill='#667eea', outline='#764ba2', width=2)
        header_icon_canvas.create_text(20, 20, text="🔐", font=('Arial', 16))
        
        header_text = tk.Frame(card_header, bg='white')
        header_text.pack(side=tk.LEFT, padx=(12, 0))
        
        tk.Label(header_text, text="Password Security Analysis", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg='#2d3748').pack(anchor='w')
        
        tk.Label(header_text, text="Enter your password for comprehensive security assessment", 
                font=('Segoe UI', 9), bg='white', fg='#718096').pack(anchor='w')
        
        # Password entry field with modern design
        entry_container = tk.Frame(input_inner, bg='white')
        entry_container.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(entry_container, text="Password", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 8))
        
        entry_frame = tk.Frame(entry_container, bg='white')
        entry_frame.pack(fill=tk.X)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(entry_frame, textvariable=self.password_var, 
                                      font=('Segoe UI', 13), show="●", bg='#f7fafc',
                                      relief='flat', highlightbackground='#cbd5e0', 
                                      highlightthickness=2, highlightcolor='#667eea')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
        self.password_entry.bind('<KeyRelease>', self.real_time_check)
        
        # Show/Hide password toggle
        self.show_password = tk.BooleanVar()
        eye_btn = tk.Checkbutton(entry_frame, text="👁", variable=self.show_password,
                                command=self.toggle_password_visibility,
                                bg='white', font=('Arial', 14), relief='flat', 
                                cursor='hand2', selectcolor='white')
        eye_btn.pack(side=tk.RIGHT)
        
        # Strength meter with animated gradient
        strength_container = tk.Frame(input_inner, bg='white')
        strength_container.pack(fill=tk.X, pady=(10, 20))
        
        strength_header = tk.Frame(strength_container, bg='white')
        strength_header.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(strength_header, text="Password Strength:", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg='#2d3748').pack(side=tk.LEFT)
        
        self.strength_var = tk.StringVar(value="Not analyzed yet")
        self.strength_label = tk.Label(strength_header, textvariable=self.strength_var,
                                      font=('Segoe UI', 10, 'bold'), bg='white', fg='#718096')
        self.strength_label.pack(side=tk.RIGHT)
        
        # Custom progress bar with gradient
        progress_bg = tk.Frame(strength_container, bg='#e2e8f0', height=12)
        progress_bg.pack(fill=tk.X)
        
        self.progress_canvas = tk.Canvas(progress_bg, height=12, bg='#e2e8f0', 
                                        highlightthickness=0)
        self.progress_canvas.pack(fill=tk.BOTH)
        
        # Create progress bar rectangle
        self.progress_rect = self.progress_canvas.create_rectangle(
            0, 0, 0, 12, fill='#48bb78', outline=''
        )
        
        # Action buttons with modern styling
        button_container = tk.Frame(input_inner, bg='white')
        button_container.pack(fill=tk.X)
        
        analyze_btn = self.create_hover_button(
            button_container, "🔍 Analyze Password", self.check_password,
            '#667eea', '#5a67d8', font=('Segoe UI', 11, 'bold'),
            fg='white', padx=25, pady=12
        )
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = self.create_hover_button(
            button_container, "🎲 Generate Strong Password", self.generate_password,
            '#48bb78', '#38a169', font=('Segoe UI', 11, 'bold'),
            fg='white', padx=25, pady=12
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = self.create_hover_button(
            button_container, "🗑️ Clear", self.clear_analysis,
            '#718096', '#4a5568', font=('Segoe UI', 10),
            fg='white', padx=20, pady=12
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Results Card with beautiful design
        results_card = self.create_glass_frame(content)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        results_inner = tk.Frame(results_card, bg='white', padx=30, pady=25)
        results_inner.pack(fill=tk.BOTH, expand=True)
        
        # Results header
        results_header = tk.Frame(results_inner, bg='white')
        results_header.pack(fill=tk.X, pady=(0, 15))
        
        results_icon_canvas = tk.Canvas(results_header, width=35, height=35, bg='white', highlightthickness=0)
        results_icon_canvas.pack(side=tk.LEFT)
        results_icon_canvas.create_oval(2, 2, 33, 33, fill='#ed8936', outline='#dd6b20', width=2)
        results_icon_canvas.create_text(17, 17, text="📊", font=('Arial', 14))
        
        tk.Label(results_header, text="Security Analysis Results", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg='#2d3748').pack(side=tk.LEFT, padx=(10, 0))
        
        # Results display with syntax highlighting
        self.results_text = scrolledtext.ScrolledText(
            results_inner, font=('Consolas', 10), bg='#1a202c', fg='#e2e8f0',
            relief='flat', wrap=tk.WORD, padx=15, pady=15,
            highlightbackground='#4a5568', highlightthickness=2
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.results_text.tag_config('header', foreground='#63b3ed', font=('Consolas', 11, 'bold'))
        self.results_text.tag_config('success', foreground='#68d391')
        self.results_text.tag_config('warning', foreground='#fbd38d')
        self.results_text.tag_config('error', foreground='#fc8181')
        self.results_text.tag_config('info', foreground='#b794f4')
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_dashboard_tab(self):
        """Setup security dashboard with modern cards"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Security Dashboard")
        
        content = tk.Frame(dashboard_frame, bg='#f7fafc', padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard header
        header = tk.Frame(content, bg='#f7fafc')
        header.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(header, text="Security Dashboard", 
                font=('Segoe UI', 20, 'bold'), bg='#f7fafc', fg='#2d3748').pack(anchor='w')
        
        tk.Label(header, text="Comprehensive security features and metrics", 
                font=('Segoe UI', 10), bg='#f7fafc', fg='#718096').pack(anchor='w', pady=(5, 0))
        
        # Stats cards at top
        stats_row = tk.Frame(content, bg='#f7fafc')
        stats_row.pack(fill=tk.X, pady=(0, 20))
        
        # Stat card 1
        stat1 = self.create_stat_card(stats_row, "🔐", "Passwords Analyzed", 
                                     str(self.passwords_analyzed), '#667eea')
        stat1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Stat card 2
        duration = datetime.now() - self.session_start
        minutes = int(duration.total_seconds() / 60)
        stat2 = self.create_stat_card(stats_row, "⏱️", "Session Duration", 
                                     f"{minutes} min", '#48bb78')
        stat2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Stat card 3
        stat3 = self.create_stat_card(stats_row, "👤", "User Role", 
                                     self.role.upper(), '#ed8936')
        stat3.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Feature cards
        features = [
            ("🔒 Password Entropy", "Measures randomness and unpredictability", '#667eea'),
            ("🛡️ Common Password Check", "Compares against known weak passwords", '#48bb78'),
            ("📊 Pattern Analysis", "Detects sequential or repeated patterns", '#ed8936'),
            ("⚡ Real-time Feedback", "Instant strength assessment as you type", '#ecc94b'),
            ("🔐 Hash Verification", "SHA-256 secure password hashing", '#9f7aea'),
            ("📈 Strength Scoring", "Comprehensive security scoring system", '#38b2ac'),
        ]
        
        for title, desc, color in features:
            card = self.create_feature_card(content, title, desc, color)
            card.pack(fill=tk.X, pady=(0, 12))
            
    def create_stat_card(self, parent, icon, title, value, color):
        """Create a stat card with icon"""
        card = self.create_glass_frame(parent)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)
        
        # Icon
        icon_canvas = tk.Canvas(inner, width=45, height=45, bg='white', highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(2, 2, 43, 43, fill=color, outline='')
        icon_canvas.create_text(22, 22, text=icon, font=('Arial', 18))
        
        # Value
        tk.Label(inner, text=value, font=('Segoe UI', 20, 'bold'), 
                bg='white', fg='#2d3748').pack(pady=(10, 2))
        
        # Title
        tk.Label(inner, text=title, font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack()
        
        return card
        
    def create_feature_card(self, parent, title, description, accent_color):
        """Create a feature card"""
        card = self.create_glass_frame(parent)
        
        inner = tk.Frame(card, bg='white', padx=25, pady=18)
        inner.pack(fill=tk.BOTH)
        
        # Left accent bar
        accent = tk.Frame(inner, bg=accent_color, width=4)
        accent.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Content
        content = tk.Frame(inner, bg='white')
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(content, text=title, font=('Segoe UI', 12, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w')
        
        tk.Label(content, text=description, font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack(anchor='w', pady=(3, 0))
        
        return card
        
    def setup_profile_tab(self):
        """Setup user profile tab"""
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="👤 User Profile")
        
        content = tk.Frame(profile_frame, bg='#f7fafc', padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Profile header
        header = tk.Frame(content, bg='#f7fafc')
        header.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(header, text="User Profile", 
                font=('Segoe UI', 20, 'bold'), bg='#f7fafc', fg='#2d3748').pack(anchor='w')
        
        tk.Label(header, text="Manage your account and session information", 
                font=('Segoe UI', 10), bg='#f7fafc', fg='#718096').pack(anchor='w', pady=(5, 0))
        
        # Profile card
        profile_card = self.create_glass_frame(content)
        profile_card.pack(fill=tk.BOTH, expand=True)
        
        profile_inner = tk.Frame(profile_card, bg='white', padx=30, pady=30)
        profile_inner.pack(fill=tk.BOTH, expand=True)
        
        # User avatar and basic info
        avatar_section = tk.Frame(profile_inner, bg='white')
        avatar_section.pack(fill=tk.X, pady=(0, 25))
        
        # Avatar
        avatar_canvas = tk.Canvas(avatar_section, width=80, height=80, bg='white', highlightthickness=0)
        avatar_canvas.pack(side=tk.LEFT, padx=(0, 20))
        avatar_canvas.create_oval(5, 5, 75, 75, fill='#667eea', outline='#764ba2', width=3)
        avatar_canvas.create_text(40, 40, text="👤", font=('Arial', 35))
        
        # User details
        details_frame = tk.Frame(avatar_section, bg='white')
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(details_frame, text=self.username, 
                font=('Segoe UI', 18, 'bold'), bg='white', fg='#2d3748').pack(anchor='w')
        
        role_color = '#e53e3e' if self.role == 'admin' else '#38a169'
        tk.Label(details_frame, text=f"● {self.role.upper()} ACCESS", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg=role_color).pack(anchor='w', pady=(5, 0))
        
        # Divider
        tk.Frame(profile_inner, bg='#e2e8f0', height=1).pack(fill=tk.X, pady=(0, 25))
        
        # Information grid
        info_items = [
            ("👤 Username", self.username),
            ("🎯 Role", self.role.upper()),
            ("🆔 User ID", f"UID_{hash(self.username) % 10000:04d}"),
            ("📧 Email", "dragneeldtensa@gmail.com"),
            ("🕐 Session Started", self.session_start.strftime('%Y-%m-%d %H:%M:%S')),
            ("🔐 2FA Status", "✅ Enabled"),
            ("📊 Passwords Analyzed", str(self.passwords_analyzed)),
            ("🔒 Security Level", "High")
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = tk.Frame(profile_inner, bg='white')
            row.pack(fill=tk.X, pady=(0, 12))
            
            tk.Label(row, text=label, font=('Segoe UI', 10, 'bold'), 
                   bg='white', fg='#2d3748', width=20, anchor='w').pack(side=tk.LEFT)
            
            tk.Label(row, text=value, font=('Segoe UI', 10), 
                   bg='white', fg='#718096').pack(side=tk.LEFT, padx=(10, 0))
        
        # Action buttons
        action_frame = tk.Frame(profile_inner, bg='white')
        action_frame.pack(fill=tk.X, pady=(20, 0))
        
        logout_btn = self.create_hover_button(
            action_frame, "🚪 Logout", self.logout,
            '#e53e3e', '#c53030', font=('Segoe UI', 11, 'bold'),
            fg='white', padx=25, pady=12
        )
        logout_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        change_pwd_btn = self.create_hover_button(
            action_frame, "🔒 Change Password", self.change_password,
            '#667eea', '#5a67d8', font=('Segoe UI', 11, 'bold'),
            fg='white', padx=25, pady=12
        )
        change_pwd_btn.pack(side=tk.LEFT)
        
    def setup_status_bar(self, parent):
        """Setup modern status bar"""
        status_frame = tk.Frame(parent, bg='#2d3748', height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        status_inner = tk.Frame(status_frame, bg='#2d3748')
        status_inner.pack(fill=tk.BOTH, padx=15)
        
        # Left side - Status message
        self.status_var = tk.StringVar(value=f"🔒 Ready • User: {self.username}")
        status_label = tk.Label(status_inner, textvariable=self.status_var,
                              font=('Segoe UI', 9), bg='#2d3748', fg='white')
        status_label.pack(side=tk.LEFT, pady=8)
        
        # Right side - Session timer
        self.session_timer_var = tk.StringVar(value="⏱️ 00:00:00")
        timer_label = tk.Label(status_inner, textvariable=self.session_timer_var,
                             font=('Segoe UI', 9), bg='#2d3748', fg='#cbd5e0')
        timer_label.pack(side=tk.RIGHT, pady=8)
        
        self.start_session_timer()
        
    def start_session_timer(self):
        """Update session timer"""
        session_duration = datetime.now() - self.session_start
        hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.session_timer_var.set(f"⏱️ {hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.start_session_timer)
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
            
    def setup_logging(self):
        # Get the script directory to save logs there
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(script_dir, 'app_audit.log')
        
        # Only configure if not already configured
        if not logging.getLogger().handlers:
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
        logging.info(f"Password Strength Checker started for user: {self.username}")
        
    def load_common_passwords(self):
        self.common_passwords = {
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', '1234567890', 'abc123'
        }
        
    def calculate_entropy(self, password):
        char_sets = 0
        if re.search(r'[a-z]', password):
            char_sets += 26
        if re.search(r'[A-Z]', password):
            char_sets += 26
        if re.search(r'[0-9]', password):
            char_sets += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            char_sets += 32
            
        entropy = len(password) * (char_sets.bit_length() if char_sets > 0 else 1)
        return entropy
        
    def check_common_password(self, password):
        return password.lower() in self.common_passwords
        
    def check_patterns(self, password):
        patterns = [
            (r'^[0-9]+$', 'Only numbers'),
            (r'^[a-zA-Z]+$', 'Only letters'),
            (r'(.)\1{2,}', 'Repeated characters'),
            (r'(123|abc|qwerty)', 'Common sequences')
        ]
        
        issues = []
        for pattern, message in patterns:
            if re.search(pattern, password.lower()):
                issues.append(message)
        return issues
        
    def update_progress_bar(self, value):
        """Update animated progress bar"""
        width = self.progress_canvas.winfo_width()
        if width <= 1:
            width = 400
        
        bar_width = (value / 100) * width
        
        # Determine color based on strength
        if value < 30:
            color = '#fc8181'
        elif value < 70:
            color = '#fbd38d'
        else:
            color = '#68d391'
        
        # Animate progress bar
        self.progress_canvas.coords(self.progress_rect, 0, 0, bar_width, 12)
        self.progress_canvas.itemconfig(self.progress_rect, fill=color)
        
    def real_time_check(self, event=None):
        password = self.password_var.get()
        if not password:
            self.update_progress_bar(0)
            self.strength_var.set("Not analyzed yet")
            self.strength_label.config(fg='#718096')
            self.status_var.set(f"🔒 Ready • User: {self.username}")
            return
            
        entropy = self.calculate_entropy(password)
        strength_score = min(entropy / 2, 100)
        
        self.update_progress_bar(strength_score)
        
        if strength_score < 30:
            self.strength_var.set("❌ Weak")
            self.strength_label.config(fg='#e53e3e')
            self.status_var.set("⚠️ Password is weak - consider improving")
        elif strength_score < 70:
            self.strength_var.set("⚠️ Medium")
            self.strength_label.config(fg='#ed8936')
            self.status_var.set("🔍 Password is acceptable but could be stronger")
        else:
            self.strength_var.set("✅ Strong")
            self.strength_label.config(fg='#38a169')
            self.status_var.set("✅ Password strength is excellent!")
            
    def clear_analysis(self):
        """Clear all analysis"""
        self.password_var.set("")
        self.results_text.delete(1.0, tk.END)
        self.update_progress_bar(0)
        self.strength_var.set("Not analyzed yet")
        self.strength_label.config(fg='#718096')
        self.status_var.set(f"🔒 Ready • User: {self.username}")
        
    def check_password(self):
        password = self.password_var.get()
        
        if not password:
            messagebox.showwarning("Input Required", "🔍 Please enter a password to analyze.")
            return
        
        self.passwords_analyzed += 1
        self.results_text.delete(1.0, tk.END)
        
        # Header
        self.results_text.insert(tk.END, "🔒 COMPREHENSIVE PASSWORD ANALYSIS\n", 'header')
        self.results_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Basic metrics
        length = len(password)
        entropy = self.calculate_entropy(password)
        
        self.results_text.insert(tk.END, "📏 LENGTH ANALYSIS:\n", 'info')
        self.results_text.insert(tk.END, f"   • Password length: {length} characters\n")
        self.results_text.insert(tk.END, f"   • Entropy score: {entropy} bits\n\n")
        
        # Character composition
        self.results_text.insert(tk.END, "🔤 CHARACTER COMPOSITION:\n", 'info')
        checks = [
            ('Lowercase letters (a-z)', r'[a-z]'),
            ('Uppercase letters (A-Z)', r'[A-Z]'),
            ('Numbers (0-9)', r'[0-9]'),
            ('Special characters', r'[^a-zA-Z0-9]')
        ]
        
        for check_name, pattern in checks:
            if re.search(pattern, password):
                self.results_text.insert(tk.END, f"   ✅ Contains {check_name}\n", 'success')
            else:
                self.results_text.insert(tk.END, f"   ❌ Missing {check_name}\n", 'error')
        
        self.results_text.insert(tk.END, "\n")
        
        # Security checks
        self.results_text.insert(tk.END, "🛡️ SECURITY CHECKS:\n", 'info')
        
        if self.check_common_password(password):
            self.results_text.insert(tk.END, "   ❌ WARNING: This is a commonly used password!\n", 'error')
        else:
            self.results_text.insert(tk.END, "   ✅ Not found in common password database\n", 'success')
            
        pattern_issues = self.check_patterns(password)
        if pattern_issues:
            self.results_text.insert(tk.END, "   ⚠️  Weak patterns detected:\n", 'warning')
            for issue in pattern_issues:
                self.results_text.insert(tk.END, f"     • {issue}\n", 'warning')
        else:
            self.results_text.insert(tk.END, "   ✅ No weak patterns detected\n", 'success')
            
        # Hash
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        self.results_text.insert(tk.END, "\n🔐 SECURITY HASH:\n", 'info')
        self.results_text.insert(tk.END, f"   SHA-256: {hash_value}\n")
        
        # Recommendation
        self.results_text.insert(tk.END, "\n💡 RECOMMENDATION:\n", 'info')
        if entropy < 50:
            self.results_text.insert(tk.END, "   ❌ This password is weak. Use a longer password\n", 'error')
            self.results_text.insert(tk.END, "   with mixed character types.\n", 'error')
        elif entropy < 80:
            self.results_text.insert(tk.END, "   ⚠️  Password is acceptable but could be stronger.\n", 'warning')
            self.results_text.insert(tk.END, "   Add more special characters or increase length.\n", 'warning')
        else:
            self.results_text.insert(tk.END, "   ✅ Excellent password strength! Good job!\n", 'success')
            
        logging.info(f"User {self.username} analyzed password: {length} chars, entropy: {entropy}")
        self.status_var.set(f"✅ Analysis complete • {self.passwords_analyzed} total analyzed")
        
    def generate_password(self):
        """Generate strong password"""
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        self.password_var.set(password)
        self.show_password.set(True)
        self.toggle_password_visibility()
        self.real_time_check()
        self.check_password()
        self.status_var.set("🎲 Strong password generated and analyzed")
        
    def logout(self):
        """Handle logout"""
        response = messagebox.askyesno(
            "Confirm Logout", 
            f"Are you sure you want to logout?\n\n"
            f"User: {self.username}\n"
            f"Role: {self.role}\n"
            f"Session: {self.session_start.strftime('%H:%M:%S')}",
            icon='question'
        )
        
        if response:
            session_duration = datetime.now() - self.session_start
            minutes = int(session_duration.total_seconds() / 60)
            
            logging.info(f"User {self.username} logged out. Session duration: {minutes} minutes")
            
            messagebox.showinfo(
                "Logout Successful", 
                f"✅ You have been logged out successfully!\n\n"
                f"User: {self.username}\n"
                f"Session duration: {minutes} minutes\n"
                f"Logout time: {datetime.now().strftime('%H:%M:%S')}"
            )
            
            self.root.destroy()
            
            try:
                import subprocess
                subprocess.Popen(['python', 'auth_system.py'])
            except:
                print("Logout completed.")
    
    def change_password(self):
        """Placeholder for change password"""
        messagebox.showinfo(
            "Change Password", 
            "Password change functionality would be implemented here.\n\n"
            "This would include:\n"
            "• Current password verification\n"
            "• New password strength validation\n"
            "• 2FA confirmation\n"
            "• Email notification"
        )
    
    def center_window(self, width, height):
        """Center window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def launch_main_app(role, username, auth_system=None):
    """Launch the main password checker application"""
    root = tk.Tk()
    app = ModernPasswordChecker(root, role, username, auth_system)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPasswordChecker(root, 'demo', 'demo_user')
    root.mainloop()