
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = 'admin'
    password = 'adminpassword123'
    email = 'admin@example.com'
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists.")
        user = User.objects.get(username=username)
        # Ensure role is ADMIN
        if user.role != 'ADMIN':
            user.role = 'ADMIN'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"Updated '{username}' role to ADMIN.")
        else:
            print(f"User '{username}' is already an ADMIN.")
    else:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.role = 'ADMIN'
        user.save()
        print(f"Created superuser '{username}' with role ADMIN.")
        print(f"Password: {password}")

if __name__ == '__main__':
    create_admin()
