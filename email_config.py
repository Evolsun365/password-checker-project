# email_config.py
"""
Email Configuration for 2FA System
Update these values with your actual email credentials
"""

# Gmail Configuration (Recommended)
SMTP_CONFIG = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'username': 'your-email@gmail.com',  # Your Gmail address
    'password': 'your-app-password'      # Gmail App Password (see instructions below)
}

# Outlook/Hotmail Configuration
# SMTP_CONFIG = {
#     'server': 'smtp-mail.outlook.com',
#     'port': 587,
#     'username': 'your-email@outlook.com',
#     'password': 'your-password'
# }

# Yahoo Mail Configuration
# SMTP_CONFIG = {
#     'server': 'smtp.mail.yahoo.com',
#     'port': 587,
#     'username': 'your-email@yahoo.com',
#     'password': 'your-app-password'
# }