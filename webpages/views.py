from django.db import models
from django.db.models import fields
from django.http.request import validate_host
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from .models import Department, FaultDetail, Station, Status
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .admin import FaultDetailResource
from django.http import HttpResponse

# Create your views here.

#  station = models.ForeignKey(Station, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     fault_no = models.IntegerField()
#     fault_description = models.TextField()
#     fault_date = models.DateField()
#     current_status = models.ForeignKey(Status, on_delete=models.CASCADE)
#     rectification_date = models.DateField(blank=True, null=True)
#     remarks = models.CharField(max_length=255, blank=True)
#     user_id = models.IntegerField(blank=True, null=True)
#     created_date = models.DateTimeField(blank=True, default=datetime.now)


def home(request):
    return render(request, 'webpages/home.html')


@ login_required(login_url='login')
def dashboard(request):
    totalcount = FaultDetail.objects.all().count()
    rectifycount = FaultDetail.objects.filter(
        current_status_id=1).count()
    pendingcount = FaultDetail.objects.filter(current_status_id=2).count()
    disputecount = FaultDetail.objects.filter(current_status_id=3).count()

    azppendcount = FaultDetail.objects.filter(
        current_status_id=2, station_id=1).count()
    slmpendcount = FaultDetail.objects.filter(
        current_status_id=2, station_id=2).count()
    nsppendcount = FaultDetail.objects.filter(
        current_status_id=2, station_id=3).count()
    naipendcount = FaultDetail.objects.filter(
        current_status_id=2, station_id=4).count()

    azprectcount = FaultDetail.objects.filter(
        current_status_id=1, station_id=1).count()
    slmrectcount = FaultDetail.objects.filter(
        current_status_id=1, station_id=2).count()
    nsprectcount = FaultDetail.objects.filter(
        current_status_id=1, station_id=3).count()
    nairectcount = FaultDetail.objects.filter(
        current_status_id=1, station_id=4).count()

    azpdispcount = FaultDetail.objects.filter(Q(current_status_id=4, station_id=1) |
                                              Q(current_status_id=3, station_id=1)).count()
    slmdispcount = FaultDetail.objects.filter(Q(current_status_id=4, station_id=2) |
                                              Q(current_status_id=3, station_id=2)).count()
    nspdispcount = FaultDetail.objects.filter(Q(current_status_id=4, station_id=3) |
                                              Q(current_status_id=3, station_id=3)).count()
    naidispcount = FaultDetail.objects.filter(Q(current_status_id=4, station_id=4) |
                                              Q(current_status_id=3, station_id=4)).count()

    azpfaultcount = FaultDetail.objects.filter(station_id=1).count()
    slmfaultcount = FaultDetail.objects.filter(
        station_id=2).count()
    nspfaultcount = FaultDetail.objects.filter(
        station_id=3).count()
    naifaultcount = FaultDetail.objects.filter(
        station_id=4).count()

    data = {
        'totalcount': totalcount,
        'rectifycount': rectifycount,
        'pendingcount': pendingcount,
        'disputecount': disputecount,
        'azppendcount': azppendcount,
        'slmpendcount': slmpendcount,
        'nsppendcount': nsppendcount,
        'naipendcount': naipendcount,
        'azprectcount': azprectcount,
        'slmrectcount': slmrectcount,
        'nsprectcount': nsprectcount,
        'nairectcount': nairectcount,
        'azpdispcount': azpdispcount,
        'slmdispcount': slmdispcount,
        'nspdispcount': nspdispcount,
        'naidispcount': naidispcount,
        'azpfaultcount': azpfaultcount,
        'slmfaultcount': slmfaultcount,
        'nspfaultcount': nspfaultcount,
        'naifaultcount': naifaultcount,

    }
    return render(request, 'webpages/dashboard.html', data)


