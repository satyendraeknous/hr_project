from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from . forms import *
from recycler_management . forms import RecyclerRegisterForm
from hotel_management.models import HotelMaster
from recycler_management.models import RecyclerMaster 
#from sycco_management.models import HotelMaster


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from hotel_management.tokens import account_activation_token
from django.core.mail import EmailMessage



#--------Start Home Page -------->
def mvp(request):
    return render(request, 'mvppage/mvp.html', {})
#--------End Home Page -------->


#--------Start User Registration -------->
def user_registration(request):

    # hotelname = HotelMaster.objects.all()
    city = City.objects.all()
    zip = Zip.objects.all()
    state = State.objects.all()
    country = Country.objects.all()
    if request.method == 'POST':
        user_form = UserForm(data=request.POST,)
        recycler_form = RecyclerRegisterForm(data=request.POST)


        if user_form.is_valid() and recycler_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            group = Group.objects.get(name="Recycler")
            user.groups.add(group)

            recycler = recycler_form.save(commit=False)

            recycler.user = user
            recycler.save()
            ##print recycler
            asd = UserProfile(user=user, phone_no=recycler.recycler_phone_no, company=recycler.recycler_name, group=group)
            #print('asd', asd)
            asd.save()


            #----Start Email verification---->
            current_site = get_current_site(request)
            mail_subject = 'Activate your Hotel Management account.'
            message = render_to_string('hotel_management/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Please check your email and click on given link')
            return HttpResponseRedirect('/hotel_management/conform_email/')
            #return HttpResponse('Please confirm your email address to complete the registration')
        else:
            messages.success(request, 'User already registered on this Zip.')
            #----End Email verification---->
    else:
        user_form = UserForm()
        recycler_form = RecyclerRegisterForm()
    context = {'user_form': user_form, 'recycler_form': recycler_form, 'city':city, 'zip':zip, 'state':state, 'country':country}
    return render(request, 'mvppage/user_registration.html', context)
#--------End User Registration-------->


# #--------OTP Send For Email verify before registration-------->
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponseRedirect('/')
#     else:
#         return HttpResponse('Activation link is invalid!')
# #--------End OTP Send For Email verify before registration-------->








#--------Start User Login-------->
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                groups = User.objects.filter(username=user, groups__name='Hotel').exists()
                groups1 = User.objects.filter(username=user, groups__name='Recycler').exists()
                groups2 = User.objects.filter(username=user, groups__name='Sycco').exists()
                
                if (groups and user.is_active) or user.is_superuser:
                    login(request, user)
                    return redirect("/hotel_management/hotel_dashboard")

                elif groups1 and user.is_active:
                    login(request, user)
                    return redirect("/recycler_management/recycler_dashboard")

                elif groups2 and user.is_active:
                    login(request, user)
                    return redirect("/sycco_management/sycco_dashboard")
                
        else:
            messages.success(request, 'Invalid Login.')
            #return HttpResponse("Invalid")
    else:
        form = AuthenticationForm()
    return render(request, 'mvppage/user_login.html', {'form': form})
#--------End User Login-------->


#--------Start User Logout -------->
@login_required(login_url='/user_login/')
def user_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Successfully Logout')
    return redirect('user_login')
#--------End User Logout -------->



#--------start User Password Change-------->
@login_required(login_url='/user_login/')
def user_passwordchange(request): 
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_login')
        else:
            messages.success(request, 'Your password Not matched!')
            #return HttpResponse('invalid!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'mvppage/user_passwordchange.html', {'form': form})
#--------End User Password Change-------->






# #--------Start SyccoProfile Registration -------->
# def sycco_registration(request):

#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST,)
#         sycco_form = SyccoProfileForm(data=request.POST)

#         if user_form.is_valid() and sycco_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.is_active = True
#             user.save()

