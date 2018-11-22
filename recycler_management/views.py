# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView
from . forms import *
from hotel_management.models import *
from sycco_management.models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


#--------Start Home Page-------->
class Recycler_Home(TemplateView): 
    template_name = 'recycler_management/recycler_home.html'
#--------End Home Page-------->



#--------Start Dashboard-------->
@method_decorator(login_required, name='dispatch')
class Recycler_Dashboard(ListView):
    model = LoadDashboard
    template_name = 'recycler_management/recycler_dashboard.html'
    context_object_name = 'query'

    def get_context_data(self, *args, **kwargs):

        getzip = RecyclerMaster.objects.get(user=self.request.user)
        reczip = getzip.recycler_zip
        hotelid = HotelMaster.objects.filter(hotel_zip=reczip)

        context = super(Recycler_Dashboard, self).get_context_data(*args, **kwargs)

        context['now1'] = []
        loadremark = []
        total = 0
        total_open = 0
        total_aknwlge = 0
        total_close = 0
        for i in hotelid:
            #print('i', i.hotel_id)
            k = i.hotel_id
            hotelid1 = LoadDashboard.objects.filter(hotel_id=k).order_by('-load_no')
            
            for load in hotelid1:

                #----start top box data---->
                total = total + 1
                if load.status == "Processing":
                    total_open = total_open + 1
                elif load.status == "Acknowledge":
                    total_aknwlge = total_aknwlge + 1
                elif load.status == "Close":
                    total_close = total_close + 1

                #----start remark tabel in Notifications---->
                remarkloadtbl = load.load_no
                context['now1'].append(load)
                remarkload = Remark.objects.filter(load_remark=remarkloadtbl).order_by('-date')
                loadremark += remarkload
        context['remarkload'] = loadremark
        context['total'] = total
        context['total_open'] = total_open
        context['total_aknwlge'] = total_aknwlge
        context['total_close'] = total_close
        return context
#--------End Dashboard-------->









# #--------Start Dashboard-------->
# @method_decorator(login_required, name='dispatch')
# class Recycler_Dashboard(ListView):
#     model = LoadDashboard
#     template_name = 'recycler_management/recycler_dashboard.html'
#     context_object_name = 'query'

#     def get_context_data(self, *args, **kwargs):

#         getzip = RecyclerMaster.objects.get(user=self.request.user)
#         reczip = getzip.recycler_zip
#         hotelid = HotelMaster.objects.filter(hotel_zip=reczip)

#         context = super(Recycler_Dashboard, self).get_context_data(*args, **kwargs)
#         context['now1'] = []
#         loadremark = []
#         for i in hotelid:
#             #print('i', i.hotel_id)
#             k = i.hotel_id
#             hotelid1 = LoadDashboard.objects.filter(hotel_id=k).order_by('-load_no')
            
#             for load in hotelid1:
#                 remarkloadtbl = load.load_no
#                 context['now1'].append(load)
#                 remarkload = Remark.objects.filter(load_remark=remarkloadtbl).order_by('-date')
#                 loadremark += remarkload
#         context['remarkload'] = loadremark
#         return context
# #--------End Dashboard-------->


#--------Start Dashboard Detail-------->
@method_decorator(login_required, name='dispatch')
class Recycler_Dashboarddetail(DetailView):
    model = LoadDashboard
    template_name = 'recycler_management/recycler_dashboarddetail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Recycler_Dashboarddetail, self).get_context_data(*args, **kwargs)
        loadtbl = Remark.objects.filter(load_remark=self.kwargs['pk']).order_by('-date')
        context['remarkload']=loadtbl

        return context

#--------End Dashboard Detail-------->



#--------Start Dashboard Detail for greenpoint-------->
@method_decorator(login_required, name='dispatch')
class Recycler_Dashboardgreendetail(DetailView):
    model = LoadDashboard
    template_name = 'recycler_management/recycler_dashboardgreendetail.html'

    def get_context_data(self, **kwargs):

        loadobjects = RecyclerMaster.objects.select_related().get(user=self.request.user)
        getscompany = loadobjects.recycler_name
        companyname = SyccoMaster.objects.get(company_name=getscompany)
        context = super(Recycler_Dashboardgreendetail, self).get_context_data(**kwargs)
        context['query'] = companyname
        #context['query2'] = SyccoMaster.objects.all().filter(company_name=getscompany)
        return context
#--------End Dashboard Detail for greenpoint-------->



