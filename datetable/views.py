from django.shortcuts import render
import datetime
from datetable.models import Timeslot
from clients.models import Client
from projects.models import Project
from datetable.forms import TimeslotForm
from members.models import Member
from django.http import JsonResponse
import json
from django.core import serializers

def _get_first_day_in_month_table_and_sequence_of_days(request):
    list_of_rows_with_days_in_table = [[], [], [], [], [], []]
    number_of_rows_in_table = 6
    if 'previous' in request.GET:
        first_day_in_table = datetime.datetime.strptime(request.GET["first_day_in_table"], "%Y,%m,%d")
        first_day_in_table = first_day_in_table - datetime.timedelta(10)
        first_day_in_table = (datetime.date(first_day_in_table.year, first_day_in_table.month, 1)
                            -datetime.timedelta(datetime.date(first_day_in_table.year, first_day_in_table.month, 1).weekday()))
    elif 'next' in request.GET:
        first_day_in_table = datetime.datetime.strptime(request.GET["first_day_in_table"], "%Y,%m,%d")
        first_day_in_table = first_day_in_table + datetime.timedelta(40)
        first_day_in_table = (datetime.date(first_day_in_table.year, first_day_in_table.month, 1)
                            -datetime.timedelta(datetime.date(first_day_in_table.year, first_day_in_table.month, 1).weekday()))
    else:
        whole_date_today = datetime.date.today()
        first_day_in_table = (datetime.date(whole_date_today.year, whole_date_today.month, 1)
                        -datetime.timedelta(datetime.date(whole_date_today.year, whole_date_today.month, 1).weekday()))                        
    
    number_of_days_in_row = 7
    for i in range(number_of_rows_in_table):
        for j in range(number_of_days_in_row):
            list_of_rows_with_days_in_table[i].append((first_day_in_table + datetime.timedelta((i*7)+j)))
    
    
    

    if list_of_rows_with_days_in_table[4][0].month != list_of_rows_with_days_in_table[5][0].month:
        list_of_rows_with_days_in_table = list_of_rows_with_days_in_table[:5]

    return [list_of_rows_with_days_in_table, first_day_in_table]

def _get_first_day_in_days_view_and_sequence_of_days(request):
    if 'current_day' in request.GET:
        current_day = datetime.datetime.strptime(request.GET["current_day"], "%Y,%m,%d")
        weekday = datetime.datetime.strptime(request.GET["current_day"], "%Y,%m,%d").weekday()
        first_day = current_day - datetime.timedelta(weekday)
        last_day = first_day + datetime.timedelta(6)

    list_of_days = []
    if 'previous' in request.GET:
        first_day = datetime.datetime.strptime(request.GET["first_day"], "%Y,%m,%d")
        first_day = first_day - datetime.timedelta(7)
    elif 'next' in request.GET:
        first_day = datetime.datetime.strptime(request.GET["first_day"], "%Y,%m,%d")
        first_day = first_day + datetime.timedelta(7)
    last_day = first_day + datetime.timedelta(6)
    
    number_of_days_in_week = 7
    for j in range(number_of_days_in_week):
        list_of_days.append(first_day + datetime.timedelta(j))

    return [list_of_days, first_day, last_day]

def _get_list_of_rows_for_worked_time(request, list_of_rows_with_days_in_table, current_month_and_year_for_date_table):
    list_of_rows_worked_time_each_week = []
    total_hours_that_month = 0
    for list in list_of_rows_with_days_in_table:
        list_of_worked_time_member_that_week = []
        for date in list:
            timeslots_member_that_day = Timeslot.objects.filter(date=date).filter(member=Member.objects.get(pk=2))
            worked_time_member_that_day = 0
            for timeslot in timeslots_member_that_day:
                worked_time_member_that_day += timeslot.time
                if timeslot.date.month == current_month_and_year_for_date_table.month:
                    total_hours_that_month += timeslot.time
            list_of_worked_time_member_that_week.append(worked_time_member_that_day)
        list_of_rows_worked_time_each_week.append(list_of_worked_time_member_that_week)
    return [list_of_rows_worked_time_each_week, total_hours_that_month]

