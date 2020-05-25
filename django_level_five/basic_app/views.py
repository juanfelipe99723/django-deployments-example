from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileForm


from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('you are login')

def register(request):
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password) #enmascara el password
            user.save() #se guarda el usuario

            profile=profile_form.save(commit=False) # commit en false para no guardar inmediatamente en la BD
            profile.user=user #relación 1-1

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form=UserForm()
        profile_form= UserProfileForm()

    return render(request, 'basic_app/registration.html', 
                    {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))


            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        
        else:
            print("alguien trato de entrar y fallo")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid Credentials")
    else:
        return render(request,'basic_app/login.html',{})
    
