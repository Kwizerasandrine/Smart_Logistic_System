from django.db import models
from django.conf import settings



class Vehicle(models.Model):
    VEHICLE_TYPES = (
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('BIKE', 'Bike'),
    )
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Capacity in kg")
    driver = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicle')

    def __str__(self):
        return f"{self.registration_number} ({self.vehicle_type})"

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    tracking_number = models.CharField(max_length=50, unique=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_shipments')
    recipient_name = models.CharField(max_length=100)
    recipient_address = models.TextField()
    recipient_contact = models.CharField(max_length=15)
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment {self.tracking_number} - {self.status}"

class Warehouse(models.Model):
    STATUS_CHOICES = (
        ('RUNNING', 'Running'),
        ('CLOSED', 'Closed'),
    )
    AVAILABILITY_CHOICES = (
        ('ACTIVE', 'Active'),
        ('AVAILABLE', 'Available'),
        ('FULL', 'Full'),
    )
    
    location = models.CharField(max_length=100)
    storage_capacity = models.CharField(max_length=50, help_text="e.g. 500,000kg")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RUNNING')
    availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.status}"
