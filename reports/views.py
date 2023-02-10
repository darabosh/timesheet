from django.shortcuts import render
from .forms import ReportForm
from datetable.models import Timeslot
from clients.models import Client
from projects.models import Project
from datetable.forms import TimeslotForm
from members.models import Member
import datetime
import json
from django.http import JsonResponse
# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django_xhtml2pdf.utils import generate_pdf

# template_src = 'reports/reports.html'
# def render_to_pdf(template_src, context):
#     template = get_template(template_src)
#     html  = template.render(context)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None


def _search_timeslots(request):
    timeslots = ["","","","","",""]
    total_hours_report = 0
    if request.method == "POST":
        client = request.POST['client']
        project = request.POST['project']
        member = request.POST['member']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date == "":
            start_date = datetime.date(1,1,1)
        if end_date == "":
            end_date = datetime.date(9999,1,1)
        timeslots = Timeslot.objects.filter(date__range=[start_date, end_date])
        
        if client != "Choose client:":
            
            client_instance = Client.objects.get(client_name=client)
            
            timeslots = timeslots.filter(client=client_instance)
            
        if project != "Choose project:":
            project_instance = Project.objects.get(project_name=project)
            timeslots = timeslots.filter(project=project_instance)
        if member != "Choose member:":
            member_instance = Member.objects.get(member_name=member)
            timeslots = timeslots.filter(member=member_instance)
        
    
        for timeslot in timeslots:
            total_hours_report += timeslot.time
    return [timeslots, total_hours_report]

def _get_form_data(request):
    form = ReportForm()

    customers = Client.objects.values_list('client_name')
    CUSTOMER_CHOICES = [("Choose client:", "Choose client:")]
    for customer in customers:
        CUSTOMER_CHOICES.append((customer[0],customer[0]))

    
    PROJECT_CHOICES = [("Choose project:", "Choose project:")]
    

    members = Member.objects.values_list('member_name')
    MEMBER_CHOICES = [("Choose member:", "Choose member:")]
    for member in members:
        MEMBER_CHOICES.append((member[0],member[0]))

    form.fields['client'].choices = CUSTOMER_CHOICES
    form.fields['project'].choices = PROJECT_CHOICES
    form.fields['member'].choices = MEMBER_CHOICES

    return form

def reports_view(request):
    timeslots, total_hours_report = _search_timeslots(request)  
        
    form = _get_form_data(request)
    
    
    context = { "navbar": "reports",
                "form": form,
                "timeslots": timeslots,
                "total_hours_report": total_hours_report }
    # if "pdf" in request.GET:
    #     resp = HttpResponse(content_type="application/pdf")
    #     pdf = generate_pdf('reports/reports.html', resp)
    #     return pdf
    # else:
    return render(request,'reports/reports.html', context = context)
    

def ajax_get_clients_projects(request):
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        selected = json.loads(request.body)
        if selected['selector'] == "Choose client:":
            projects = ["Choose project:"]
        else:
            customer = Client.objects.get(client_name=selected['selector'])
            projects = list(Project.objects.filter(customer=customer).values())
        
        
        return JsonResponse({'projects_options': projects, 'selector_number': selected['selector_number']})
