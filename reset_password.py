
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password():
    username = 'admin'
    password = 'min12345' # Simpler password
    
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"SUCCESS: Password for '{username}' has been reset to '{password}'.")
    except User.DoesNotExist:
        print(f"ERROR: User '{username}' does not exist.")

if __name__ == '__main__':
    reset_password()
