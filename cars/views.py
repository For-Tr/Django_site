import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt

from .forms import CreateUserForm, LoginForm, ParkingSpaceForm
from django.db.models import Sum

from django.contrib.auth.models import auth, User

from django.contrib.auth.decorators import login_required


from django.contrib import messages


from .models import ParkingSpace, RentalRecord
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


from django.contrib.auth import authenticate, login, logout


def homepage(request):
    return render(request, 'cars/index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            return redirect("loginpage")

        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        # Perform custom validation if needed
        print(username)
        if not username or not email or not password or not confirm_password:
            return JsonResponse({'error': 'Please fill all the fields'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

            # Create a new user
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Registration successful'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def login1(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username)
        # Perform custom validation if needed
        if not username or not password:
            return JsonResponse({'error': 'Please provide username and password'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url="loginpage")
def user_orders(request):
    user = request.user
    if not user.is_staff:
        return HttpResponseForbidden
    # The User model needs to be created
    users = User.objects.all()
    user_orders_dict = {user: user.orders.all() for user in users}
    return render(request, 'user_orders.html', {'user_orders_dict': user_orders_dict})


@login_required(login_url="loginpage")
def send_emails_to_all_users(request, subject, message, from_email):
    user = request.user
    if not user.is_staff:
        return HttpResponseForbidden

    users = User.objects.all()
    for user in users:
        try:
            send_mail(
                subject,
                message,
                from_email,
                [user.email],
                fail_silently=False,
            )
            print(f"Email has been sent to: {user.email}")
        except Exception as e:
            print(f"There was an error sending an email to {user.email}:{e}")


def loginpage(request):

    return render(request, 'loginpage.html')


def user_logout(request):

    auth.logout(request)

    return redirect("")


@login_required(login_url="loginpage")
def dashboard(request):
    return render(request, 'cars/dashboard.html')


@login_required(login_url="loginpage")
def parking_space_list(request):
    spaces = ParkingSpace.objects.all()
    return render(request, 'cars/parking_space_list.html', {'spaces': spaces})


@login_required(login_url="loginpage")
def parking_space_detail(request, id):
    space = get_object_or_404(ParkingSpace, id=id)
    record = RentalRecord()
    record.provider = request.user
    record.parking_space = space
    record.price = space.hourly_price
    record.save()
    return render(request, 'cars/parking_space_detail.html', {'space': space})


@login_required(login_url="loginpage")
def parking_space_create(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            space = form.save(commit=False)
            space.owner = request.user
            print(space)
            space.save()
            return redirect('parking_space_list')
    else:
        form = ParkingSpaceForm()
    return render(request, 'cars/parking_space_form.html', {'form': form})


@login_required(login_url="loginpage")
def parking_space_update(request, id):
    user = request.user
    if not user.is_staff:
        return HttpResponseForbidden()
    space = get_object_or_404(ParkingSpace, id=id, owner=request.user)
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            return redirect('parking_space_list')
    else:
        form = ParkingSpaceForm(instance=space)
    return render(request, 'cars/parking_space_form.html', {'form': form})


@login_required(login_url="loginpage")
def parking_space_delete(request, id):
    user = request.user

    space = get_object_or_404(ParkingSpace, id=id)
    if request.method == 'POST':
        space.delete()
        return redirect('parking_space_list')
    return render(request, 'cars/parking_space_confirm_delete.html', {'space': space})


@login_required
def provider_rental_history(request):
    provider = request.user
    rental_records = RentalRecord.objects.filter(provider=provider)




    context = {
        'rental_records': rental_records,
    }
    return render(request, 'cars/provider_rental_history.html', context)
@login_required
def provider_total_earning(request):
    provider = request.user
    total_earning = RentalRecord.objects.filter(parking_space__owner=provider).aggregate(
        total_earning=Sum('price')).get('total_earning') or 0.00
    context = {
        'total_earning': total_earning,
    }
    return render(request, 'cars/provider_total_earning.html', context)


@login_required
def view_customer_info(request, customer_id):
    user = get_object_or_404(User, id=customer_id)
    if request.user.is_staff or request.user.groups.filter(name='provider').exists():
        print(user)
        context = {
            'customer': user,
        }
        return render(request, 'cars/view_customer_info.html', context)
    # else:
    #     return HttpResponseForbidden