#             syccoprof = sycco_form.save(commit=False)
#             syccoprof.user = user
#             syccoprof.save()
#             #print syccoprof
#             # asd = UserProfile(user=user, phone_no=recycler.recycler_phone_no, company=recycler.recycler_name)
#             # #print('asd', asd)
#             # asd.save()
#             return redirect('/')
#         else:
#             return HttpResponse('Invalid registered.')
#     else:
#         user_form = UserForm()
#         sycco_form = SyccoProfileForm()
#     context = {'user_form': user_form, 'sycco_form': sycco_form, }
#     return render(request, 'mvppage/sycco_registration.html', context)
# #--------Start SyccoProfile Registration-------->




# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             #Select_Group = form.cleaned_data["Select_Group"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 groups = User.objects.filter(username=user, groups__name='Hotel').exists()
#                 groups1 = User.objects.filter(username=user, groups__name='Recycler').exists()
#                 groups2 = User.objects.filter(username=user, groups__name='Sycco').exists()
    
#                 if groups or request.user.is_superuser:
#                     login(request, user)
#                     return redirect("/hotel_management/hotel_dashboard")

#                 # elif request.user.is_superuser:
#                 #     login(request, user)
#                 #     return redirect("/hotel_management/hotel_dashboard")
#                 elif groups1 and user.is_active:
#                     login(request, user)
#                     return redirect("/recycler_management/recycler_dashboard")

#                 elif groups2 and user.is_active:
#                     login(request, user)
#                     return redirect("/sycco_management/sycco_dashboard")

#                 # else:
#                 #     login(request, user)
#                 #     return redirect('/hotel_management/hotel_home')
#         else:
#             return HttpResponse("Invalide")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'mvppage/user_login.html', {'form': form})





# #--------Start User Registration -------->
# def user_registration(request):

#     aa = RecyclerMaster.objects.all()
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST,)
#         profile_form = UserProfileForm(data=request.POST)
#         #recycler_form = RecyclerMaster(data=request.POST)
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)

#             user.is_active = True
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             #print profile
#             return redirect('/')
#         else:
#             return HttpResponse('Invalid registered.')
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
        
#     context = {'user_form': user_form, 
#                 'profile_form': profile_form, 'aa':aa,
#             }
#     return render(request, 'mvppage/user_registration.html', context)
# #--------End User Registration-------->













# #--------Start User Registration -------->
# def user_registration(request):

#     aa = RecyclerMaster.objects.all()
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST,)
#         profile_form = UserProfileForm(data=request.POST)
#         #recycler_form = RecyclerMaster(data=request.POST)
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)

#             user.is_active = True
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             #print profile
#             return redirect('/')
#         else:
#             return HttpResponse('Invalid registered.')
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
        
#     context = {'user_form': user_form, 
#                 'profile_form': profile_form, 'aa':aa,
#             }
#     return render(request, 'mvppage/user_registration.html', context)
# #--------End User Registration-------->


















# #--------Start User Registration -------->
# def user_registration(request):
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST,)
#         profile_form = UserProfileForm(data=request.POST)
    
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)

#             # group = Group.objects.get(name=request.POST.get('Select_Group'))
#             # user.groups.add(group)

#             user.is_active = True
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             #print profile
#             return redirect('/')
#         else:
#             return HttpResponse('Invalid registered.')
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
        
#     context = {'user_form': user_form, 
#                 'profile_form': profile_form, 
#             }
#     return render(request, 'mvppage/user_registration.html', context)
# #--------End User Registration-------->





# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     #return HttpResponse("Successfully Login")
#                     return redirect('hotel_management/hotel_dashboard')
#                 else:
#                     return HttpResponse("Invalid")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'mvppage/user_login.html', {'form': form})
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             #Select_Group = form.cleaned_data["Select_Group"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 groups = User.objects.filter(username=user, groups__name='Hotel').exists()
#                 if groups and user.is_active:
#                     login(request, user)
#                     return redirect("/hotel_management/hotel_dashboard")

#                 elif request.user.is_superuser:
#                     login(request, user)
#                     return redirect("/hotel_management/hotel_dashboard")

#                 else:
#                     login(request, user)
#                     return redirect('/hotel_management/hotel_home')
#         else:
#             return HttpResponse("Invalide")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'mvppage/user_login.html', {'form': form})