def _get_form_data(request, first_day):
    if 'current_day' in request.GET:
        current_day = datetime.datetime.strptime(request.GET["current_day"], "%Y,%m,%d")
    else:
        current_day = first_day
    
    forms = []
    blank_forms = []

    customers = Client.objects.values_list('client_name')
    CUSTOMER_CHOICES = [("Choose client:", "Choose client:")]
    for customer in customers:
        CUSTOMER_CHOICES.append((customer[0],customer[0]))

    

    PROJECT_CHOICES_BLANK_FORMS = [("Choose project:", "Choose project:")]
    
    timeslots = Timeslot.objects.filter(date=current_day).filter(member=Member.objects.get(pk=2))

    

    number_of_timeslots = len(timeslots)
    total_time = 0
    for i in range(7):
        if i <= number_of_timeslots-1:
            total_time = total_time + timeslots[i].time
            forms.append(TimeslotForm(initial={
                                            'client': timeslots[i].client,
                                            'project': timeslots[i].project,
                                            'description': timeslots[i].description,
                                            'time': timeslots[i].time,
                                            'pk': timeslots[i].pk,
                                            'overtime': timeslots[i].overtime }))
            projects = Project.objects.filter(customer=timeslots[i].client)
            PROJECT_CHOICES = []
            for project in projects:
                PROJECT_CHOICES.append((project,project))
            forms[i].fields['project'].choices = PROJECT_CHOICES
        else:
            blank_forms.append(TimeslotForm())

    for form in forms:
        form.fields['client'].choices = CUSTOMER_CHOICES
        
    
    for blank_form in blank_forms:
        blank_form.fields['client'].choices = CUSTOMER_CHOICES
        blank_form.fields['project'].choices = PROJECT_CHOICES_BLANK_FORMS
    
    return [current_day, forms, blank_forms, total_time]

def _updating_and_creating_new_timeslot(request):
    if request.method == "POST":
        pk_list = request.POST.getlist('pk')
        client_list = request.POST.getlist('client')
        project_list = request.POST.getlist('project')
        description_list = request.POST.getlist('description')
        time_list = request.POST.getlist('time')
        overtime_list = request.POST.getlist('overtime')
        for i in range(len(pk_list)):
            if pk_list[i] != "":
                timeslot = Timeslot.objects.get(pk=int(pk_list[i]))
                client_instance = Client.objects.get(client_name=client_list[i])
                timeslot.client = client_instance
                project_instance = Project.objects.get(project_name=project_list[i])
                timeslot.project = project_instance
                timeslot.description = description_list[i]
                timeslot.time = time_list[i]
                timeslot.overtime = overtime_list[i]
                timeslot.save()
            elif client_list[i] != "Choose client:" and project_list[i] != "Choose project" and time_list[i] != "" and pk_list[i] == '':
                timeslot = Timeslot()
                current_day = datetime.datetime.strptime(request.GET["current_day"], "%Y,%m,%d")
                timeslot.date = current_day
                client_instance = Client.objects.get(client_name=client_list[i])
                timeslot.client = client_instance
                project_instance = Project.objects.get(project_name=project_list[i])
                timeslot.project = project_instance
                timeslot.description = description_list[i]
                timeslot.time = time_list[i]
                if overtime_list[i] == "":
                    overtime_list[i] = 0
                timeslot.overtime = overtime_list[i]
                timeslot.member = Member.objects.get(pk=2)
                timeslot.save()

def datetable_view(request):
    list_of_rows_with_days_in_table, first_day_in_table = _get_first_day_in_month_table_and_sequence_of_days(request)
    current_month_and_year_for_date_table = list_of_rows_with_days_in_table[2][5]

    list_of_rows_worked_time_each_week, total_hours_that_month = _get_list_of_rows_for_worked_time(request, list_of_rows_with_days_in_table, current_month_and_year_for_date_table)
    
    list_of_data_for_each_date_in_table = []
    for i in range(len(list_of_rows_with_days_in_table)):
        list_of_data_for_each_date_in_table.append(zip(list_of_rows_with_days_in_table[i], list_of_rows_worked_time_each_week[i]))
    
    today_date = datetime.date.today()

    context = { "navbar": "timesheet",
                "list_of_data_for_each_date_in_table": list_of_data_for_each_date_in_table,
                "first_day_in_table": first_day_in_table,
                "current_month_and_year_for_date_table": current_month_and_year_for_date_table,
                "today_date": today_date,
                "total_hours_that_month": total_hours_that_month }

    return render(request,'datetable/datetable.html', context = context)


def days_view(request):
    

    _updating_and_creating_new_timeslot(request)
        
    list_of_days, first_day, last_day = _get_first_day_in_days_view_and_sequence_of_days(request)

    current_day, forms, blank_forms, total_time = _get_form_data(request, first_day)

    context = { "navbar": "timesheet",
                "list_of_days": list_of_days,
                "first_day": first_day,
                "last_day": last_day,
                "current_day": current_day,
                "forms": forms,
                "blank_forms": blank_forms,
                "total_time": total_time }
    return render(request,'datetable/days.html', context = context)

def ajax_get_clients_projects(request):
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        selected = json.loads(request.body)
        if selected['selector'] == "Choose client:":
            projects = ["Choose project:"]
        else:
            customer = Client.objects.get(client_name=selected['selector'])
            projects = list(Project.objects.filter(customer=customer).values())
        
        
        return JsonResponse({'projects_options': projects, 'selector_number': selected['selector_number']})