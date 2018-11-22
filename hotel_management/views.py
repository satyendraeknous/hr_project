# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from hotel_recycler_management.forms import *
from . forms import *
from django.http import HttpResponseRedirect, HttpResponse, Http404
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sycco_management .models import SyccoMaster, SyccoProfile
from django.contrib.auth import authenticate, login, logout




from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


#test for git


#--------Start Home Page-------->
# def hotel_home(request):
#     return render(request, 'hotel_management/hotel_home.html', {})
#--------End Home Page-------->

def conform_email(request):
    return render(request, 'hotel_management/conform_email.html', {})

def invalid_email(request):
    return render(request, 'hotel_management/invalid_email.html', {})


#--------Start hotel search by Zip-------->
def hotel_search(request):
    rform = HotelsearchForm(request.POST or None)
    if request.method == 'POST':
        zip = Zip.objects.filter(zip=request.POST.get('hotel_zip'))
        print('zip', str(zip))
        if not zip:
            context = {'frm': rform, }
            messages.error(request, 'Please enter valid zip')
            return render(request, 'hotel_management/hotel_search.html', context)
        else:
            getfilter = HotelMaster.objects.filter(hotel_zip=zip)
            context = {'frm': rform, 'getfilter': getfilter, }
    else:
        context = {'frm': rform, }
    return render(request, 'hotel_management/hotel_search.html', context)
#--------End hotel search by Zip-------->


# #--------Start hotel search by Zip-------->
# def hotel_search(request):
#     rform = HotelsearchForm(request.POST or None)
#     if request.method == 'POST':
#         getValue = request.POST.get('hotel_zip')
#         #print getValue
#         zip = Zip.objects.get(zip=getValue)
#         getfilter = HotelMaster.objects.filter(hotel_zip=zip)
#         #print getfilter
#         context = {'frm': rform, 'getfilter': getfilter}
#     else:
#         #rform = HotelsearchForm()
#         context = {'frm': rform}
#     return render(request, 'hotel_management/hotel_search.html', context)
# #--------End hotel search by Zip-------->


#--------Start hotel search by Zip details-------->
def hotel_details(request, pk):
    instance = get_object_or_404(HotelMaster, hotel_id=pk)
    return render(request, "hotel_management/hotel_search_details.html", {"instance": instance})
#--------End hotel search by Zip details-------->


#--------Start User Registration for Hotel-------->
def hotel_register(request, pk): 

    instance = get_object_or_404(HotelMaster, hotel_id=pk)
    if request.method == 'POST':
        user_form = UserForm(data=request.POST,)
        profile_form = UserProfileForm(data=request.POST)

        #----User_Count for Hotel Registration---->
        hotelname = HotelMaster.objects.get(hotel_id=instance.hotel_id)
        count_user = UserProfile.objects.filter(company=hotelname).count()
        #print('count_user', count_user)
        if count_user <= 2:

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.is_active = False
                user.save()

                group = Group.objects.get(name="Hotel")
                user.groups.add(group)

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                #print profile

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
                messages.success(request, 'Invalid registered by You.')
                #return HttpResponse('Invalid registered by You.')
        else:
            #return HttpResponse('Sorry! Three User already registered.')
            messages.success(request, 'Sorry! Three User already registered.')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 
                'profile_form': profile_form, 
                'instance': instance,
            }
    return render(request, 'hotel_management/hotel_register.html', context)
#--------End User Registration for Hotel-------->


#--------OTP Send For Email verify before registration-------->
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Successfully registered please login here')
        return HttpResponseRedirect('/')
    else:
        messages.success(request, 'Activation link is invalid!')
        return HttpResponseRedirect('/hotel_management/invalid_email/')
        #return HttpResponse('Activation link is invalid!')
#--------End OTP Send For Email verify before registration-------->


