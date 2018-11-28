# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from hotel_recycler_management.forms import *
from . forms import SyccoProfileForm, SyccoMasterForm
from . models import *
from hotel_management .models import UserProfile
from recycler_management .models import * 


#----for Email verify----> 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from hotel_management.tokens import account_activation_token
from django.core.mail import EmailMessage

# Create your views here.


#--------Start Home Page-------->
class Sycco_Home(TemplateView):
    template_name = 'sycco_management/sycco_home.html'
#--------End Home Page-------->


#--------Start SyccoProfile Registration-------->
class Sycco_Registration(View):

    city = City.objects.all()
    zip = Zip.objects.all()
    state = State.objects.all()
    country = Country.objects.all()

    user_form_class = UserForm
    profile_form_class = SyccoProfileForm
    template_name = 'sycco_management/sycco_registration.html'

    def get(self, request):
        user_form = self.user_form_class(None)
        profile_form = self.profile_form_class(None)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'city':self.city, 'zip':self.zip, 'state':self.state, 'country':self.country, })

    def post(self, request): 
        user_form = self.user_form_class(request.POST)
        profile_form = self.profile_form_class(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)

            user.is_active = True
            user.save()

            group = Group.objects.get(name="Sycco")
            user.groups.add(group)
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

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
            return HttpResponseRedirect('/hotel_management/conform_email/')
            #return HttpResponse('Please confirm your email address to complete the registration')
        else:
            messages.success(request, 'Invalid registered by You.')
            # return HttpResponseRedirect('/')
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form, 'city':self.city, 'zip':self.zip, 'state':self.state, 'country':self.country, })
#--------End SyccoProfile Registration-------->


#--------Start Sycco Dashboard-------->
@method_decorator(login_required, name='dispatch')
class Sycco_Dashboard(ListView):
    model = SyccoMaster
    template_name = 'sycco_management/sycco_dashboard.html'
    context_object_name = 'query'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(Recycler_Dashboard, self).get_context_data(*args, **kwargs)
    #     #context['query1'] = LoadDashboard.objects.all().filter(hotel_zip=2)
    #     return context


class Sycco_DashboardDetail(DetailView): 
    model = SyccoMaster
    template_name = 'sycco_management/sycco_dashboarddetail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Sycco_DashboardDetail, self).get_context_data(*args, **kwargs)
        idd = self.kwargs.get('pk')
        instance = get_object_or_404(SyccoMaster, pk=idd)
        h_name = HotelMaster.objects.get(hotel_name=instance.company_name)
        recyObj = RecyclerMaster.objects.get(recycler_zip=h_name.hotel_zip)
        c_sycco = SyccoMaster.objects.get(company_name=recyObj.recycler_name)
        context['now'] = c_sycco
        return context


class Sycco_DashboardDetail_Cmpny(DetailView): 
    model = SyccoMaster
    template_name = 'sycco_management/sycco_dashboarddetail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Sycco_DashboardDetail_Cmpny, self).get_context_data(*args, **kwargs)
        idd = self.kwargs.get('pk')

        instance = get_object_or_404(SyccoMaster, pk=idd)

        h_name = HotelMaster.objects.get(hotel_name=instance.company_name)
        recyObj = RecyclerMaster.objects.get(recycler_zip=h_name.hotel_zip)
        c_sycco = SyccoMaster.objects.get(company_name=recyObj.recycler_name)

        context['now'] = c_sycco
        return context
    