@ login_required(login_url='login')
def addfault(request):

    station_search = Station.objects.all()
    department_search = Department.objects.all()
    status_search = Status.objects.all()

    data = {
        'station_search': station_search,
        'department_search': department_search,
        'status_search': status_search,
    }

    if request.method == 'POST':
        station = request.POST['station']
        department = request.POST['department']
        fault_no = request.POST['fault_no']
        fault_description = request.POST['fault_description']
        fault_date = request.POST['fault_date']
        current_status = request.POST['current_status']
        rectification_date = request.POST['rectification_date']
        remarks = request.POST['remarks']
        user_id = request.POST['user_id']

        addfault = FaultDetail(station_id=station, department_id=department, fault_no=fault_no, fault_description=fault_description,
                               fault_date=fault_date, current_status_id=current_status, rectification_date=rectification_date, remarks=remarks, user_id=user_id)

        addfault.save()
        messages.success(request, ': Fault added sucessfully..!')
        return redirect('addfault')

    return render(request, 'webpages/addfault.html', data)


@ login_required(login_url='login')
def search(request):
    faultdetails = FaultDetail.objects.order_by('-created_date')
    data = {
        'faultdetails': faultdetails,
    }

    return render(request, 'webpages/search.html', data)


@ login_required(login_url='login')
def update(request):
    updatefaultdetail = FaultDetail.objects.order_by('-created_date')
    editfault = FaultDetail.objects.all()
    station_filter = Station.objects.values_list(
        'name', flat=True).distinct()
    status_filter = Status.objects.values_list(
        'status', flat=True).distinct()
    department_filter = Department.objects.values_list(
        'dep_name', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            updatefaultdetail = updatefaultdetail.filter(
                fault_no__icontains=keyword)

    if 'station' in request.GET:
        station = request.GET['station']
        if station:
            updatefaultdetail = updatefaultdetail.filter(
                station__name__iexact=station)

    if 'status' in request.GET:
        status = request.GET['status']
        if status:
            updatefaultdetail = updatefaultdetail.filter(
                current_status__status__iexact=status)

    if 'department' in request.GET:
        department = request.GET['department']
        if department:
            updatefaultdetail = updatefaultdetail.filter(
                department__dep_name__iexact=department)

    # if 'update' in request.GET:
    #     update = request.GET['update']
    #     print(update)
    #     updatefault = FaultDetail(fault_no=update)
    #     updatefault.save()
    #     return redirect('update')

    data = {
        'updatefaultdetail': updatefaultdetail,
        'station_filter': station_filter,
        'status_filter': status_filter,
        'department_filter': department_filter,
        'updatefaultdetail': updatefaultdetail,
        'editfault': editfault,
    }
    return render(request, 'webpages/update.html', data)


@ login_required(login_url='login')
def edit(request, pk):
    list_search = Status.objects.all()
    editfault = FaultDetail.objects.get(id=pk)

    if request.method == 'POST':
        station = request.POST['station']
        department = request.POST['department']
        fault_no = request.POST['fault_no']
        fault_description = request.POST['fault_description']
        fault_date = request.POST['fault_date']
        current_status = request.POST['current_status']
        rectification_date = request.POST['rectification_date']
        remarks = request.POST['remarks']
        user_id = request.POST['user_id']

        editfault = FaultDetail(id=editfault.id, station_id=station, department_id=department, fault_no=fault_no, fault_description=fault_description,
                                fault_date=fault_date, current_status_id=current_status, rectification_date=rectification_date,
                                remarks=remarks, created_date=editfault.created_date, user_id=user_id)

        editfault.save()
        messages.success(request, ': Fault status updated sucessfully..!')
        return redirect('update')

    data = {
        'editfault': editfault,
        'list_search': list_search,
    }
    return render(request, 'webpages/editfault.html', data)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, ': You are logged in')
            return redirect('dashboard')

        else:
            messages.warning(request, ': Invalid Credentials')
            return redirect('login')
    return render(request, 'webpages/home.html')


def logout_user(request):
    logout(request)
    messages.success(request, ': Logged out')
    return redirect('login')


def export(request):
    faultdetail_resource = FaultDetailResource()
    dataset = faultdetail_resource.export()
    response = HttpResponse(
        dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="faultdetail.xlsx"'
    return response