#--------Start Hoteldashboard-------->
@login_required(login_url='/user_login/')
def hotel_dashboard(request): 

    queryset = LoadDashboard.objects.filter(user_id=request.user).order_by('-load_no')

    #----star top box data---->
    total = LoadDashboard.objects.filter(user_id=request.user).count()
    total_open = LoadDashboard.objects.filter(user_id=request.user).filter(status='Processing').count()
    total_aknwlge = LoadDashboard.objects.filter(user_id=request.user).filter(status='Acknowledge').count()
    total_close = LoadDashboard.objects.filter(user_id=request.user).filter(status='Close').count()

    #----Show Remark table in Notifications box---->
    remarkloadss = []
    for query1 in queryset:
    
        rmrkload = query1.load_no
        remarkload = Remark.objects.filter(load_remark=rmrkload).order_by('-date')
        remarkloadss += remarkload

    context = {
        'queryset': queryset, 
        'remarkload':remarkloadss, 
        'total':total,
        'total_open':total_open, 
        'total_aknwlge':total_aknwlge,
        'total_close':total_close,
    }
    return render(request, 'hotel_management/hotel_dashboard.html', context)
#--------End Hoteldashboard-------->







#--------Start Hoteldashboarddetails-------->
@login_required(login_url='/user_login/')
def hotel_dashboarddetails(request, pk):
    instance = get_object_or_404(LoadDashboard, load_no=pk)
    remarkload = Remark.objects.filter(load_remark=instance.load_no).order_by('-date')
    context = {
        'instance':instance, 'remarkload':remarkload,
    }
    return render(request, "hotel_management/hotel_dashboarddetails.html", context)
#--------End Hoteldashboarddetails-------->


#--------Start Hoteldashboardhoteldetail-------->
@login_required(login_url='/user_login/')
def hotel_dashboardhoteldetail(request, pk):
    loadobject = LoadDashboard.objects.select_related().get(pk=pk)
    #print ("HM: ", loadobject.hotel_id.hotel_name)
    getcompany = loadobject.hotel_id.hotel_name
    instance = get_object_or_404(SyccoMaster, company_name=getcompany)
    return render(request, 'hotel_management/hotel_dashboardhoteldetail.html', {'instance': instance})
#--------End Hoteldashboardhoteldetail-------->



#--------Start HoteldashboardCreate-------->
@login_required(login_url='/user_login/')
def hotel_dashboardCreate(request):

    product = Product.objects.all()
    category = Category.objects.all()
    if request.method == 'POST':
        form = HoteldashboardcreateForm(data=request.POST)
        ##print form
        if form.is_valid():

            form1 = form.save(commit=False)
            form1.user_id = User.objects.get(username=request.user)
            #----statr Sycco Green Point---->
            loadweight = form1.weight
            # #print('loadweight', loadweight)
            # #print type(loadweight)
            #userget = User.objects.get(username=request.user)
            userprobject = UserProfile.objects.get(user=request.user)
            form1.hotel_id = HotelMaster.objects.get(hotel_name=userprobject.company)
            hotelname = form1.hotel_id
            ##print('hotel_name', form1.hotel_id.hotel_name)
            syccomaster = SyccoMaster.objects.get(company_name=hotelname.hotel_name)
            ##print('syccomaster', syccomaster.company_name)

            syccogreenpoint = ""
            sycmstrtotlgrnpt = 0
            tamount = 0
            syccoamount = ""
            syccoamount = syccomaster.amount
            ##print('syccoamount', syccoamount)
            syccogreenpoint = syccomaster.green_point
            ##print('syccogreenpoint', syccogreenpoint)

            if syccomaster.total_amount:
                tamount = syccomaster.total_amount
               # #print('tamount', tamount)

            if syccomaster.total_greenpoint:
                sycmstrtotlgrnpt = syccomaster.total_greenpoint
               # #print ('sycmstrtotlgrnpt', sycmstrtotlgrnpt)
               # #print type(sycmstrtotlgrnpt)

            sycototlgrnpt = int(loadweight)*syccogreenpoint 
            ##print('sycototlgrnpt', sycototlgrnpt)
            syctotlamount = int(sycototlgrnpt)*syccoamount/syccogreenpoint
            ##print('syctotlamount', syctotlamount)

            #----SyccoMaster table Update---->
            syccomaster.total_greenpoint = sycmstrtotlgrnpt+sycototlgrnpt
            syccomaster.total_amount = tamount+syctotlamount
            syccomaster.save()
            #----End Sycco Green Point---->

            form1.green_point_hotel = sycototlgrnpt
            form1.save()
            ##print form1

            #----Create Remark table---->
            loadremark = LoadDashboard.objects.latest('load_no')
            ##print('loadremark', loadremark)
            ##print('loadremark.remarks', loadremark.remarks)
            ##print('loadremark.user_id', loadremark.user_id)
            remark_tbl = Remark
            remarks = remark_tbl(user=loadremark.user_id, comment=loadremark.remarks, load_remark=loadremark)
            remarks.save()

            messages.success(request, "Successfully Created")
            return HttpResponseRedirect('/hotel_management/hotel_dashboard/')
        else:
            messages.success(request, 'Invalid Load')
            #return HttpResponse('invalid!')
    else:
        form = HoteldashboardcreateForm()
    context = {'form': form, 'product': product, 'category': category, }
    return render(request, 'hotel_management/hotel_dashboardcreate.html', context)
