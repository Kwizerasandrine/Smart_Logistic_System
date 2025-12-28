
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Shipment, Vehicle
from django.contrib.auth import get_user_model

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.role == 'CLIENT':
        context['shipments'] = Shipment.objects.filter(sender=user).order_by('-created_at')
        context['active_count'] = context['shipments'].exclude(status__in=['DELIVERED', 'CANCELLED']).count()
        
        
        context['stat_pending'] = context['shipments'].filter(status='PENDING').count()
        context['stat_in_transit'] = context['shipments'].filter(status='IN_TRANSIT').count()
        context['stat_delivered'] = context['shipments'].filter(status='DELIVERED').count()
        
    elif user.role == 'DRIVER':
        
        if hasattr(user, 'vehicle'):
            context['vehicle'] = user.vehicle
            context['assigned_shipments'] = Shipment.objects.filter(vehicle=user.vehicle, status__in=['PENDING', 'IN_TRANSIT'])
        else:
            context['vehicle'] = None
            context['assigned_shipments'] = []
            
    elif user.role == 'ADMIN':
        User = get_user_model()
        context['total_users'] = User.objects.count()
        context['total_shipments'] = Shipment.objects.count()
        context['pending_count'] = Shipment.objects.filter(status='PENDING').count()
        context['in_transit_count'] = Shipment.objects.filter(status='IN_TRANSIT').count()
        context['delivered_count'] = Shipment.objects.filter(status='DELIVERED').count()
        
        context['recent_shipments'] = Shipment.objects.all().order_by('-created_at')[:5]
        context['recent_users'] = User.objects.all().order_by('-date_joined')[:5]
        
    return render(request, 'logistics/dashboard_v2.html', context)

@user_passes_test(is_admin)
def admin_drivers(request):
    User = get_user_model()
    drivers = User.objects.filter(role='DRIVER').order_by('-date_joined')
    return render(request, 'logistics/admin_drivers.html', {'drivers': drivers})

@user_passes_test(is_admin)
def admin_users(request):
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'logistics/admin_users.html', {'users': users})

@user_passes_test(is_admin)
def admin_deliveries(request):
    shipments = Shipment.objects.all().order_by('-created_at')
    return render(request, 'logistics/admin_deliveries.html', {'shipments': shipments})

@user_passes_test(is_admin)
def admin_warehouses(request):
    return render(request, 'logistics/coming_soon.html', {'title': 'Warehouses'})

@user_passes_test(is_admin)
def admin_feedback(request):
    return render(request, 'logistics/coming_soon.html', {'title': 'Feedback'})

@user_passes_test(is_admin)
def admin_settings(request):
    return render(request, 'logistics/coming_soon.html', {'title': 'Settings'})

@login_required
def client_shipments(request):
    shipments = Shipment.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'logistics/admin_deliveries.html', {'shipments': shipments, 'title': 'My Shipments'})

@login_required
def driver_tasks(request):
    if hasattr(request.user, 'vehicle'):
        shipments = Shipment.objects.filter(vehicle=request.user.vehicle, status__in=['PENDING', 'IN_TRANSIT']).order_by('-created_at')
    else:
        shipments = []
    return render(request, 'logistics/admin_deliveries.html', {'shipments': shipments, 'title': 'My Tasks'})