class Sycco_DashboardCreate(CreateView): 
    form_class = SyccoMasterForm
    template_name = 'sycco_management/sycco_dashboardcreate.html'
    success_url = reverse_lazy('sycco_dashboard')

    def form_valid(self, form):

        fo = form.save(commit=False)
        uss = User.objects.get(username=str(self.request.user))
        fo.user = uss
        fo.company_name = self.request.POST.get('company')
        aagroup = self.request.POST.get('group')
        print('aagroup', aagroup)

        fo.save()
        return super(Sycco_DashboardCreate, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(Sycco_DashboardCreate, self).get_context_data(*args, **kwargs)
        context['userpro'] = UserProfile.objects.all()
        #context['userpro'] = UserProfile.objects.all().filter(group="Recycler")
        #context['userhotel'] = UserProfile.objects.all().filter(group="Hotel")
        return context


class Sycco_DashboardUpdate(UpdateView):

    model = SyccoMaster
    #form_class = SyccoMasterForm
    fields = ['weight', 'green_point', 'amount']
    template_name = 'sycco_management/sycco_dashboardupdate.html'
    success_url = reverse_lazy('sycco_dashboard')


class Sycco_DashboardDelete(DeleteView):
    model = SyccoMaster
    success_url = reverse_lazy('sycco_dashboard')



#--------Start SyccoProfile Registration -------->
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
#--------End SyccoProfile Registration-------->












# class Sycco_DashboardDetail(DetailView): 
#     model = SyccoMaster
#     template_name = 'sycco_management/sycco_dashboarddetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(Sycco_DashboardDetail, self).get_context_data(**kwargs)
#         recuser = self.request.user
#         idd = self.kwargs.get('pk')
#         abc = SyccoMaster.objects.filter(user=self.request.user)
        
#         sycco_company = ""
#         for a in abc:
#             sycco_company = a.company_name
#             print('sycco_company', sycco_company)

#         sypro = SyccoProfile.objects.get(user=a.user)
#         print('sypro', str(sypro))
#         print('sypro', sypro.zip)

#         recy_tb = RecyclerMaster.objects.get(recycler_zip=sypro.zip)
#         print('recy_tb', recy_tb.recycler_zip)

#         htl = HotelMaster.objects.filter(hotel_zip=recy_tb.recycler_zip)
#         hotelzip = ""
#         h_name = ""
#         for ht in htl:
#             hotelzip = ht.hotel_zip
#             print('ht', ht.hotel_zip)
#             print('ht', str(ht.hotel_name))
#             ht.hotel_name = sycco_company
#             print('ht.hotel_name', ht.hotel_name)
#             h_name =  ht.hotel_name

#         rec_sycco = SyccoMaster.objects.get(company_name=h_name)
        


        


#         # rec_tb = RecyclerMaster.objects.get(recycler_name=sycco_company)
#         # print(rec_tb, rec_tb.recycler_name)
#         # rec_sycco = SyccoMaster.objects.get(company_name=rec_tb.recycler_name)
#         # print ('rec_sycco', rec_sycco.company_name)
#         # # print('rec_tb_name', rec_sycco.recycler_name)
#         # rec_zip = rec_tb.recycler_zip
#         # print('rec_zip1', rec_zip)
#         context['rec_sycco'] = rec_sycco
#         #context['rec_sycco'] = SyccoMaster.objects.get(company_name=rec_tb.recycler_name)
#         print('context1', context)

#         #context['now'] = SyccoHRtable.objects.all().filter(user=recuser)
#         print("context", context)
#         return context



#(22/11/2018)
# class Sycco_DashboardDetail(DetailView): 
#     model = SyccoMaster
#     template_name = 'sycco_management/sycco_dashboarddetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(Sycco_DashboardDetail, self).get_context_data(**kwargs)
#         recuser = self.request.user
#         idd = self.kwargs.get('pk')
#         abc = SyccoMaster.objects.filter(user=self.request.user)
        
#         sycco_company = ""
#         for a in abc:
#             sycco_company = a.company_name
#             print('sycco_company', sycco_company)

#         rec_tb = RecyclerMaster.objects.get(recycler_name=sycco_company)
#         print(rec_tb, rec_tb.recycler_name)
#         rec_sycco = SyccoMaster.objects.get(company_name=rec_tb.recycler_name)
#         print ('rec_sycco', rec_sycco.company_name)
#         # print('rec_tb_name', rec_sycco.recycler_name)
#         rec_zip = rec_tb.recycler_zip
#         print('rec_zip1', rec_zip)
#         context['rec_sycco'] = rec_sycco
#         #context['rec_sycco'] = SyccoMaster.objects.get(company_name=rec_tb.recycler_name)
#         print('context1', context)

#         #context['now'] = SyccoHRtable.objects.all().filter(user=recuser)
#         print("context", context)
#         return context






# class Sycco_DashboardDetail(DetailView): 
#     model = SyccoMaster
#     template_name = 'sycco_management/sycco_dashboarddetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(Sycco_DashboardDetail, self).get_context_data(**kwargs)
#         recuser = self.request.user
#         context['now'] = SyccoHRtable.objects.all().filter(user=recuser)
#         print("context", context)
#         return context






















#28/11/2018
# class Sycco_DashboardDetail(DetailView): 
#     model = SyccoMaster
#     template_name = 'sycco_management/sycco_dashboarddetail.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(Sycco_DashboardDetail, self).get_context_data(*args, **kwargs)
#         idd = self.kwargs.get('pk')
#         ######
#         rec = SyccoMaster.objects.all().filter(id=idd)
#         print('##########', rec)
#         for i in rec:
#             co = i.company_name
#             print('@@@@@@@@', co)
#         # context['rec'] = rec
#             if co.hotel == True:
#                 h_name = HotelMaster.objects.get(hotel_name=co)
#                 print('h_nmaeeeeeeeeeeeeeeeeee', h_name)
#                 recyObj = RecyclerMaster.objects.get(recycler_zip=h_name.hotel_zip)
#                 print('recyobj',recyObj)
#                 c_sycco = SyccoMaster.objects.get(company_name=recyObj.recycler_name)
#                 print('c_sycco',c_sycco)
#                 context['now'] = c_sycco
#             if co.rec == True:
#                 context['rec'] = rec
#         print(context)
#         ######
#         # instance = get_object_or_404(SyccoMaster, pk=idd)
#         # h_name = HotelMaster.objects.get(hotel_name=instance.company_name)
#         # recyObj = RecyclerMaster.objects.get(recycler_zip=h_name.hotel_zip)
#         # c_sycco = SyccoMaster.objects.get(company_name=recyObj.recycler_name)
#         # context['now'] = c_sycco
        
#         return context