#--------End HoteldashboardCreate-------->


#--------Start HoteldashboardUpdate-------->
@login_required(login_url='/user_login/')
def hotel_dashboardUpdate(request, pk):

    product = Product.objects.all()
    category = Category.objects.all()
    instance = get_object_or_404(LoadDashboard, load_no=pk)
    #queryset = LoadDashboard.objects.filter(user_id=instance.user_id)
    if request.method == "POST":
        form = HoteldashboardcreateForm(data=request.POST, instance=instance)
        
        if form.is_valid():
            if ("Processing" in instance.status):
                instance = form.save(commit=False)
                instance.user_id = User.objects.get(username=request.user.username)

                ##print('instance.load_no', instance.load_no)

                loadweight = instance.weight
                ##print('loadweight', loadweight)
                compnyname = instance.hotel_id.hotel_name
                ##print('compnyname', compnyname)
                syccomaster = SyccoMaster.objects.get(company_name=compnyname)

                syccogreenpoint = ""
                sycmstrtotlgrnpt = 0
                tamount = 0
                syccoamount = ""
                syccoamount = syccomaster.amount
                ##print('syccoamount', syccoamount)
                syccogreenpoint = syccomaster.green_point
                #print('syccogreenpoint', syccogreenpoint)

                if syccomaster.total_amount:
                    tamount = syccomaster.total_amount
                    #print('tamount', tamount)

                if syccomaster.total_greenpoint:
                    sycmstrtotlgrnpt = syccomaster.total_greenpoint
                    #print ('sycmstrtotlgrnpt', sycmstrtotlgrnpt)
                    #print type(sycmstrtotlgrnpt)

                sycototlgrnpt = int(loadweight)*syccogreenpoint
                #print('sycototlgrnpt', sycototlgrnpt)
                syctotlamount = int(sycototlgrnpt)*syccoamount/syccogreenpoint
                #print('syctotlamount', syctotlamount)

                loadid = LoadDashboard.objects.get(load_no=instance.load_no)
                #print('loadid', loadid)
                loadidweight = loadid.weight
                #print('loadidweight', loadidweight)

                hotelgreenpt = loadid.green_point_hotel
                #print('hotelgreenpt', hotelgreenpt)

                #----Start SyccoMaster table Update---->
                updategrnpts = sycmstrtotlgrnpt-hotelgreenpt
                #print('updategrnpts', updategrnpts)
                finalupdate = updategrnpts+sycototlgrnpt
                #print('finalupdate', finalupdate)
                syccomaster.total_greenpoint = finalupdate

                #syccomaster.total_amount = tamount+syctotlamount
                updateamounts = tamount-loadidweight
                #print('updateamounts', updateamounts)
                finalamountupdate = updateamounts+syctotlamount
                #print('finalamountupdate', finalamountupdate)
                syccomaster.total_amount = finalamountupdate
                #print('syccomaster.total_amount', syccomaster.total_amount)
                syccomaster.save()
                #----End SyccoMaster table Update---->

                #print('syccomaster.total_greenpoint', syccomaster.total_greenpoint)

                #----Update Hotel GreenPoint of LoadDashboard table---->
                instance.green_point_hotel = sycototlgrnpt
                #print('instancehotelgrnpoint' ,instance.green_point_hotel)

                #----Update Remark table---->
                remark_tbl = Remark
                remarks = remark_tbl(user=instance.user_id, comment=instance.remarks, load_remark=loadid)
                remarks.save()

                instance.save()
                #print instance
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect('/hotel_management/hotel_dashboard/')
            else:
                messages.success(request, 'Sorry! Already Acknowledge or Closed')
        else:
            messages.success(request, "Invalid Form")
    else:
        form = HoteldashboardcreateForm()
    context = {'form': form, 'instance': instance, 'product':product, 'category':category, }

    return render(request, 'hotel_management/hotel_dashboardupdate.html', context)