#--------Start recycler dashboard Update-------->
@method_decorator(login_required, name='dispatch') 
class RecyclerUpdateView(UpdateView):
    model = LoadDashboard
    #form_class = RecyclerDashboardForm 
    fields = []
    template_name = 'recycler_management/recycler_dashboardupdate.html'
    success_url = 'recycler_management/recycler_dashboar.html'
    
    def get_object(self, pk=None):
        ldobj = LoadDashboard.objects.get(pk=self.kwargs['pk'])
        if ldobj.status == "Processing":
            self.fields = ['load_no', 'no_of_bags', 'weight', 'pickup_date', 'status',]
        elif ldobj.status == "Acknowledge":
            self.fields = ['load_no', 'no_of_bags', 'weight', 'actual_no_of_bags', 'actual_weight', 'status',]
        return self.model.objects.get(pk=self.kwargs['pk'])


    def form_valid(self, form):

        instance = self.model.objects.get(pk=self.kwargs['pk'])
        form.instance.person_id = self.kwargs.get('pk')
        #print('form.status', form)
        a = form.cleaned_data['status']

        if a == "Processing":
            a = "Acknowledge"

            instance = form.save(commit=False)
            instance.status = a
            instance.save()
            messages.success(self.request, "Successfully Updated")

        elif a == "Acknowledge":
            #print('acknowldege', a)
            a = "Close"
            #print('a', a)
            instance = form.save(commit=False)
            instance.status = a
            
            #----Start Sycco Green Point---->
            actweight = instance.actual_weight

            x = User.objects.get(username=self.request.user)

            y = UserProfile.objects.get(user=self.request.user)
            sycomster = SyccoMaster.objects.get(company_name=y.company)
            
            sycgrnpt = ""
            syctotlgrnpt = 0
            sycamount = ""
            syctotalamount = 0

            sycamount = sycomster.amount
            sycgrnpt = sycomster.green_point

            if sycomster.total_amount:
                syctotalamount = sycomster.total_amount

            if sycomster.total_greenpoint:
                syctotlgrnpt = sycomster.total_greenpoint

            scytotlgptupdate = int(actweight)*sycgrnpt

            syctotlamtupdate = int(scytotlgptupdate)*sycamount/sycgrnpt

            sycomster.total_greenpoint = syctotlgrnpt+scytotlgptupdate
            sycomster.total_amount = syctotalamount+syctotlamtupdate
            sycomster.save()
            #----End Sycco Green Point---->

            #----Update Recycler GreenPoint in LoadDashboard table---->
            instance.green_point_recycler = scytotlgptupdate

            #----Remark table create---->
            remark_tbl = Remark
            if self.request.method == 'POST':
                remark2 = self.request.POST.get('remarks')
                if remark2:
                    remark_comment = remark_tbl(user=self.request.user, load_remark=LoadDashboard.objects.get(load_no=instance.load_no), comment=remark2 )
                    remark_comment.save()
            instance.save()
            messages.success(self.request, "Successfully Updated")
        else:
            messages.success(self.request, "Already Acknowledge")
        return HttpResponseRedirect('/recycler_management/recycler_dashboard/') 
#--------End recycler dashboard Update-------->



# #--------Start Dashboard Detail-------->
# @method_decorator(login_required, name='dispatch')
# class Recycler_Dashboarddetail(DetailView):
#     model = LoadDashboard
#     template_name = 'recycler_management/recycler_dashboarddetail.html'

#     def get_context_data(self, *args, **kwargs):
#         getzip = RecyclerMaster.objects.get(user=self.request.user)
#         reczip = getzip.recycler_zip
#         hotelid = HotelMaster.objects.filter(hotel_zip=reczip)

#         context = super(Recycler_Dashboarddetail, self).get_context_data(*args, **kwargs)
#         loadremark = []
#         for i in hotelid:
#             #print('i', i.hotel_id)
#             k = i.hotel_id
#             hotelid1 = LoadDashboard.objects.filter(hotel_id=k).order_by('-date_and_time')
#             loaduser = ""
#             for load in hotelid1:
#                 loaduser = load.user_id
#             remarkload = Remark.objects.filter(user=loaduser).order_by('-date')
#             loadremark += remarkload
#         context['remarkload'] = loadremark
#         return context
# #--------End Dashboard Detail-------->





# #--------Start Update-------->
# @method_decorator(login_required, name='dispatch') 
# class RecyclerUpdateView(UpdateView):
#     model = LoadDashboard
#     #form_class = RecyclerDashboardForm
#     fields = ['load_no', 'no_of_bags', 'weight', 'pickup_date', 'actual_no_of_bags', 'actual_weight', 'status']
#     template_name = 'recycler_management/recycler_dashboardupdate.html'
#     success_url = 'recycler_management/recycler_dashboar.html'
    
