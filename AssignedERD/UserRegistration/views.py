from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Destination, BookOrder, Wishlist
from .forms import UserLogin, UserRegistration
from django.http import HttpResponse
from django.db import connection

# Create your views here.

def home(request):
    destination = Destination.objects.all()
    user_validated = request.session.get('user_validated', None)
    admin_validated = request.session.get('admin_validated', None)
    admin = None
    user = None
    
    if admin_validated:
        admin = User.objects.get(user_id=request.session.get('admin_id'))
    elif user_validated:
        user = User.objects.get(user_id=request.session.get('user_id'))
    
    context = {
        'destination': destination,
        'user': user,
        'admin': admin,
    }

    print(destination)
    return render(request, 'home.html', context)

def register(request):
    form = UserRegistration()
    request.session['registration_status'] = None
    
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            contact_number = form.cleaned_data['contact_number']
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                request.session['registration_status'] = False

            else:
                user = User(username=username, email=email, password=password, first_name=first_name,
                            last_name=last_name, contact_number=contact_number
                            )
                user.save()
                request.session.clear()
                
                return redirect('/signin/')
        
    return render(request, 'register.html', {'form':form})

def sign_in(request):
    form = UserLogin()
    request.session['registered'] = None
    destination_id = request.session.get('destination_id', None)

    if request.method == 'POST':
        form = UserLogin(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(username=username)
                
                if user.check_admin(user.usertype):
                    request.session['admin_validated'] = True
                    request.session['admin_id'] = user.user_id
                    
                    return redirect('/')
                elif user.check_password(password):
                    request.session['user_validated'] = True
                    request.session['user_id'] = user.user_id

                    if request.session.get('on_destination'):
                        return redirect('/destination/' + str(destination_id))
                    elif request.session.get('on_bookings'):
                        return redirect('/book_order/')
                    else:
                        return redirect('/')
                else:
                    request.session['user_validated'] = False
                    
            except User.DoesNotExist:
                request.session['registered'] = False
            
        else:
            return HttpResponse('Invalid')

    return render(request, 'signin.html', {'form': form})

def sign_out(request):
    request.session.clear()
    
    return redirect('/')

def my_account(request):
    user_validated = request.session.get('user_validated', None)
    admin_validated = request.session.get('admin_validated', None)
    user = None
    admin = None
    
    if admin_validated:
        admin = User.objects.get(user_id=request.session.get('admin_id'))
    elif user_validated:
        user = User.objects.get(user_id=request.session.get('user_id'))
    
    context = {
        'user': user,
        'admin': admin,
    }
    
    return render(request, 'my_account.html', context)

def my_bookings(request):
    user_id = request.session.get('user_id', None)

    if user_id is not None:
        with connection.cursor() as cursor:
            cursor.callproc('getOrders', [user_id])
            results = cursor.fetchall()

            bookings_with_status = [
                {
                    'destination': Destination(*row[:-1]),
                    'status': row[-1]
                }

                for row in results
            ]

            approved = [
                order['destination'] for order in bookings_with_status if order['status'] == 1
            ]
            pending = [
                order['destination'] for order in bookings_with_status if order['status'] == 0
            ]
            failed = [
                order['destination'] for order in bookings_with_status if order['status'] == 2
            ]

            context = {
                'approved': approved,
                'pending': pending,
                'failed': failed,
            }

            return render(request, 'my_bookings.html', context)
    else:
        return redirect('/signin/')

def manage_bookings(request):
    admin_validated = request.session.get('admin_validated', None)

    if admin_validated:
        admin = User.objects.get(user_id=request.session.get('admin_id'))
    
        return render(request, 'manage_bookings.html', {'admin': admin})
    else:
        return redirect('/signin')

def manage_destinations(request):
    admin_validated = request.session.get('admin_validated', None)

    if admin_validated:
        destination = Destination.objects.all()
        admin = User.objects.get(user_id=request.session.get('admin_id'))

        context = {
            'admin': admin,
            'destination': destination,
        }

        return render(request, 'manage_destinations.html', context)
    else:
        return redirect('/signin/')

def display_destination(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    request.session['destination_id'] = destination.destination_id
    request.session['on_destination'] = True
    user_validated = request.session.get('user_validated', None)

    if user_validated:
        user_id = request.session.get('user_id')
        request.session['in_bookings'] = BookOrder.objects.filter(user_id=user_id, destination_id=destination.destination_id).exists()
        request.session['in_wishlist'] = Wishlist.objects.filter(user_id=user_id, destination_id=destination.destination_id).exists()

    context = {
        'destination': destination
    }
    
    return render(request, 'display_destination.html', context)

def display_wishlist(request):
    user_validated = request.session.get('user_validated', None)

    if user_validated:
        user_id = request.session.get('user_id')

        with connection.cursor() as cursor:
            cursor.callproc('getWishlist', [user_id])
            results = cursor.fetchall()

            destination = [Destination(
                destination_id=row[0],
                destination_name=row[1],
                image=row[4],
            ) for row in results]

        context = {
            'destination': destination,
        }

        return render(request, 'my_wishlist.html', context)
    else:
        return redirect('/signin/')

def add_wishlist(request):
    user_validated = request.session.get('user_validated')
    destination = Destination.objects.get(destination_id=request.session.get('destination_id'))
    
    if user_validated:
        user = User.objects.get(user_id=request.session.get('user_id'))
        wishlist = Wishlist.objects.create(
            user_id=user,
            destination_id=destination
        )
        
        return redirect('/destination/' + str(destination.destination_id))
    else:
        return redirect('/signin/')

def add_book_order(request):
    destination_id = request.session.get('destination_id')

    if request.session.get('user_validated'):
        user = User.objects.get(user_id=request.session.get('user_id'))
        destination = Destination.objects.get(destination_id=destination_id)
        book_order = BookOrder.objects.create(
            user_id = user,
            destination_id = destination
        )

        context = {
            'book_order': book_order,
        }

        return redirect('/destination/' + str(destination_id))
    else:
        return redirect('/signin/')

def edit_destination(request, destination_id):
    admin = None

    if request.session.get('admin_validated'):
        admin = User.objects.get(user_id=request.session.get('admin_id'))
    else:
        return redirect('/signin/')

    destination = get_object_or_404(Destination, pk=destination_id)
    request.session['destination_id'] = destination.destination_id

    context = {
        'admin': admin,
        'destination': destination,
    }

    return render(request, 'edit_destination.html', context)

def book_order(request):
    user = None
    destination = Destination.objects.all()

    if request.session.get('user_validated'):
        user = User.objects.get(user_id=request.session.get('user_id'))

        context = {
            'user': user,
            'destination': destination,
        }

        return render(request, 'book_order.html', context)
    else:
        request.session['on_bookings'] = True
        return redirect('/signin/')