#--------End HoteldashboardUpdate-------->


#--------Start HoteldashboardDelete-------->
@login_required(login_url='/user_login/')
def Hotel_dashboardDelete(request, pk):

    instance = get_object_or_404(LoadDashboard, pk=pk)
    instance.user_id = User.objects.get(username=request.user.username)
    queryset = LoadDashboard.objects.all().order_by('-date_and_time')
    if ("Processing" in instance.status):

        loadweight = instance.weight
        compnyname = instance.hotel_id.hotel_name
        #print('compnyname', compnyname)
        syccomaster = SyccoMaster.objects.get(company_name=compnyname)

        syccogreenpoint = ""
        sycmstrtotlgrnpt = 0
        tamount = 0
        syccoamount = ""
        syccoamount = syccomaster.amount
        #print('syccoamount', syccoamount)
        syccogreenpoint = syccomaster.green_point
        #print('syccogreenpoint', syccogreenpoint)

        if syccomaster.total_amount:
            tamount = syccomaster.total_amount
            #print('tamount', tamount)

        if syccomaster.total_greenpoint:
            sycmstrtotlgrnpt = syccomaster.total_greenpoint
            #print ('sycmstrtotlgrnpt', sycmstrtotlgrnpt)
            #print type(sycmstrtotlgrnpt)

        sycototlgrnpt = int(loadweight)*syccogreenpoint
        #print('sycototlgrnpt', sycototlgrnpt)
        syctotlamount = int(sycototlgrnpt)*syccoamount/syccogreenpoint
        #print('syctotlamount', syctotlamount)

        #----SyccoMaster table Update---->
        syccomaster.total_greenpoint = sycmstrtotlgrnpt-sycototlgrnpt
        syccomaster.total_amount = tamount-syctotlamount
        syccomaster.save()
        #----End Sycco Green Point---->

        instance.delete()
        messages.success(request, "Successfully Deleted")
        return HttpResponseRedirect('/hotel_management/hotel_dashboard/')
    else:
        messages.success(request, "Not Allow!")
    #queryset = LoadDashboard.objects.all().order_by('-date_and_time')
    return render(request, 'hotel_management/hotel_dashboard.html', {"queryset": queryset})
#--------End HoteldashboardDelete-------->


# #--------Start Hoteldashboard-------->
# @login_required(login_url='/user_login/')
# def hotel_dashboard(request): 

#     queryset = LoadDashboard.objects.filter(user_id=request.user).order_by('-load_no')

#     remarkloadss = []
#     for query1 in queryset:
#         #print('query1', query1.load_no)
#         rmrkload = query1.load_no

#         remarkload = Remark.objects.filter(load_remark=rmrkload).order_by('-date')
#         remarkloadss += remarkload
#     context = {
#         "queryset": queryset, 'remarkload':remarkloadss,
#     }
#     return render(request, 'hotel_management/hotel_dashboard.html', context)
# #--------End Hoteldashboard-------->



#--------Start Hoteldashboarddetails-------->
# @login_required(login_url='/user_login/')
# def hotel_dashboarddetails(request, pk):
#     instance = get_object_or_404(LoadDashboard, load_no=pk)
#     loadremark = LoadDashboard.objects.filter(load_no=instance.load_no)

#     loadloop = []
#     for loadrmrk in loadremark:
#         loadrmrk = loadrmrk.load_no
#         #print('loadrmrk', loadrmrk)
#         remarkload = Remark.objects.filter(load_remark=loadrmrk).order_by('-date')
#         loadloop += remarkload
#     #remarkload = Remark.objects.filter(user=request.user).order_by('-date')
#     context = {
#         'instance':instance, 'remarkload':loadloop,
#     }
#     return render(request, "hotel_management/hotel_dashboarddetails.html", context)
#--------End Hoteldashboarddetails-------->



#--------Start Hoteldashboard-------->
# @login_required(login_url='/user_login/')
# def hotel_dashboard(request): 

#     queryset = LoadDashboard.objects.filter(user_id=request.user).order_by('-date_and_time')
#     remarkload = Remark.objects.filter(user=request.user)

    
#     context = {
#         "queryset": queryset, 'remarkload':remarkload,
#     }
#     return render(request, 'hotel_management/hotel_dashboard.html', context)
#--------End Hoteldashboard-------->



