# password_strength_checker.py
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
        self.setup_modern_gui()
        self.setup_logging()
        self.load_common_passwords()
        
    def setup_modern_gui(self):
        """Setup modern and professional GUI with logout features"""
        self.root.title(f"🔐 Password Analyzer Pro - {self.role.title()} Mode")
        self.root.geometry("900x750")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window(900, 750)
        
        # Create main container with modern layout
        main_container = tk.Frame(self.root, bg='#f8f9fa', padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header Section with User Info and Logout
        header_frame = tk.Frame(main_container, bg='#f8f9fa')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side - App Title
        title_frame = tk.Frame(header_frame, bg='#f8f9fa')
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(title_frame, text="🔒 Password Analyzer Pro", 
                font=('Arial', 20, 'bold'), bg='#f8f9fa', fg='#2c3e50').pack(anchor='w')
        
        tk.Label(title_frame, text="Advanced Password Security Assessment Tool", 
                font=('Arial', 11), bg='#f8f9fa', fg='#7f8c8d').pack(anchor='w', pady=(5, 0))
        
        # Right side - User Info and Logout
        user_frame = tk.Frame(header_frame, bg='#f8f9fa')
        user_frame.pack(side=tk.RIGHT)
        
        # User info card
        user_info_card = tk.Frame(user_frame, bg='#e8f4f8', relief='flat',
                                 highlightbackground='#bde0fe', highlightthickness=1)
        user_info_card.pack(fill=tk.X, pady=(0, 10))
        
        user_info_inner = tk.Frame(user_info_card, bg='#e8f4f8', padx=12, pady=8)
        user_info_inner.pack(fill=tk.BOTH)
        
        # User details
        user_details = tk.Frame(user_info_inner, bg='#e8f4f8')
        user_details.pack(fill=tk.X)
        
        tk.Label(user_details, text=f"👤 {self.username}", 
                font=('Arial', 10, 'bold'), bg='#e8f4f8', fg='#2c3e50').pack(side=tk.LEFT)
        
        role_color = '#e74c3c' if self.role == 'admin' else '#27ae60'
        role_label = tk.Label(user_details, text=f"● {self.role.upper()}", 
                             font=('Arial', 9, 'bold'), bg='#e8f4f8', fg=role_color)
        role_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Session info
        session_label = tk.Label(user_info_inner, 
                                text=f"🕒 Session: {self.session_start.strftime('%H:%M:%S')}",
                                font=('Arial', 8), bg='#e8f4f8', fg='#7f8c8d')
        session_label.pack(anchor='w', pady=(2, 0))
        
        # Logout button
        logout_btn = tk.Button(user_frame, text="🚪 Logout", 
                              font=('Arial', 9, 'bold'), bg='#e74c3c', fg='white',
                              relief='flat', cursor='hand2', padx=15,
                              command=self.logout)
        logout_btn.pack(fill=tk.X)
        logout_btn.bind('<Enter>', lambda e: logout_btn.configure(bg='#c0392b'))
        logout_btn.bind('<Leave>', lambda e: logout_btn.configure(bg='#e74c3c'))
        
        # Main Content Card
        content_card = tk.Frame(main_container, bg='white', relief='flat',
                               highlightbackground='#e1e8ed', highlightthickness=1)
        content_card.pack(fill=tk.BOTH, expand=True)
        
        # Create Notebook for tabs
        self.notebook = ttk.Notebook(content_card)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Password Analysis
        self.setup_analysis_tab()
        
        # Tab 2: Security Dashboard
        self.setup_dashboard_tab()
        
        # Tab 3: User Profile (New)
        self.setup_profile_tab()
        
        # Status Bar
        self.setup_status_bar(main_container)
        
    def setup_analysis_tab(self):
        """Setup the main password analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="🔍 Password Analysis")
        
        # Password Input Section
        input_frame = tk.Frame(analysis_frame, bg='white', padx=20, pady=20)
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Enter Password to Analyze:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        
        # Password entry with show/hide toggle
        entry_frame = tk.Frame(input_frame, bg='white')
        entry_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(entry_frame, textvariable=self.password_var, 
                                      font=('Arial', 12), show="•", bg='#f8f9fa',
                                      relief='flat', highlightbackground='#ddd', 
                                      highlightthickness=1, highlightcolor='#3498db')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.password_entry.bind('<KeyRelease>', self.real_time_check)
        
        self.show_password = tk.BooleanVar()
        eye_btn = tk.Checkbutton(entry_frame, text="👁", variable=self.show_password,
                                command=self.toggle_password_visibility,
                                bg='white', relief='flat', cursor='hand2')
        eye_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Strength Meter
        strength_frame = tk.Frame(input_frame, bg='white')
        strength_frame.pack(fill=tk.X, pady=(15, 10))
        
        tk.Label(strength_frame, text="Password Strength:", 
                font=('Arial', 10, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.strength_var = tk.StringVar(value="Not analyzed")
        strength_label = tk.Label(strength_frame, textvariable=self.strength_var,
                                 font=('Arial', 11, 'bold'), bg='white')
        strength_label.pack(anchor='w', pady=(5, 0))
        
        # Modern progress bar
        self.progress = ttk.Progressbar(strength_frame, orient='horizontal', 
                                       length=300, mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        # Action Buttons
        button_frame = tk.Frame(input_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        analyze_btn = tk.Button(button_frame, text="🔍 Analyze Password", 
                               font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                               relief='flat', cursor='hand2', command=self.check_password)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        analyze_btn.bind('<Enter>', lambda e: analyze_btn.configure(bg='#2980b9'))
        analyze_btn.bind('<Leave>', lambda e: analyze_btn.configure(bg='#3498db'))
        
        generate_btn = tk.Button(button_frame, text="🎲 Generate Strong Password", 
                                font=('Arial', 10), bg='#27ae60', fg='white',
                                relief='flat', cursor='hand2', command=self.generate_password)
        generate_btn.pack(side=tk.LEFT)
        generate_btn.bind('<Enter>', lambda e: generate_btn.configure(bg='#219652'))
        generate_btn.bind('<Leave>', lambda e: generate_btn.configure(bg='#27ae60'))
        
        # Results Section
        results_frame = tk.Frame(analysis_frame, bg='white', padx=20, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(results_frame, text="Analysis Results:", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        
        # Modern results display
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     font=('Consolas', 9),
                                                     bg='#f8f9fa', relief='flat',
                                                     highlightbackground='#ddd',
                                                     highlightthickness=1,
                                                     wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
    def setup_dashboard_tab(self):
        """Setup security dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Security Dashboard")
        
        content = tk.Frame(dashboard_frame, bg='white', padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Security metrics
        metrics = [
            ("🔒 Password Entropy", "Measures randomness and unpredictability"),
            ("🛡️ Common Password Check", "Compares against known weak passwords"),
            ("📊 Pattern Analysis", "Detects sequential or repeated patterns"),
            ("⚡ Real-time Feedback", "Instant strength assessment"),
            ("🔍 Hash Verification", "SHA-256 password hashing"),
            ("📈 Strength Scoring", "Comprehensive security scoring"),
            ("👤 User Session", f"Logged in as: {self.username}"),
            ("🎯 User Role", f"Access level: {self.role.upper()}"),
            ("🕒 Session Duration", f"Started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        ]
        
        for i, (title, desc) in enumerate(metrics):
            metric_frame = tk.Frame(content, bg='#f8f9fa', relief='flat',
                                  highlightbackground='#e1e8ed', highlightthickness=1)
            metric_frame.pack(fill=tk.X, pady=(0, 10))
            
            inner_frame = tk.Frame(metric_frame, bg='#f8f9fa', padx=15, pady=10)
            inner_frame.pack(fill=tk.BOTH)
            
            tk.Label(inner_frame, text=title, font=('Arial', 11, 'bold'),
                   bg='#f8f9fa', fg='#2c3e50').pack(anchor='w')
            tk.Label(inner_frame, text=desc, font=('Arial', 9),
                   bg='#f8f9fa', fg='#7f8c8d').pack(anchor='w', pady=(2, 0))
    
    def setup_profile_tab(self):
        """Setup user profile tab"""
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="👤 User Profile")
        
        content = tk.Frame(profile_frame, bg='white', padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Profile Header
        header_frame = tk.Frame(content, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="User Profile & Session Information", 
                font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        
        # Profile Card
        profile_card = tk.Frame(content, bg='#f8f9fa', relief='flat',
                               highlightbackground='#e1e8ed', highlightthickness=1)
        profile_card.pack(fill=tk.X, pady=(0, 20))
        
        profile_inner = tk.Frame(profile_card, bg='#f8f9fa', padx=20, pady=20)
        profile_inner.pack(fill=tk.BOTH)
        
        # User Information
        info_grid = tk.Frame(profile_inner, bg='#f8f9fa')
        info_grid.pack(fill=tk.X)
        
        user_info = [
            ("👤 Username:", self.username),
            ("🎯 Role:", self.role.upper()),
            ("🆔 User ID:", f"UID_{hash(self.username) % 10000:04d}"),
            ("📧 Email:", "dragneeldtensa@gmail.com"),  # This would come from auth system
            ("🕒 Session Start:", self.session_start.strftime('%Y-%m-%d %H:%M:%S')),
            ("⏱️ Session Duration:", "Active now"),
            ("🔐 2FA Status:", "Enabled"),
            ("📊 Passwords Analyzed:", "0")  # Could track this
        ]
        
        for i, (label, value) in enumerate(user_info):
            row = tk.Frame(info_grid, bg='#f8f9fa')
            row.pack(fill=tk.X, pady=(0, 8))
            
            tk.Label(row, text=label, font=('Arial', 10, 'bold'), 
                   bg='#f8f9fa', fg='#2c3e50', width=15, anchor='w').pack(side=tk.LEFT)
            tk.Label(row, text=value, font=('Arial', 10), 
                   bg='#f8f9fa', fg='#7f8c8d').pack(side=tk.LEFT, padx=(10, 0))
        
        # Action Buttons
        action_frame = tk.Frame(content, bg='white')
        action_frame.pack(fill=tk.X)
        
        # Logout button in profile
        profile_logout_btn = tk.Button(action_frame, text="🚪 Logout from System", 
                                      font=('Arial', 11, 'bold'), bg='#e74c3c', fg='white',
                                      relief='flat', cursor='hand2',
                                      command=self.logout)
        profile_logout_btn.pack(side=tk.LEFT, padx=(0, 10))
        profile_logout_btn.bind('<Enter>', lambda e: profile_logout_btn.configure(bg='#c0392b'))
        profile_logout_btn.bind('<Leave>', lambda e: profile_logout_btn.configure(bg='#e74c3c'))
        
        # Change Password button (placeholder)
        change_pwd_btn = tk.Button(action_frame, text="🔑 Change Password", 
                                  font=('Arial', 11), bg='#3498db', fg='white',
                                  relief='flat', cursor='hand2',
                                  command=self.change_password)
        change_pwd_btn.pack(side=tk.LEFT)
        change_pwd_btn.bind('<Enter>', lambda e: change_pwd_btn.configure(bg='#2980b9'))
        change_pwd_btn.bind('<Leave>', lambda e: change_pwd_btn.configure(bg='#3498db'))
        
    def setup_status_bar(self, parent):
        """Setup status bar with session info"""
        status_frame = tk.Frame(parent, bg='#2c3e50', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        # Left side - Status message
        left_frame = tk.Frame(status_frame, bg='#2c3e50')
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_var = tk.StringVar(value=f"🔒 Welcome {self.username}! Session active since {self.session_start.strftime('%H:%M:%S')}")
        status_label = tk.Label(left_frame, textvariable=self.status_var,
                              font=('Arial', 9), bg='#2c3e50', fg='white')
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Right side - Session info and logout
        right_frame = tk.Frame(status_frame, bg='#2c3e50')
        right_frame.pack(side=tk.RIGHT)
        
        # Quick logout button in status bar
        quick_logout_btn = tk.Button(right_frame, text="🚪 Logout", 
                                   font=('Arial', 8, 'bold'), bg='#e74c3c', fg='white',
                                   relief='flat', cursor='hand2', padx=8,
                                   command=self.logout)
        quick_logout_btn.pack(side=tk.RIGHT, padx=(5, 10))
        quick_logout_btn.bind('<Enter>', lambda e: quick_logout_btn.configure(bg='#c0392b'))
        quick_logout_btn.bind('<Leave>', lambda e: quick_logout_btn.configure(bg='#e74c3c'))
        
        # Session timer
        self.session_timer_var = tk.StringVar(value="🕒 00:00:00")
        timer_label = tk.Label(right_frame, textvariable=self.session_timer_var,
                             font=('Arial', 8), bg='#2c3e50', fg='#bdc3c7')
        timer_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Start session timer
        self.start_session_timer()
        
    def start_session_timer(self):
        """Start updating session timer"""
        session_duration = datetime.now() - self.session_start
        hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.session_timer_var.set(f"🕒 {hours:02d}:{minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.start_session_timer)
        
    def logout(self):
        """Handle user logout with confirmation"""
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
            
            # Log the logout
            logging.info(f"User {self.username} logged out. Session duration: {minutes} minutes")
            
            # Show logout message
            messagebox.showinfo(
                "Logout Successful", 
                f"✅ You have been logged out successfully!\n\n"
                f"User: {self.username}\n"
                f"Session duration: {minutes} minutes\n"
                f"Logout time: {datetime.now().strftime('%H:%M:%S')}"
            )
            
            # Close the application
            self.root.destroy()
            
            # Optional: Restart auth system
            try:
                import subprocess
                subprocess.Popen(['python', 'auth_system.py'])
            except:
                print("Logout completed. Auth system can be restarted manually.")
    
    def change_password(self):
        """Placeholder for change password functionality"""
        messagebox.showinfo(
            "Change Password", 
            "Password change functionality would be implemented here.\n\n"
            "This would include:\n"
            "• Current password verification\n"
            "• New password strength validation\n"
            "• 2FA confirmation\n"
            "• Email notification"
        )
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
            
    def setup_logging(self):
        logging.basicConfig(
            filename='app_audit.log',
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
        
    def real_time_check(self, event=None):
        password = self.password_var.get()
        if not password:
            self.progress['value'] = 0
            self.strength_var.set("Strength: Not analyzed")
            self.status_var.set(f"🔒 Welcome {self.username}! Ready for password analysis")
            return
            
        entropy = self.calculate_entropy(password)
        strength_score = min(entropy / 2, 100)
        
        self.progress['value'] = strength_score
        
        if strength_score < 30:
            self.strength_var.set("Strength: ❌ Weak")
            self.progress.configure(style='red.Horizontal.TProgressbar')
            self.status_var.set("⚠️  Password is weak - consider improving")
        elif strength_score < 70:
            self.strength_var.set("Strength: ⚠️  Medium")
            self.progress.configure(style='yellow.Horizontal.TProgressbar')
            self.status_var.set("🔐 Password is acceptable but could be stronger")
        else:
            self.strength_var.set("Strength: ✅ Strong")
            self.progress.configure(style='green.Horizontal.TProgressbar')
            self.status_var.set("✅ Password strength is excellent!")
            
    def check_password(self):
        password = self.password_var.get()
        
        if not password:
            messagebox.showwarning("Input Required", "🔍 Please enter a password to analyze.")
            return
            
        self.results_text.delete(1.0, tk.END)
        
        # Comprehensive analysis
        results = ["🔒 COMPREHENSIVE PASSWORD ANALYSIS\n" + "="*40 + "\n"]
        
        # Basic metrics
        length = len(password)
        entropy = self.calculate_entropy(password)
        
        results.append(f"📏 LENGTH ANALYSIS:")
        results.append(f"   • Password length: {length} characters")
        results.append(f"   • Entropy score: {entropy} bits\n")
        
        # Character composition
        results.append("🔠 CHARACTER COMPOSITION:")
        checks = [
            ('Lowercase letters (a-z)', r'[a-z]'),
            ('Uppercase letters (A-Z)', r'[A-Z]'),
            ('Numbers (0-9)', r'[0-9]'),
            ('Special characters', r'[^a-zA-Z0-9]')
        ]
        
        all_checks_passed = True
        for check_name, pattern in checks:
            if re.search(pattern, password):
                results.append(f"   ✅ Contains {check_name}")
            else:
                results.append(f"   ❌ Missing {check_name}")
                all_checks_passed = False
        results.append("")
        
        # Security checks
        results.append("🛡️ SECURITY CHECKS:")
        
        # Common password check
        if self.check_common_password(password):
            results.append("   ❌ WARNING: This is a commonly used password!")
        else:
            results.append("   ✅ Not found in common password database")
            
        # Pattern analysis
        pattern_issues = self.check_patterns(password)
        if pattern_issues:
            results.append("   ⚠️  Weak patterns detected:")
            for issue in pattern_issues:
                results.append(f"     • {issue}")
        else:
            results.append("   ✅ No weak patterns detected")
            
        # Hash display
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        results.append(f"\n🔐 SECURITY HASH:")
        results.append(f"   SHA-256: {hash_value}")
        
        # Overall recommendation
        results.append("\n💡 RECOMMENDATION:")
        if entropy < 50:
            results.append("   ❌ This password is weak. Consider using a longer password")
            results.append("   with mixed character types.")
        elif entropy < 80:
            results.append("   ⚠️  This password is acceptable but could be stronger.")
            results.append("   Add more special characters or increase length.")
        else:
            results.append("   ✅ Excellent password strength! Good job!")
            
        # Display results
        for result in results:
            self.results_text.insert(tk.END, result + '\n')
            
        logging.info(f"User {self.username} analyzed password: {length} chars, entropy: {entropy}")
        self.status_var.set("✅ Analysis complete - check results above")
        
    def generate_password(self):
        """Generate a strong password"""
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        self.password_var.set(password)
        self.toggle_password_visibility()  # Show the generated password
        self.show_password.set(True)
        self.real_time_check()
        self.check_password()
        self.status_var.set("🎲 Strong password generated and analyzed")
        
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

# Configure ttk styles
def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure progressbar styles
    style.configure('red.Horizontal.TProgressbar', background='#e74c3c')
    style.configure('yellow.Horizontal.TProgressbar', background='#f39c12')
    style.configure('green.Horizontal.TProgressbar', background='#27ae60')
    style.configure('Horizontal.TProgressbar', background='#3498db')

def launch_main_app(role, username, auth_system=None):
    """Launch the main password checker application"""
    root = tk.Tk()
    configure_styles()
    app = ModernPasswordChecker(root, role, username, auth_system)
    root.mainloop()

# For direct execution
if __name__ == "__main__":
    root = tk.Tk()
    configure_styles()
    app = ModernPasswordChecker(root, 'demo', 'demo_user')
    root.mainloop()