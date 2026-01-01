from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Shipment, Vehicle, Warehouse
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.forms import UserRegistrationForm, UserEditForm, AdminUserCreationForm
from .forms import ShipmentForm
from django.shortcuts import get_object_or_404
import uuid

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

def is_dispatcher(user):
    return user.is_authenticated and (user.role == 'DISPATCHER' or user.role == 'ADMIN')

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
        # Add more stats for Driver Dashboard matching the image
        all_driver_shipments = Shipment.objects.filter(vehicle__driver=user)
        context['shipments'] = all_driver_shipments.order_by('-created_at')
        context['stat_delivered'] = all_driver_shipments.filter(status='DELIVERED').count()
        context['stat_pending'] = all_driver_shipments.filter(status='PENDING').count()
        context['stat_in_transit'] = all_driver_shipments.filter(status='IN_TRANSIT').count()
        
        if hasattr(user, 'vehicle'):
            context['vehicle'] = user.vehicle
            context['assigned_shipments'] = all_driver_shipments.filter(status__in=['PENDING', 'IN_TRANSIT'])
        else:
            context['vehicle'] = None
            context['assigned_shipments'] = []
            
    elif user.role == 'DISPATCHER':
        User = get_user_model()
        context['total_shipments'] = Shipment.objects.count()
        context['pending_count'] = Shipment.objects.filter(status='PENDING').count()
        context['in_transit_count'] = Shipment.objects.filter(status='IN_TRANSIT').count()
        context['delivered_count'] = Shipment.objects.filter(status='DELIVERED').count()
        context['total_drivers'] = User.objects.filter(role='DRIVER').count()
        context['recent_shipments'] = Shipment.objects.all().order_by('-created_at')[:8]
        
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

@login_required
def create_shipment(request):
    if request.user.role != 'CLIENT':
        messages.error(request, 'Only clients can create shipments.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.sender = request.user
            # Generate unique tracking number
            tracking_number = f"SLS-{str(uuid.uuid4())[:8].upper()}"
            shipment.tracking_number = tracking_number
            shipment.status = 'PENDING'
            shipment.save()
            messages.success(request, f'Shipment created successfully! Your tracking number is: {tracking_number}')
            return redirect('client_shipments')
    else:
        form = ShipmentForm()
    
    return render(request, 'logistics/create_shipment.html', {'form': form})

@user_passes_test(is_dispatcher)
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
    shipments = Shipment.objects.filter(vehicle__driver=request.user, status__in=['PENDING', 'IN_TRANSIT']).order_by('-created_at')
    return render(request, 'logistics/admin_deliveries.html', {'shipments': shipments, 'title': 'My Tasks'})

@user_passes_test(is_dispatcher)
def dispatcher_deliveries(request):
    from django.utils import timezone
    from datetime import timedelta
    
    shipments = Shipment.objects.all().order_by('-created_at')
    
    # Calculate weekly trend data
    today = timezone.now().date()
    labels = []
    delivered_trend = []
    total_trend = []
    active_trend = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d %b'))
        
        day_shipments = shipments.filter(created_at__date=day)
        total_trend.append(day_shipments.count())
        delivered_trend.append(day_shipments.filter(status='DELIVERED').count())
        active_trend.append(day_shipments.filter(status='IN_TRANSIT').count())

    context = {
        'shipments': shipments,
        'title': 'Deliveries Management Panel',
        'delivered_count': shipments.filter(status='DELIVERED').count(),
        'pending_count': shipments.filter(status='PENDING').count(),
        'in_transit_count': shipments.filter(status='IN_TRANSIT').count(),
        'labels': labels,
        'delivered_trend': delivered_trend,
        'total_trend': total_trend,
        'active_trend': active_trend,
    }
    return render(request, 'logistics/dispatcher_deliveries.html', context)

@user_passes_test(is_dispatcher)
def dispatcher_warehouses(request):
    warehouses = Warehouse.objects.all().order_by('-created_at')
    return render(request, 'logistics/dispatcher_warehouses.html', {'warehouses': warehouses})

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully!")
            return redirect('admin_users')
    else:
        form = AdminUserCreationForm()
    return render(request, 'logistics/add_user.html', {'form': form})

@user_passes_test(is_admin)
def edit_user(request, pk):
    User = get_user_model()
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {target_user.username} updated successfully!")
            return redirect('admin_users')
    else:
        form = UserEditForm(instance=target_user)
    return render(request, 'logistics/edit_user.html', {'form': form, 'target_user': target_user})

@user_passes_test(is_admin)
def delete_user(request, pk):
    User = get_user_model()
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f"User {username} deleted successfully!")
    return redirect('admin_users')