# #--------Start HoteldashboardDelete-------->
# @login_required(login_url='/user_login/')
# def Hotel_dashboardDelete(request, pk):

#     instance = get_object_or_404(LoadDashboard, pk=pk)
#     instance.user_id = User.objects.get(username=request.user.username)
#     if not ("Close" in instance.status):
#         instance.delete()
#         messages.success(request, "Successfully Deleted")
#     else:
#         messages.success(request, "Already Closed")
#     queryset = LoadDashboard.objects.all()
        
#     return render(request, 'hotel_management/hotel_dashboard.html', {"queryset":queryset})
# #--------End HoteldashboardDelete-------->


# #--------Start HoteldashboardUpdate-------->
# @login_required(login_url='/user_login/')
# def hotel_dashboardUpdate(request, pk):
#     instance = get_object_or_404(LoadDashboard, load_no=pk)
#     if request.method == "POST":
#         form = HoteldashboardcreateForm(request.POST, instance=instance)
#         if form.is_valid():
#             if not ("Close" in instance.status):
#                 instance = form.save(commit=False)
#                 instance.user_id = User.objects.get(username=request.user.username)
#                 instance.save()
#                 #print instance
#                 queryset = LoadDashboard.objects.filter(user_id =instance.user_id)
#                 messages.success(request, "Successfully Updated")
#                 return render(request, 'hotel_management/hotel_dashboard.html', {'queryset': queryset})
#             else:
#                 #print "Already CLOSED"
#                 return HttpResponse("Already Closed")
#     else:
#         form = HoteldashboardcreateForm(instance=instance)
#     context = {'form': form }
#     return render(request, 'hotel_management/hotel_dashboardupdate.html', context)
# #--------End HoteldashboardUpdate-------->


#--------Start Hoteldashboard-------->
# @login_required(login_url='/user_login/')
# def hotel_dashboard(request): 
#     group = Group.objects.get(name="Hotel").user_set.all()
#     if request.user.is_superuser or (request.user in group):
#         #return HttpResponseRedirect(reverse('recycler_dashboard'))
#         return HttpResponseRedirect(reverse('hotel_dashboard'))
#     elif not request.user.is_authenticated():
#         #print "not authonticated "
#         return HttpResponseRedirect(reverse('user_login'))
#     else:
#         #print " authonticated "
#     queryset = LoadDashboard.objects.filter(user_id=request.user)
#     #queryset1 = Hoteldashboard.objects.filter(hotel=request.user)
#     context = {
#         "queryset": queryset, "group": group, "group1":group,
#     }
#     return render(request, 'hotel_management/hotel_dashboard.html', context)
#--------End Hoteldashboard-------->


# #--------Start User Registration for Hotel-------->
# def hotel_register(request, pk):
#     # registered = False
#     instance = get_object_or_404(HotelMaster, hotel_id=pk)
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST,)
#         profile_form = UserProfileForm(data=request.POST)
#         a = Hotel.objects.get(hotel_id =instance.hotel_id)

#         #--------Count User for Hotel-------->
#         # count_user = UserProfile.objects.filter(hotel_name=a).count()
#         # #print count_user
#         # if count_user<=3:
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.is_active = False
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.hotel_name = a
#             profile.save()
#             #print profile

#             # current_site = get_current_site(request)
#             # mail_subject = 'Activate your Hotel Management account.'
#             # message = render_to_string('hotel_management/acc_active_email.html', {
#             #     'user': user,
#             #     'domain': current_site.domain,
#             #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             #     'token':account_activation_token.make_token(user),
#             # })
#             # to_email = user_form.cleaned_data.get('email')
#             # email = EmailMessage(mail_subject, message, to=[to_email])
#             # email.send()
#             # return HttpResponse('Please confirm your email address to complete the registration')
        
#             #return HttpResponseRedirect('/hotel_management/hotel_login/')
#             # registered = True
#         else:
#             return HttpResponse('Invalid registered.')
#     #else:return HttpResponse('Sorry! Three User already registered.')
    
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
        
#     context = {'user_form': user_form, 
#                 'profile_form': profile_form, 
#                 'instance': instance, 'a':a,
#             }
#     return render(request, 'hotel_management/hotel_register.html', context)
# #--------End User Registration for Hotel-------->