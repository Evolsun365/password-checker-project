# auth_system.py
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
        """Generate a 6-digit 2FA code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    def send_2fa_email(self, user_email, code):
        """Send 2FA code to user's email"""
        try:
            # Email configuration
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = user_email
            msg['Subject'] = '🔐 Your Password Analyzer - 2FA Verification Code'
            
            # Email body
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
                        🔐 If you didn't request this login, please ignore this email.
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
            
            # Connect to SMTP server and send email
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()  # Enable security
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ 2FA code sent to {user_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send 2FA email: {e}")
            # Show the code in message box for testing
            messagebox.showinfo("2FA Code (Fallback)", 
                              f"📧 Email sending failed. Your verification code:\n\n"
                              f"🔐 Code: {code}\n\n"
                              f"Error: {str(e)}")
            return True

    def send_welcome_email(self, user_email, username):
        """Send welcome email to new users"""
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
        """Initiate 2FA process for a user"""
        code = self.generate_2fa_code()
        self.pending_verifications[username] = {
            'code': code,
            'timestamp': time.time(),
            'email': user_email
        }
        
        # Send email in a separate thread to avoid UI freezing
        def send_email_thread():
            success = self.send_2fa_email(user_email, code)
            return success
        
        thread = threading.Thread(target=send_email_thread)
        thread.daemon = True
        thread.start()
        
        return code
    
    def verify_2fa_code(self, username, entered_code):
        """Verify the 2FA code with expiration check"""
        if username not in self.pending_verifications:
            return False
        
        verification_data = self.pending_verifications[username]
        stored_code = verification_data['code']
        timestamp = verification_data['timestamp']
        
        # Check if code is expired (10 minutes)
        if time.time() - timestamp > 600:  # 10 minutes in seconds
            del self.pending_verifications[username]
            return False
        
        # Verify the code
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
        """Load users from JSON file, create default if doesn't exist"""
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
        """Create default users with different roles and email addresses"""
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
        """Save users to JSON file"""
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
        """Check if username already exists"""
        return username in self.users
    
    def email_exists(self, email):
        """Check if email already exists"""
        for user_data in self.users.values():
            if user_data.get('email', '').lower() == email.lower():
                return True
        return False
    
    def create_user(self, username, password, email, role='user'):
        """Create a new user account"""
        if self.username_exists(username):
            return False, "Username already exists"
        
        if self.email_exists(email):
            return False, "Email already registered"
        
        # Validate email format
        if not self.is_valid_email(email):
            return False, "Invalid email format"
        
        # Validate password strength
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
        
        # Send welcome email in background
        def send_welcome():
            self.two_fa_system.send_welcome_email(email, username)
        
        thread = threading.Thread(target=send_welcome)
        thread.daemon = True
        thread.start()
        
        return True, "User created successfully"
    
    def is_valid_email(self, email):
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_strong_password(self, password):
        """Check password strength"""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):  # uppercase
            return False
        if not re.search(r'[a-z]', password):  # lowercase
            return False
        if not re.search(r'[0-9]', password):  # numbers
            return False
        if not re.search(r'[^A-Za-z0-9]', password):  # special characters
            return False
        return True

