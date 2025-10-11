# auth_system.py - Enhanced UI/UX Version
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
import secrets
import smtplib
import random
import threading
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Real2FASystem:
    def __init__(self):
        self.pending_verifications = {}
        self.smtp_config = {
            'server': 'smtp.gmail.com',
            'port': 587,
            'username': 'noreply.alert.banking@gmail.com',
            'password': 'iwpo zull mhiz fnub'
        }
        
    def generate_2fa_code(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def send_2fa_email(self, user_email, code):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = user_email
            msg['Subject'] = '🔐 Your Password Analyzer - 2FA Verification Code'
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #2c3e50; text-align: center;">🔒 Password Analyzer Pro</h2>
                    <h3 style="color: #3498db;">Two-Factor Authentication Required</h3>
                    
                    <p>Hello,</p>
                    <p>You are attempting to log in to <strong>Password Analyzer Pro</strong>. 
                    Please use the following verification code to complete your login:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="font-size: 32px; font-weight: bold; color: #e74c3c; letter-spacing: 5px; 
                                  background: #f8f9fa; padding: 15px; border-radius: 8px; border: 2px dashed #bdc3c7;">
                            {code}
                        </div>
                    </div>
                    
                    <p style="color: #7f8c8d; font-size: 12px;">
                        ⏰ This code will expire in 10 minutes.<br>
                        🔒 If you didn't request this login, please ignore this email.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                    <p style="color: #95a5a6; font-size: 11px; text-align: center;">
                        Password Analyzer Pro | DevSecOps Project | Security Testing & Assurance
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ 2FA code sent to {user_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send 2FA email: {e}")
            messagebox.showinfo("2FA Code (Fallback)", 
                              f"📧 Email sending failed. Your verification code:\n\n"
                              f"🔑 Code: {code}\n\n"
                              f"Error: {str(e)}")
            return True

    def send_welcome_email(self, user_email, username):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = user_email
            msg['Subject'] = '🎉 Welcome to Password Analyzer Pro!'
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #2c3e50; text-align: center;">🔒 Password Analyzer Pro</h2>
                    <h3 style="color: #27ae60;">Welcome Aboard!</h3>
                    
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Welcome to <strong>Password Analyzer Pro</strong> - your comprehensive password security assessment tool!</p>
                    
                    <div style="background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4 style="color: #2c3e50; margin-top: 0;">What you can do:</h4>
                        <ul style="color: #2c3e50;">
                            <li>🔍 Analyze password strength in real-time</li>
                            <li>📊 Get detailed security metrics</li>
                            <li>🛡️ Check against common passwords</li>
                            <li>⚡ Generate strong passwords</li>
                            <li>🔐 Secure 2FA authentication</li>
                        </ul>
                    </div>
                    
                    <p style="color: #7f8c8d; font-size: 12px;">
                        🔒 Your account is protected with industry-standard security measures including:<br>
                        • Password hashing with SHA-256<br>
                        • Two-factor authentication<br>
                        • Role-based access control<br>
                        • Secure email verification
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ecf0f1; margin: 20px 0;">
                    <p style="color: #95a5a6; font-size: 11px; text-align: center;">
                        Password Analyzer Pro | DevSecOps Project | Security Testing & Assurance
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Welcome email sent to {user_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send welcome email: {e}")
            return False
        
    def initiate_2fa(self, username, user_email):
        code = self.generate_2fa_code()
        self.pending_verifications[username] = {
            'code': code,
            'timestamp': time.time(),
            'email': user_email
        }
        
        def send_email_thread():
            success = self.send_2fa_email(user_email, code)
            return success
        
        thread = threading.Thread(target=send_email_thread)
        thread.daemon = True
        thread.start()
        
        return code
    
    def verify_2fa_code(self, username, entered_code):
        if username not in self.pending_verifications:
            return False
        
        verification_data = self.pending_verifications[username]
        stored_code = verification_data['code']
        timestamp = verification_data['timestamp']
        
        if time.time() - timestamp > 600:
            del self.pending_verifications[username]
            return False
        
        if entered_code == stored_code:
            del self.pending_verifications[username]
            return True
        
        return False

class AuthSystem:
    def __init__(self):
        self.users_file = 'users.json'
        self.two_fa_system = Real2FASystem()
        self.load_users()
        
    def load_users(self):
        try:
            if os.path.exists(self.users_file) and os.path.getsize(self.users_file) > 0:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
                print(f"✅ Loaded {len(self.users)} users from {self.users_file}")
            else:
                self.create_default_users()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Error loading users: {e}. Creating default users...")
            self.create_default_users()
            
    def create_default_users(self):
        self.users = {
            'admin': {
                'password_hash': self.hash_password('Admin123!'),
                'role': 'admin',
                'email': 'dragneeldtensa@gmail.com',
                '2fa_enabled': True,
                'created_at': time.time()
            },
            'demo': {
                'password_hash': self.hash_password('Demo123!'),
                'role': 'user',
                'email': 'dragneeldtensa@gmail.com',
                '2fa_enabled': True,
                'created_at': time.time()
            }
        }
        self.save_users()
        print("✅ Default users created successfully!")
            
    def save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            print(f"✅ Saved {len(self.users)} users to {self.users_file}")
        except Exception as e:
            print(f"❌ Error saving users: {e}")
            
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username, password):
        if username in self.users:
            return self.users[username]['password_hash'] == self.hash_password(password)
        return False
        
    def get_user_role(self, username):
        return self.users.get(username, {}).get('role', 'user')
    
    def get_user_email(self, username):
        return self.users.get(username, {}).get('email', '')
    
    def is_2fa_enabled(self, username):
        return self.users.get(username, {}).get('2fa_enabled', True)
    
    def username_exists(self, username):
        return username in self.users
    
    def email_exists(self, email):
        for user_data in self.users.values():
            if user_data.get('email', '').lower() == email.lower():
                return True
        return False
    
    def create_user(self, username, password, email, role='user'):
        if self.username_exists(username):
            return False, "Username already exists"
        
        if self.email_exists(email):
            return False, "Email already registered"
        
        if not self.is_valid_email(email):
            return False, "Invalid email format"
        
        if not self.is_strong_password(password):
            return False, "Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters"
        
        self.users[username] = {
            'password_hash': self.hash_password(password),
            'role': role,
            'email': email,
            '2fa_enabled': True,
            'created_at': time.time()
        }
        
        self.save_users()
        
        def send_welcome():
            self.two_fa_system.send_welcome_email(email, username)
        
        thread = threading.Thread(target=send_welcome)
        thread.daemon = True
        thread.start()
        
        return True, "User created successfully"
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[^A-Za-z0-9]', password):
            return False
        return True

class ModernAuthWindow:
    def __init__(self, root, auth_system):
        self.root = root
        self.auth_system = auth_system
        self.current_username = None
        self.animation_running = False
        self.countdown_after_id = None  # Track countdown timer
        self.setup_welcome_screen()
        
    def create_gradient_canvas(self, parent, width, height, color1, color2):
        """Create a gradient background canvas"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Create gradient effect
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
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_glass_frame(self, parent, **kwargs):
        """Create a glassmorphism-style frame"""
        frame = tk.Frame(parent, bg='#ffffff', **kwargs)
        frame.configure(highlightbackground='#e0e7ff', highlightthickness=2)
        return frame
    
    def animate_fade_in(self, widget, duration=500, delay=0):
        """Fade in animation for widgets"""
        if delay > 0:
            self.root.after(delay, lambda: self.animate_fade_in(widget, duration, 0))
            return
        
        widget.configure(bg=widget.cget('bg'))
        steps = 20
        step_time = duration // steps
        
        def fade_step(step):
            if step <= steps:
                alpha = step / steps
                widget.lift()
                self.root.after(step_time, lambda: fade_step(step + 1))
        
        fade_step(0)
    
    def create_hover_button(self, parent, text, command, bg_color, hover_color, **kwargs):
        """Create a button with hover effect"""
        btn = tk.Button(parent, text=text, command=command, bg=bg_color, 
                       relief='flat', cursor='hand2', **kwargs)
        
        def on_enter(e):
            btn.configure(bg=hover_color)
            btn.configure(relief='raised')
        
        def on_leave(e):
            btn.configure(bg=bg_color)
            btn.configure(relief='flat')
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
        
    def setup_welcome_screen(self):
        """Setup welcome screen with modern animations and effects"""
        self.root.title("🔐 Password Analyzer Pro - Welcome")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.center_window(600, 700)
        
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create gradient background
        bg_canvas = self.create_gradient_canvas(self.root, 600, 700, '#667eea', '#764ba2')
        bg_canvas.place(x=0, y=0)
        
        # Main container with glass effect
        main_container = self.create_glass_frame(self.root)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=520, height=620)
        
        # Animate main container
        self.animate_fade_in(main_container, duration=600)
        
        # Header Section with animated icon
        header_frame = tk.Frame(main_container, bg='white')
        header_frame.pack(pady=(30, 20))
        
        # Animated lock icon
        icon_canvas = tk.Canvas(header_frame, width=80, height=80, bg='white', highlightthickness=0)
        icon_canvas.pack()
        
        # Draw animated lock
        icon_canvas.create_oval(10, 30, 70, 70, fill='#667eea', outline='#764ba2', width=3)
        icon_canvas.create_rectangle(25, 45, 55, 65, fill='#ffd700', outline='#ffa500', width=2)
        icon_canvas.create_oval(35, 50, 45, 60, fill='#764ba2', outline='')
        
        tk.Label(header_frame, text="Password Analyzer Pro", 
                font=('Segoe UI', 26, 'bold'), bg='white', fg='#2d3748').pack(pady=(15, 5))
        
        tk.Label(header_frame, text="Secure • Reliable • Professional", 
                font=('Segoe UI', 11), bg='white', fg='#718096').pack()
        
        # Action Cards Container
        cards_container = tk.Frame(main_container, bg='white')
        cards_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Login Card with shadow effect
        login_card = self.create_glass_frame(cards_container)
        login_card.pack(fill=tk.X, pady=(0, 15))
        
        login_content = tk.Frame(login_card, bg='white', padx=25, pady=20)
        login_content.pack(fill=tk.BOTH)
        
        # Login icon and text
        login_header = tk.Frame(login_content, bg='white')
        login_header.pack(fill=tk.X)
        
        login_icon_canvas = tk.Canvas(login_header, width=40, height=40, bg='white', highlightthickness=0)
        login_icon_canvas.pack(side=tk.LEFT)
        login_icon_canvas.create_oval(5, 5, 35, 35, fill='#4299e1', outline='#3182ce', width=2)
        login_icon_canvas.create_text(20, 20, text="🔓", font=('Arial', 16))
        
        login_text_frame = tk.Frame(login_header, bg='white')
        login_text_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        tk.Label(login_text_frame, text="Existing User", font=('Segoe UI', 14, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w')
        
        tk.Label(login_text_frame, text="Access your secure account", font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack(anchor='w')
        
        # Login button with gradient-like effect
        login_btn = self.create_hover_button(
            login_content, "Login to Account", self.show_login_screen,
            '#4299e1', '#3182ce', font=('Segoe UI', 11, 'bold'), 
            fg='white', width=25, pady=12
        )
        login_btn.pack(pady=(15, 0))
        
        # Signup Card
        signup_card = self.create_glass_frame(cards_container)
        signup_card.pack(fill=tk.X, pady=(0, 15))
        
        signup_content = tk.Frame(signup_card, bg='white', padx=25, pady=20)
        signup_content.pack(fill=tk.BOTH)
        
        # Signup icon and text
        signup_header = tk.Frame(signup_content, bg='white')
        signup_header.pack(fill=tk.X)
        
        signup_icon_canvas = tk.Canvas(signup_header, width=40, height=40, bg='white', highlightthickness=0)
        signup_icon_canvas.pack(side=tk.LEFT)
        signup_icon_canvas.create_oval(5, 5, 35, 35, fill='#48bb78', outline='#38a169', width=2)
        signup_icon_canvas.create_text(20, 20, text="🚀", font=('Arial', 16))
        
        signup_text_frame = tk.Frame(signup_header, bg='white')
        signup_text_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        tk.Label(signup_text_frame, text="New User", font=('Segoe UI', 14, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w')
        
        tk.Label(signup_text_frame, text="Join our secure platform", font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack(anchor='w')
        
        # Signup button
        signup_btn = self.create_hover_button(
            signup_content, "Create Account", self.show_signup_screen,
            '#48bb78', '#38a169', font=('Segoe UI', 11, 'bold'), 
            fg='white', width=25, pady=12
        )
        signup_btn.pack(pady=(15, 0))
        
        # Demo Accounts Card with premium design
        demo_card = tk.Frame(cards_container, bg='#f7fafc', relief='flat',
                            highlightbackground='#cbd5e0', highlightthickness=2)
        demo_card.pack(fill=tk.X)
        
        demo_inner = tk.Frame(demo_card, bg='#f7fafc', padx=20, pady=15)
        demo_inner.pack(fill=tk.BOTH)
        
        tk.Label(demo_inner, text="💡 Demo Accounts", font=('Segoe UI', 11, 'bold'), 
                bg='#f7fafc', fg='#2d3748').pack(anchor='w')
        
        accounts_frame = tk.Frame(demo_inner, bg='#f7fafc')
        accounts_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Admin account
        admin_frame = tk.Frame(accounts_frame, bg='#f7fafc')
        admin_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(admin_frame, text="👑 Admin:", font=('Segoe UI', 9, 'bold'), 
                bg='#f7fafc', fg='#e53e3e').pack(side=tk.LEFT)
        tk.Label(admin_frame, text="admin / Admin123!", font=('Segoe UI', 9), 
                bg='#f7fafc', fg='#4a5568').pack(side=tk.LEFT, padx=(5, 0))
        
        # Demo account
        demo_frame = tk.Frame(accounts_frame, bg='#f7fafc')
        demo_frame.pack(fill=tk.X)
        tk.Label(demo_frame, text="👤 Demo:", font=('Segoe UI', 9, 'bold'), 
                bg='#f7fafc', fg='#38a169').pack(side=tk.LEFT)
        tk.Label(demo_frame, text="demo / Demo123!", font=('Segoe UI', 9), 
                bg='#f7fafc', fg='#4a5568').pack(side=tk.LEFT, padx=(5, 0))
        
        # Animated delay for cards
        self.animate_fade_in(login_card, duration=400, delay=200)
        self.animate_fade_in(signup_card, duration=400, delay=400)
        self.animate_fade_in(demo_card, duration=400, delay=600)

    def show_login_screen(self):
        """Show enhanced login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - Login")
        
        # Gradient background
        bg_canvas = self.create_gradient_canvas(self.root, 600, 700, '#4c51bf', '#6b46c1')
        bg_canvas.place(x=0, y=0)
        
        # Main container
        main_container = self.create_glass_frame(self.root)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=480, height=580)
        
        # Back button with icon
        back_frame = tk.Frame(main_container, bg='white')
        back_frame.pack(fill=tk.X, padx=25, pady=(20, 0))
        
        back_btn = self.create_hover_button(
            back_frame, "← Back", self.setup_welcome_screen,
            '#e2e8f0', '#cbd5e0', font=('Segoe UI', 9),
            fg='#2d3748', padx=15, pady=5
        )
        back_btn.pack(side=tk.LEFT)
        
        # Header
        header_frame = tk.Frame(main_container, bg='white')
        header_frame.pack(pady=(20, 30))
        
        # Icon
        icon_canvas = tk.Canvas(header_frame, width=70, height=70, bg='white', highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(5, 5, 65, 65, fill='#4c51bf', outline='#6b46c1', width=3)
        icon_canvas.create_text(35, 35, text="🔓", font=('Arial', 30))
        
        tk.Label(header_frame, text="Welcome Back", 
                font=('Segoe UI', 22, 'bold'), bg='white', fg='#2d3748').pack(pady=(15, 5))
        
        tk.Label(header_frame, text="Sign in to continue your session", 
                font=('Segoe UI', 10), bg='white', fg='#718096').pack()
        
        # Form container
        form_frame = tk.Frame(main_container, bg='white', padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username field
        tk.Label(form_frame, text="Username", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 5))
        
        self.login_username_var = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=self.login_username_var, 
                                 font=('Segoe UI', 11), bg='#f7fafc', relief='flat',
                                 highlightbackground='#cbd5e0', highlightthickness=2,
                                 highlightcolor='#4c51bf')
        username_entry.pack(fill=tk.X, ipady=10, pady=(0, 20))
        username_entry.focus()
        
        # Password field
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 5))
        
        self.login_password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=self.login_password_var, 
                                 font=('Segoe UI', 11), bg='#f7fafc', relief='flat',
                                 highlightbackground='#cbd5e0', highlightthickness=2,
                                 highlightcolor='#4c51bf', show="●")
        password_entry.pack(fill=tk.X, ipady=10, pady=(0, 30))
        
        # Login button
        login_btn = self.create_hover_button(
            form_frame, "🔐 Continue to 2FA", self.verify_credentials,
            '#4c51bf', '#6b46c1', font=('Segoe UI', 12, 'bold'), 
            fg='white', width=30, pady=14
        )
        login_btn.pack(fill=tk.X)
        
        # Signup link
        redirect_frame = tk.Frame(form_frame, bg='white')
        redirect_frame.pack(pady=(20, 0))
        
        tk.Label(redirect_frame, text="Don't have an account?", font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack(side=tk.LEFT)
        
        signup_link = tk.Label(redirect_frame, text="Sign up here", font=('Segoe UI', 9, 'bold'), 
                              bg='white', fg='#4c51bf', cursor='hand2')
        signup_link.pack(side=tk.LEFT, padx=(5, 0))
        signup_link.bind('<Button-1>', lambda e: self.show_signup_screen())
        signup_link.bind('<Enter>', lambda e: signup_link.configure(fg='#6b46c1'))
        signup_link.bind('<Leave>', lambda e: signup_link.configure(fg='#4c51bf'))
        
        self.root.bind('<Return>', lambda event: self.verify_credentials())
        
        # Animate entrance
        self.animate_fade_in(main_container, duration=500)

    def show_signup_screen(self):
        """Show enhanced signup screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - Sign Up")
        
        # Gradient background
        bg_canvas = self.create_gradient_canvas(self.root, 600, 700, '#38b2ac', '#319795')
        bg_canvas.place(x=0, y=0)
        
        # Main container
        main_container = self.create_glass_frame(self.root)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=480, height=620)
        
        # Back button
        back_frame = tk.Frame(main_container, bg='white')
        back_frame.pack(fill=tk.X, padx=25, pady=(20, 0))
        
        back_btn = self.create_hover_button(
            back_frame, "← Back", self.setup_welcome_screen,
            '#e2e8f0', '#cbd5e0', font=('Segoe UI', 9),
            fg='#2d3748', padx=15, pady=5
        )
        back_btn.pack(side=tk.LEFT)
        
        # Header
        header_frame = tk.Frame(main_container, bg='white')
        header_frame.pack(pady=(15, 25))
        
        # Icon
        icon_canvas = tk.Canvas(header_frame, width=60, height=60, bg='white', highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(5, 5, 55, 55, fill='#38b2ac', outline='#319795', width=3)
        icon_canvas.create_text(30, 30, text="🚀", font=('Arial', 24))
        
        tk.Label(header_frame, text="Create Account", 
                font=('Segoe UI', 20, 'bold'), bg='white', fg='#2d3748').pack(pady=(12, 5))
        
        tk.Label(header_frame, text="Join our secure platform today", 
                font=('Segoe UI', 10), bg='white', fg='#718096').pack()
        
        # Form container
        form_frame = tk.Frame(main_container, bg='white', padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username field
        tk.Label(form_frame, text="Username", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 5))
        
        self.signup_username_var = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=self.signup_username_var, 
                                 font=('Segoe UI', 11), bg='#f7fafc', relief='flat',
                                 highlightbackground='#cbd5e0', highlightthickness=2,
                                 highlightcolor='#38b2ac')
        username_entry.pack(fill=tk.X, ipady=10, pady=(0, 15))
        username_entry.focus()
        
        # Email field
        tk.Label(form_frame, text="Email Address", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 5))
        
        self.signup_email_var = tk.StringVar()
        email_entry = tk.Entry(form_frame, textvariable=self.signup_email_var, 
                              font=('Segoe UI', 11), bg='#f7fafc', relief='flat',
                              highlightbackground='#cbd5e0', highlightthickness=2,
                              highlightcolor='#38b2ac')
        email_entry.pack(fill=tk.X, ipady=10, pady=(0, 15))
        
        # Password field
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 5))
        
        self.signup_password_var = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=self.signup_password_var, 
                                 font=('Segoe UI', 11), bg='#f7fafc', relief='flat',
                                 highlightbackground='#cbd5e0', highlightthickness=2,
                                 highlightcolor='#38b2ac', show="●")
        password_entry.pack(fill=tk.X, ipady=10, pady=(0, 10))
        
        # Password requirements
        req_frame = tk.Frame(form_frame, bg='#e6fffa', relief='flat',
                           highlightbackground='#81e6d9', highlightthickness=1)
        req_frame.pack(fill=tk.X, pady=(0, 20))
        
        req_inner = tk.Frame(req_frame, bg='#e6fffa', padx=12, pady=8)
        req_inner.pack()
        
        tk.Label(req_inner, 
                text="🔒 8+ chars • Uppercase • Lowercase • Numbers • Special chars",
                font=('Segoe UI', 8), bg='#e6fffa', fg='#2c7a7b').pack()
        
        # Signup button
        signup_btn = self.create_hover_button(
            form_frame, "🎉 Create Account", self.create_account,
            '#38b2ac', '#319795', font=('Segoe UI', 12, 'bold'), 
            fg='white', width=30, pady=14
        )
        signup_btn.pack(fill=tk.X)
        
        # Login link
        redirect_frame = tk.Frame(form_frame, bg='white')
        redirect_frame.pack(pady=(15, 0))
        
        tk.Label(redirect_frame, text="Already have an account?", font=('Segoe UI', 9), 
                bg='white', fg='#718096').pack(side=tk.LEFT)
        
        login_link = tk.Label(redirect_frame, text="Login here", font=('Segoe UI', 9, 'bold'), 
                             bg='white', fg='#38b2ac', cursor='hand2')
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind('<Button-1>', lambda e: self.show_login_screen())
        login_link.bind('<Enter>', lambda e: login_link.configure(fg='#319795'))
        login_link.bind('<Leave>', lambda e: login_link.configure(fg='#38b2ac'))
        
        self.root.bind('<Return>', lambda event: self.create_account())
        
        # Animate entrance
        self.animate_fade_in(main_container, duration=500)

    def show_2fa_screen(self, username, user_email):
        """Show enhanced 2FA verification screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - 2FA Verification")
        
        # Gradient background
        bg_canvas = self.create_gradient_canvas(self.root, 600, 700, '#ed8936', '#dd6b20')
        bg_canvas.place(x=0, y=0)
        
        # Main container
        main_container = self.create_glass_frame(self.root)
        main_container.place(relx=0.5, rely=0.5, anchor='center', width=480, height=550)
        
        # Header
        header_frame = tk.Frame(main_container, bg='white')
        header_frame.pack(pady=(30, 20))
        
        # Animated email icon
        icon_canvas = tk.Canvas(header_frame, width=70, height=70, bg='white', highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_oval(5, 5, 65, 65, fill='#ed8936', outline='#dd6b20', width=3)
        icon_canvas.create_text(35, 35, text="📧", font=('Arial', 30))
        
        tk.Label(header_frame, text="Verify Your Identity", 
                font=('Segoe UI', 20, 'bold'), bg='white', fg='#2d3748').pack(pady=(15, 5))
        
        tk.Label(header_frame, text=f"Code sent to {user_email}", 
                font=('Segoe UI', 10), bg='white', fg='#718096').pack()
        
        # Form container
        form_frame = tk.Frame(main_container, bg='white', padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info box
        info_box = tk.Frame(form_frame, bg='#fffaf0', relief='flat',
                          highlightbackground='#fbd38d', highlightthickness=2)
        info_box.pack(fill=tk.X, pady=(0, 25))
        
        info_inner = tk.Frame(info_box, bg='#fffaf0', padx=15, pady=12)
        info_inner.pack()
        
        tk.Label(info_inner, 
                text="📬 Please check your email inbox\nEnter the 6-digit verification code below",
                font=('Segoe UI', 9), bg='#fffaf0', fg='#744210', justify=tk.CENTER).pack()
        
        # 2FA Code Entry
        tk.Label(form_frame, text="Verification Code", font=('Segoe UI', 10, 'bold'), 
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 8))
        
        self.tfa_var = tk.StringVar()
        
        # Create custom code entry with individual boxes (visual effect)
        code_container = tk.Frame(form_frame, bg='white')
        code_container.pack(pady=(0, 15))
        
        tfa_entry = tk.Entry(code_container, textvariable=self.tfa_var, 
                            font=('Segoe UI', 20, 'bold'), bg='#f7fafc', relief='flat',
                            highlightbackground='#cbd5e0', highlightthickness=2,
                            highlightcolor='#ed8936', width=12, justify=tk.CENTER)
        tfa_entry.pack(ipady=12)
        tfa_entry.focus()
        
        # Countdown timer
        self.countdown_time = 600
        self.countdown_label = tk.Label(form_frame, font=('Segoe UI', 9, 'bold'), 
                                       bg='white', fg='#e53e3e')
        self.countdown_label.pack(pady=(10, 20))
        self.start_countdown()
        
        # Verify button
        verify_btn = self.create_hover_button(
            form_frame, "✅ Verify Code", lambda: self.verify_2fa_code(username),
            '#48bb78', '#38a169', font=('Segoe UI', 11, 'bold'), 
            fg='white', width=30, pady=12
        )
        verify_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Resend button
        resend_btn = self.create_hover_button(
            form_frame, "🔄 Resend Code", lambda: self.resend_2fa_code(username, user_email),
            '#ed8936', '#dd6b20', font=('Segoe UI', 10), 
            fg='white', width=30, pady=10
        )
        resend_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_btn = self.create_hover_button(
            form_frame, "← Back to Login", self.show_login_screen,
            '#e2e8f0', '#cbd5e0', font=('Segoe UI', 9),
            fg='#2d3748', width=30, pady=8
        )
        back_btn.pack(fill=tk.X)
        
        self.root.bind('<Return>', lambda event: self.verify_2fa_code(username))
        
        # Animate entrance
        self.animate_fade_in(main_container, duration=500)

    def create_account(self):
        """Create a new user account"""
        username = self.signup_username_var.get()
        email = self.signup_email_var.get()
        password = self.signup_password_var.get()
        
        if not all([username, email, password]):
            messagebox.showerror("Input Error", "❌ Please fill in all fields.")
            return
        
        success, message = self.auth_system.create_user(username, password, email)
        
        if success:
            messagebox.showinfo("Account Created", 
                              f"✅ {message}\n\n"
                              f"Welcome, {username}!\n\n"
                              f"A welcome email has been sent to {email}")
            self.show_login_screen()
        else:
            messagebox.showerror("Signup Failed", f"❌ {message}")

    def verify_credentials(self):
        """Verify username and password, then initiate 2FA"""
        username = self.login_username_var.get()
        password = self.login_password_var.get()
        
        if not username or not password:
            messagebox.showerror("Input Error", "❌ Please enter both username and password.")
            return
        
        if self.auth_system.verify_password(username, password):
            user_email = self.auth_system.get_user_email(username)
            if not user_email:
                messagebox.showerror("Configuration Error", "❌ User email not configured.")
                return
            
            self.current_username = username
            
            messagebox.showinfo("2FA Required", 
                              f"📧 Sending verification code to {user_email}...\n\n"
                              "Please check your email and enter the 6-digit code.")
            
            code = self.auth_system.two_fa_system.initiate_2fa(username, user_email)
            
            if code:
                self.show_2fa_screen(username, user_email)
            else:
                messagebox.showerror("2FA Error", "❌ Failed to send 2FA code. Please try again.")
        else:
            messagebox.showerror("Authentication Failed", "❌ Invalid username or password.")

    def start_countdown(self):
        """Start countdown timer for 2FA code expiration"""
        if self.countdown_time > 0:
            minutes = self.countdown_time // 60
            seconds = self.countdown_time % 60
            self.countdown_label.config(text=f"⏰ Code expires in: {minutes:02d}:{seconds:02d}")
            self.countdown_time -= 1
            self.root.after(1000, self.start_countdown)
        else:
            self.countdown_label.config(text="❌ Code expired - please request a new one")

    def verify_2fa_code(self, username):
        """Verify the entered 2FA code"""
        entered_code = self.tfa_var.get()
        
        if not entered_code or len(entered_code) != 6:
            messagebox.showerror("Input Error", "❌ Please enter a valid 6-digit code.")
            return
        
        if self.auth_system.two_fa_system.verify_2fa_code(username, entered_code):
            role = self.auth_system.get_user_role(username)
            messagebox.showinfo("Access Granted", 
                              f"✅ Login successful!\n\nWelcome, {username}!\nRole: {role.title()}")
            self.root.destroy()
            self.launch_main_app(role, username)
        else:
            messagebox.showerror("Verification Failed", 
                               "❌ Invalid or expired verification code.\n\n"
                               "Please check the code and try again, or request a new one.")

    def resend_2fa_code(self, username, user_email):
        """Resend 2FA code"""
        code = self.auth_system.two_fa_system.initiate_2fa(username, user_email)
        if code:
            messagebox.showinfo("Code Resent", "✅ New verification code sent to your email!")
            self.countdown_time = 600
        else:
            messagebox.showerror("Resend Failed", "❌ Failed to resend code. Please try again.")

    def launch_main_app(self, role, username):
        """Launch the main password checker application"""
        try:
            from password_strength_checker import launch_main_app
            launch_main_app(role, username, self.auth_system)
        except ImportError:
            messagebox.showinfo("Success", f"Logged in as {username} ({role})")
            print(f"User {username} with role {role} logged in successfully")

    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    """Main function"""
    print("🚀 Starting Secure Password Analyzer with Enhanced UI/UX...")
    print("📧 Using email: noreply.alert.banking@gmail.com")
    
    root = tk.Tk()
    auth_system = AuthSystem()
    auth_app = ModernAuthWindow(root, auth_system)
    root.mainloop()

if __name__ == "__main__":
    main()