#     def get_object(self, pk=None):
#         return self.model.objects.get(pk=self.kwargs['pk'])

#     def form_valid(self, form):

#         instance = self.model.objects.get(pk=self.kwargs['pk'])
#         form.instance.person_id = self.kwargs.get('pk')
#         a = form.cleaned_data['status']
#         b = form.cleaned_data['pickup_date']
#         #print('aa', a)
#         #print type(a)
#         if not b:
#             messages.success(self.request, "Plz Enter pickupdate")
#         else:
#             if a == "Processing":
#                 a = "Acknowledge"

#                 instance = form.save(commit=False)
#                 instance.status = a
#                 instance.save()
#                 messages.success(self.request, "Successfully Updated")

#             elif a == "Acknowledge":
#                 #print('acknowldege', a)
#                 a = "Close"
#                 #print('a', a)
#                 instance = form.save(commit=False)
#                 instance.status = a
                

#                 #----Start Sycco Green Point---->
#                 actweight = instance.actual_weight

#                 x = User.objects.get(username=self.request.user)

#                 y = UserProfile.objects.get(user=self.request.user)
#                 sycomster = SyccoMaster.objects.get(company_name=y.company)
                
#                 sycgrnpt = ""
#                 syctotlgrnpt = 0
#                 sycamount = ""
#                 syctotalamount = 0

#                 sycamount = sycomster.amount
#                 sycgrnpt = sycomster.green_point

#                 if sycomster.total_amount:
#                     syctotalamount = sycomster.total_amount

#                 if sycomster.total_greenpoint:
#                     syctotlgrnpt = sycomster.total_greenpoint

#                 scytotlgptupdate = int(actweight)*sycgrnpt

#                 syctotlamtupdate = int(scytotlgptupdate)*sycamount/sycgrnpt

#                 sycomster.total_greenpoint = syctotlgrnpt+scytotlgptupdate
#                 sycomster.total_amount = syctotalamount+syctotlamtupdate
#                 sycomster.save()

#                 #----End Sycco Green Point---->
#                 instance.green_point_recycler = scytotlgptupdate
#                 instance.save()
#             else:
#                 messages.success(self.request, "Already Acknowledge")
#         return HttpResponseRedirect('/recycler_management/recycler_dashboard/') 

# #--------End Update-------->


# class Recycler_Registeration(View):
#     form_class = RecyclerRegisterForm
#     template_name = 'recycler_management/recycler_registration.html'

#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():

#             instance = form.save(commit=False)

#             # user = form.cleaned_data['recycler_name']
#             # email = form.cleaned_data['email']
#             # password = form.cleaned_data['password']

#             instance.save()

#             # User.objects.create_user(
#             #     username=user, email=email,  password=password)
#             messages.success(request, 'Successfully Register')
#             return HttpResponseRedirect('/')
#             # return HttpResponse('Successfully Registered')
#         return render(request, self.template_name, {'form': form})







# #--------Start Update-------->
# @method_decorator(login_required, name='dispatch')
# class RecyclerUpdateView(UpdateView):
#     model = LoadDashboard
#     form_class = RecyclerDashboardForm
#     template_name = 'recycler_management/recycler_dashboardupdate.html'
#     success_url = 'recycler_management/recycler_dashboar.html'
    
#     def get_object(self, pk=None):
#         return self.model.objects.get(pk=self.kwargs['pk'])

#     def form_valid(self, form):
#         instance = self.model.objects.get(pk=self.kwargs['pk'])
#         form.instance.person_id = self.kwargs.get('pk')
#         a = form.cleaned_data['status']
#         b = form.cleaned_data['pickup_date']
#         #print b

#         if not b:
#             messages.success(self.request, "Plz Enter pickupdate")
#         else:
#             if a == "Processing":
#                 a = "Acknowledge"
#                 #print a
#                 instance = form.save(commit=False)
#                 instance.status = a
#                 instance.save()
#                 messages.success(self.request, "Successfully Updated")

#             elif a == "Acknowledge":
#                 a = "Close"
#                 instance = form.save(commit=False)
#                 instance.status = a
#                 instance.save()
#             else:
#                 messages.success(self.request, "Already Acknowledge")
#         return HttpResponseRedirect('/recycler_management/recycler_dashboard/') 

# #--------End Update-------->