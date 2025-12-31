import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_system.settings')
django.setup()

from accounts.models import User
from logistics.models import Warehouse, Shipment, Vehicle

def seed_data():
    # Create Dispatcher
    dispatcher, created = User.objects.get_or_create(
        username='dispatcher1',
        defaults={
            'email': 'dispatcher1@example.com',
            'role': 'DISPATCHER',
            'phone_number': '0788123456'
        }
    )
    if created:
        dispatcher.set_password('password123')
        dispatcher.save()
        print("Dispatcher created.")

    # Create Driver
    driver, created = User.objects.get_or_create(
        username='driver1',
        defaults={
            'email': 'driver1@example.com',
            'role': 'DRIVER',
            'phone_number': '0788654321'
        }
    )
    if created:
        driver.set_password('password123')
        driver.save()
        print("Driver created.")

    # Create Vehicle for Driver
    vehicle, created = Vehicle.objects.get_or_create(
        registration_number='RAC 123 A',
        defaults={
            'vehicle_type': 'TRUCK',
            'capacity': 5000,
            'driver': driver
        }
    )
    if created:
        print("Vehicle created.")

    # Create Warehouses
    warehouses_data = [
        ('Rusumo', '500,000kg', 'RUNNING', 'ACTIVE'),
        ('Cyanika', '200,000kg', 'CLOSED', 'FULL'),
        ('Uwizeye', '200,000kg', 'RUNNING', 'AVAILABLE'),
        ('Cyanika', '120,000kg', 'CLOSED', 'AVAILABLE'),
        ('Uwizeye', '400,000kg', 'RUNNING', 'ACTIVE'),
    ]
    for loc, cap, stat, avail in warehouses_data:
        Warehouse.objects.get_or_create(
            location=loc,
            storage_capacity=cap,
            status=stat,
            availability=avail
        )
    print("Warehouses created.")

    # Create some Shipments for Driver
    client = User.objects.filter(role='CLIENT').first()
    if client:
        for i in range(1, 4):
            Shipment.objects.get_or_create(
                tracking_number=f'INV 000{i} R',
                defaults={
                    'sender': client,
                    'recipient_name': f'Recipient {i}',
                    'recipient_address': f'Address {i}',
                    'recipient_contact': '0788000000',
                    'vehicle': vehicle,
                    'status': 'PENDING' if i == 1 else 'IN_TRANSIT' if i == 2 else 'DELIVERED'
                }
            )
        print("Shipments created.")

if __name__ == '__main__':
    seed_data()
