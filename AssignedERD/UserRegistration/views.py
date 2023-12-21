from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Destination
from .forms import UserLogin, UserRegistration
from django.http import HttpResponse

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
    else:
        request.session.clear()
    
    context = {
        'destination': destination,
        'user': user,
        'admin': admin,
    }
    
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
                        return redirect('/add_wishlist/')
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
    
def manage_bookings(request):
    admin = User.objects.get(user_id=request.session.get('admin_id'))
    
    return render(request, 'manage_bookings.html', {'admin':admin})    

def manage_destinations(request):
    destination = Destination.objects.all()
    admin = User.objects.get(user_id=request.session.get('admin_id'))

    context = {
        'admin': admin,
        'destination': destination,
    }

    return render(request, 'manage_destinations.html', context)

def display_destination(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    request.session['destination_id'] = destination.destination_id
    
    user = None
    admin = None
    in_wishlist = None
    
    if request.session.get('user_validated'):
        user = User.objects.get(user_id=request.session.get('user_id'))
        in_wishlist = destination in user.wishlist.all()
    elif request.session.get('admin_validated'):
        admin = User.objects.get(user_id=request.session.get('admin_id'))
        in_wishlist = destination in admin.wishlist.all()
        
    context = {
        'destination': destination,
        'in_wishlist': in_wishlist
    }
    
    return render(request, 'display_destination.html', context)

def display_wishlist(request):
    admin = None
    user = None
    if request.session.get('admin_validated'):
        admin = User.objects.get(user_id=request.session.get('admin_id'))
    else:
        user = User.objects.get(user_id=request.session.get('user_id'))
    
    context = {
        'user': user,
        'admin': admin,
    }
    
    return render(request, 'my_wishlist.html', context)

def add_wishlist(request):
    destination = Destination.objects.get(destination_id=request.session.get('destination_id'))
    
    if request.session.get('user_validated'):
        user = User.objects.get(user_id=request.session.get('user_id'))
        user.wishlist.add(destination)
        user.save()
        
        return redirect('/destination/' + str(destination.destination_id))
    elif request.session.get('admin_validated'):
        admin = User.objects.get(user_id=request.session.get('admin_id'))
        admin.wishlist.add(destination)
        admin.save()
    else:
        request.session['on_destination'] = True
        return redirect('/signin/')