class ModernAuthWindow:
    def __init__(self, root, auth_system):
        self.root = root
        self.auth_system = auth_system
        self.current_username = None
        self.setup_welcome_screen()
        
    def setup_welcome_screen(self):
        """Setup welcome screen with login/signup options"""
        self.root.title("🔐 Password Analyzer Pro - Welcome")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f2f5')
        self.root.resizable(False, False)
        
        self.center_window(500, 600)
        
        # Clear existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f2f5', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header Section
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(pady=(40, 30))
        
        icon_label = tk.Label(header_frame, text="🔒", font=('Arial', 50), bg='#f0f2f5', fg='#2c3e50')
        icon_label.pack()
        
        title_label = tk.Label(header_frame, text="Password Analyzer Pro", 
                              font=('Arial', 24, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(header_frame, text="Secure Password Strength Assessment", 
                                 font=('Arial', 12), bg='#f0f2f5', fg='#7f8c8d')
        subtitle_label.pack()
        
        # Action Cards
        cards_frame = tk.Frame(main_container, bg='#f0f2f5')
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 30))
        
        # Login Card
        login_card = tk.Frame(cards_frame, bg='white', relief='flat', 
                             highlightbackground='#e1e8ed', highlightthickness=1)
        login_card.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        login_content = tk.Frame(login_card, bg='white', padx=25, pady=25)
        login_content.pack(fill=tk.BOTH)
        
        tk.Label(login_content, text="🔓 Existing User", font=('Arial', 14, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        tk.Label(login_content, text="Sign in to your account", font=('Arial', 10), 
                bg='white', fg='#7f8c8d').pack(anchor='w', pady=(0, 15))
        
        login_btn = tk.Button(login_content, text="Login to Account", 
                             font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                             relief='flat', cursor='hand2', width=20,
                             command=self.show_login_screen)
        login_btn.pack(anchor='w')
        login_btn.bind('<Enter>', lambda e: login_btn.configure(bg='#2980b9'))
        login_btn.bind('<Leave>', lambda e: login_btn.configure(bg='#3498db'))
        
        # Signup Card
        signup_card = tk.Frame(cards_frame, bg='white', relief='flat', 
                              highlightbackground='#e1e8ed', highlightthickness=1)
        signup_card.pack(fill=tk.X, pady=(0, 15), padx=10)
        
        signup_content = tk.Frame(signup_card, bg='white', padx=25, pady=25)
        signup_content.pack(fill=tk.BOTH)
        
        tk.Label(signup_content, text="🚀 New User", font=('Arial', 14, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        tk.Label(signup_content, text="Create a new account", font=('Arial', 10), 
                bg='white', fg='#7f8c8d').pack(anchor='w', pady=(0, 15))
        
        signup_btn = tk.Button(signup_content, text="Create Account", 
                              font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                              relief='flat', cursor='hand2', width=20,
                              command=self.show_signup_screen)
        signup_btn.pack(anchor='w')
        signup_btn.bind('<Enter>', lambda e: signup_btn.configure(bg='#219652'))
        signup_btn.bind('<Leave>', lambda e: signup_btn.configure(bg='#27ae60'))
        
        # Demo Accounts
        demo_frame = tk.Frame(main_container, bg='#e8f4f8', relief='flat',
                             highlightbackground='#bde0fe', highlightthickness=1)
        demo_frame.pack(fill=tk.X, padx=10)
        
        demo_inner = tk.Frame(demo_frame, bg='#e8f4f8', padx=15, pady=15)
        demo_inner.pack(fill=tk.BOTH)
        
        tk.Label(demo_inner, text="💡 Demo Accounts", font=('Arial', 11, 'bold'), 
                bg='#e8f4f8', fg='#2c3e50').pack(anchor='w')
        
        accounts_frame = tk.Frame(demo_inner, bg='#e8f4f8')
        accounts_frame.pack(fill=tk.X, pady=(10, 0))
        
        admin_frame = tk.Frame(accounts_frame, bg='#e8f4f8')
        admin_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(admin_frame, text="👑 Admin:", font=('Arial', 9, 'bold'), 
                bg='#e8f4f8', fg='#e74c3c').pack(side=tk.LEFT)
        tk.Label(admin_frame, text="admin / Admin123!", font=('Arial', 9), 
                bg='#e8f4f8', fg='#2c3e50').pack(side=tk.LEFT, padx=(5, 0))
        
        demo_frame = tk.Frame(accounts_frame, bg='#e8f4f8')
        demo_frame.pack(fill=tk.X)
        tk.Label(demo_frame, text="👤 Demo:", font=('Arial', 9, 'bold'), 
                bg='#e8f4f8', fg='#27ae60').pack(side=tk.LEFT)
        tk.Label(demo_frame, text="demo / Demo123!", font=('Arial', 9), 
                bg='#e8f4f8', fg='#2c3e50').pack(side=tk.LEFT, padx=(5, 0))

    def show_signup_screen(self):
        """Show the signup screen"""
        # Clear existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - Sign Up")
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f2f5', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(pady=(0, 20))
        
        back_btn = tk.Button(header_frame, text="← Back", font=('Arial', 9), 
                            bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                            command=self.setup_welcome_screen)
        back_btn.pack(anchor='w')
        back_btn.bind('<Enter>', lambda e: back_btn.configure(bg='#7f8c8d'))
        back_btn.bind('<Leave>', lambda e: back_btn.configure(bg='#95a5a6'))
        
        icon_label = tk.Label(header_frame, text="🚀", font=('Arial', 40), bg='#f0f2f5', fg='#2c3e50')
        icon_label.pack(pady=(10, 0))
        
        title_label = tk.Label(header_frame, text="Create New Account", 
                              font=('Arial', 20, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(10, 5))
        
        # Signup Card
        signup_card = tk.Frame(main_container, bg='white', relief='flat', 
                              highlightbackground='#e1e8ed', highlightthickness=1)
        signup_card.pack(fill=tk.BOTH, expand=True, padx=10)
        
        signup_frame = tk.Frame(signup_card, bg='white', padx=30, pady=30)
        signup_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        username_frame = tk.Frame(signup_frame, bg='white')
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(username_frame, text="Username", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.signup_username_var = tk.StringVar()
        username_entry = tk.Entry(username_frame, textvariable=self.signup_username_var, 
                                 font=('Arial', 11), bg='#f8f9fa', relief='flat',
                                 highlightbackground='#ddd', highlightthickness=1,
                                 highlightcolor='#3498db')
        username_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        username_entry.focus()
        
        # Email
        email_frame = tk.Frame(signup_frame, bg='white')
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(email_frame, text="Email Address", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.signup_email_var = tk.StringVar()
        email_entry = tk.Entry(email_frame, textvariable=self.signup_email_var, 
                              font=('Arial', 11), bg='#f8f9fa', relief='flat',
                              highlightbackground='#ddd', highlightthickness=1,
                              highlightcolor='#3498db')
        email_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Password
        password_frame = tk.Frame(signup_frame, bg='white')
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(password_frame, text="Password", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.signup_password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=self.signup_password_var, 
                                 font=('Arial', 11), bg='#f8f9fa', relief='flat',
                                 highlightbackground='#ddd', highlightthickness=1,
                                 highlightcolor='#3498db', show="•")
        password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Password requirements
        requirements = tk.Label(signup_frame, 
                               text="🔐 Password must contain: 8+ characters, uppercase, lowercase, numbers, and special characters",
                               font=('Arial', 8), bg='white', fg='#7f8c8d', justify=tk.LEFT)
        requirements.pack(anchor='w', pady=(0, 20))
        
        # Signup Button
        signup_btn = tk.Button(signup_frame, text="🎉 Create Account", 
                              font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                              relief='flat', cursor='hand2',
                              command=self.create_account)
        signup_btn.pack(fill=tk.X, pady=(10, 0), ipady=10)
        signup_btn.bind('<Enter>', lambda e: signup_btn.configure(bg='#219652'))
        signup_btn.bind('<Leave>', lambda e: signup_btn.configure(bg='#27ae60'))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.create_account())
        
        # Login redirect
        redirect_frame = tk.Frame(signup_frame, bg='white')
        redirect_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(redirect_frame, text="Already have an account?", font=('Arial', 9), 
                bg='white', fg='#7f8c8d').pack(side=tk.LEFT)
        
        login_link = tk.Label(redirect_frame, text="Login here", font=('Arial', 9, 'bold'), 
                             bg='white', fg='#3498db', cursor='hand2')
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind('<Button-1>', lambda e: self.show_login_screen())
        login_link.bind('<Enter>', lambda e: login_link.configure(fg='#2980b9'))
        login_link.bind('<Leave>', lambda e: login_link.configure(fg='#3498db'))

    def show_login_screen(self):
        """Show the login screen"""
        # Clear existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - Login")
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f2f5', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(pady=(0, 20))
        
        back_btn = tk.Button(header_frame, text="← Back", font=('Arial', 9), 
                            bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                            command=self.setup_welcome_screen)
        back_btn.pack(anchor='w')
        
        icon_label = tk.Label(header_frame, text="🔓", font=('Arial', 40), bg='#f0f2f5', fg='#2c3e50')
        icon_label.pack(pady=(10, 0))
        
        title_label = tk.Label(header_frame, text="Login to Your Account", 
                              font=('Arial', 20, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(10, 5))
        
        # Login Card
        login_card = tk.Frame(main_container, bg='white', relief='flat', 
                             highlightbackground='#e1e8ed', highlightthickness=1)
        login_card.pack(fill=tk.BOTH, expand=True, padx=10)
        
        login_frame = tk.Frame(login_card, bg='white', padx=30, pady=30)
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        username_frame = tk.Frame(login_frame, bg='white')
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(username_frame, text="Username", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.login_username_var = tk.StringVar()
        username_entry = tk.Entry(username_frame, textvariable=self.login_username_var, 
                                 font=('Arial', 11), bg='#f8f9fa', relief='flat',
                                 highlightbackground='#ddd', highlightthickness=1,
                                 highlightcolor='#3498db')
        username_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        username_entry.focus()
        
        # Password
        password_frame = tk.Frame(login_frame, bg='white')
        password_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(password_frame, text="Password", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.login_password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=self.login_password_var, 
                                 font=('Arial', 11), bg='#f8f9fa', relief='flat',
                                 highlightbackground='#ddd', highlightthickness=1,
                                 highlightcolor='#3498db', show="•")
        password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Login Button
        login_btn = tk.Button(login_frame, text="🔓 Continue to 2FA", 
                             font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                             relief='flat', cursor='hand2',
                             command=self.verify_credentials)
        login_btn.pack(fill=tk.X, pady=(10, 0), ipady=10)
        login_btn.bind('<Enter>', lambda e: login_btn.configure(bg='#2980b9'))
        login_btn.bind('<Leave>', lambda e: login_btn.configure(bg='#3498db'))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.verify_credentials())
        
        # Signup redirect
        redirect_frame = tk.Frame(login_frame, bg='white')
        redirect_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(redirect_frame, text="Don't have an account?", font=('Arial', 9), 
                bg='white', fg='#7f8c8d').pack(side=tk.LEFT)
        
        signup_link = tk.Label(redirect_frame, text="Sign up here", font=('Arial', 9, 'bold'), 
                              bg='white', fg='#27ae60', cursor='hand2')
        signup_link.pack(side=tk.LEFT, padx=(5, 0))
        signup_link.bind('<Button-1>', lambda e: self.show_signup_screen())
        signup_link.bind('<Enter>', lambda e: signup_link.configure(fg='#219652'))
        signup_link.bind('<Leave>', lambda e: signup_link.configure(fg='#27ae60'))

    # ... (The rest of the methods for 2FA verification remain the same as before)
    # [Include all the 2FA-related methods from the previous version here]

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
            
            # Show loading message
            messagebox.showinfo("2FA Required", 
                              f"📧 Sending verification code to {user_email}...\n\n"
                              "Please check your email and enter the 6-digit code.")
            
            # Initiate 2FA process
            code = self.auth_system.two_fa_system.initiate_2fa(username, user_email)
            
            if code:
                self.show_2fa_screen(username, user_email)
            else:
                messagebox.showerror("2FA Error", "❌ Failed to send 2FA code. Please try again.")
        else:
            messagebox.showerror("Authentication Failed", "❌ Invalid username or password.")

    def show_2fa_screen(self, username, user_email):
        """Show the 2FA verification screen"""
        # Clear existing frames
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("🔐 Password Analyzer Pro - 2FA Verification")
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f2f5', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(pady=(0, 20))
        
        icon_label = tk.Label(header_frame, text="📧", font=('Arial', 40), bg='#f0f2f5', fg='#2c3e50')
        icon_label.pack()
        
        title_label = tk.Label(header_frame, text="Two-Factor Authentication", 
                              font=('Arial', 18, 'bold'), bg='#f0f2f5', fg='#2c3e50')
        title_label.pack(pady=(10, 5))
        
        # 2FA Card
        tfa_card = tk.Frame(main_container, bg='white', relief='flat', 
                           highlightbackground='#e1e8ed', highlightthickness=1)
        tfa_card.pack(fill=tk.BOTH, expand=True, padx=10)
        
        tfa_frame = tk.Frame(tfa_card, bg='white', padx=30, pady=30)
        tfa_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = tk.Label(tfa_frame, 
                               text=f"We've sent a verification code to:\n{user_email}",
                               font=('Arial', 11), bg='white', fg='#2c3e50',
                               justify=tk.CENTER)
        instructions.pack(pady=(0, 20))
        
        # 2FA Code Entry
        code_frame = tk.Frame(tfa_frame, bg='white')
        code_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(code_frame, text="Enter 6-digit Code", font=('Arial', 10, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        self.tfa_var = tk.StringVar()
        tfa_entry = tk.Entry(code_frame, textvariable=self.tfa_var, 
                            font=('Arial', 16, 'bold'), bg='#f8f9fa', relief='flat',
                            highlightbackground='#ddd', highlightthickness=1,
                            highlightcolor='#3498db', width=10, justify=tk.CENTER)
        tfa_entry.pack(fill=tk.X, pady=(5, 0), ipady=10)
        tfa_entry.focus()
        
        # Verify Button
        verify_btn = tk.Button(tfa_frame, text="✅ Verify Code", 
                              font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                              relief='flat', cursor='hand2',
                              command=lambda: self.verify_2fa_code(username))
        verify_btn.pack(fill=tk.X, pady=(15, 0), ipady=10)
        
        # Resend Code Button
        resend_btn = tk.Button(tfa_frame, text="🔄 Resend Code", 
                              font=('Arial', 10), bg='#f39c12', fg='white',
                              relief='flat', cursor='hand2',
                              command=lambda: self.resend_2fa_code(username, user_email))
        resend_btn.pack(fill=tk.X, pady=(10, 0), ipady=8)
        
        # Back Button
        back_btn = tk.Button(tfa_frame, text="← Back to Login", 
                            font=('Arial', 9), bg='#95a5a6', fg='white',
                            relief='flat', cursor='hand2',
                            command=self.show_login_screen)
        back_btn.pack(fill=tk.X, pady=(10, 0), ipady=6)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.verify_2fa_code(username))
        
        # Countdown
        self.countdown_time = 600
        self.countdown_label = tk.Label(tfa_frame, font=('Arial', 9), 
                                       bg='white', fg='#e74c3c')
        self.countdown_label.pack(pady=(10, 0))
        self.start_countdown()

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
            launch_main_app(role, username, self.auth_system)  # Pass auth_system
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
    print("🚀 Starting Secure Password Analyzer with Complete Auth System...")
    print("📧 Using email: noreply.alert.banking@gmail.com")
    
    root = tk.Tk()
    auth_system = AuthSystem()
    auth_app = ModernAuthWindow(root, auth_system)
    root.mainloop()

if __name__ == "__main__":
    main()