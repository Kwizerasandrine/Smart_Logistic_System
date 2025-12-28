
import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_system.settings')
django.setup()

def verify_admin_login():
    username = 'admin'
    password = 'adminpassword123'
    
    user = authenticate(username=username, password=password)
    if user is not None:
        print(f"SUCCESS: Authentication valid for user '{username}'.")
        print(f"User Active: {user.is_active}")
        print(f"User Role: {user.role}")
    else:
        print(f"FAILURE: Authentication failed for user '{username}'.")

if __name__ == '__main__':
    verify_admin_login()
