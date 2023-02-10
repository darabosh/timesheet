from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Project
import math
from .forms import UpdateForm
from clients.models import Client
from members.models import Member

def _updating_project(request):
    if request.method == "POST":
        project_for_update = Project.objects.get(pk=request.POST['pk'])
        project_for_update.project_name = request.POST['project_name']
        project_for_update.description = request.POST['description']
        converting_customer_name_to_whole_client_instance = Client.objects.get(client_name=request.POST['customer'])
        project_for_update.customer = converting_customer_name_to_whole_client_instance
        converting_lead_name_to_whole_member_instance = Member.objects.get(member_name=request.POST['lead'])
        project_for_update.lead = converting_lead_name_to_whole_member_instance
        
        try: 
            if request.POST['archive'] == "on":
                project_for_update.archive = True
        except:
            project_for_update.archive = False
        project_for_update.save()

def _disabled_letters(search_letters):
    disabled_letters = []
    for letter in search_letters:
        if not Project.objects.filter(project_name__istartswith = letter):
            disabled_letters.append(letter)
    return disabled_letters

def _get_search_and_page_data(request):
    try:
        search_letter = request.GET['search_letter']
    except:
        search_letter = 'D'
    try:
        page_number = int(request.GET['page_number'])
    except:
        page_number = 1
    try:
        search_term = request.GET['search_term']
    except:
        search_term = ""

    return [search_letter, page_number, search_term]

def _get_projects_and_pages(search_letter, search_term, page_number):
    if search_term == "":
        number_of_projects = Project.objects.filter(project_name__istartswith = search_letter).count()
        list_of_pages = list(range(1,math.ceil(number_of_projects/5)+1))
        number_of_pages = len(list_of_pages)
        projects = Project.objects.filter(project_name__istartswith = search_letter)[ page_number*5-5 : page_number*5 ]
    else:
        number_of_projects = Project.objects.filter(project_name__istartswith = search_letter).filter(project_name__icontains = search_term).count()
        list_of_pages = list(range(1,math.ceil(number_of_projects/5)+1))
        number_of_pages = len(list_of_pages)
        projects = Project.objects.filter(project_name__istartswith = search_letter).filter(project_name__icontains = search_term)[ page_number*5-5 : page_number*5 ]
    
    if page_number-1 < 0:
        previous_page = 0
    else:
        previous_page = page_number-1
    if page_number+1 > number_of_pages:
        next_page = 0
    else:
        next_page = page_number+1

    return [list_of_pages, number_of_pages, projects, previous_page , next_page]

def _get_form_data_for_existing_clients(projects, UpdateForm):
    forms = []

    customers = Client.objects.values_list('client_name')
    CUSTOMER_CHOICES = []
    for customer in customers:
        CUSTOMER_CHOICES.append((customer[0],customer[0]))

    members = Member.objects.values_list('member_name')
    MEMBER_CHOICES = []
    for member in members:
        MEMBER_CHOICES.append((member[0],member[0]))
    
    for project in projects:
        forms.append(UpdateForm(initial={
                                        'project_name': project.project_name,
                                        'description': project.description,
                                        'customer': project.customer,
                                        'lead': project.lead,
                                        'pk': project.pk,
                                        'archive': project.archive }))
    for form in forms:
        form.fields['customer'].choices = CUSTOMER_CHOICES
        form.fields['lead'].choices = MEMBER_CHOICES
    return forms

search_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def projects_view(request):
    _updating_project(request)
    
    disabled_letters = _disabled_letters(search_letters)
    
    search_letter, page_number, search_term = _get_search_and_page_data(request)
    
    list_of_pages, number_of_pages, projects, previous_page, next_page = _get_projects_and_pages(search_letter, search_term, page_number)

    forms = _get_form_data_for_existing_clients(projects, UpdateForm)

    projects_data = zip(projects, forms)

    context = { 'navbar': 'projects',
                'projects_data': projects_data,
                'list_of_pages': list_of_pages,
                'number_of_pages': number_of_pages,
                'page_number': page_number,
                'next_page': next_page,
                'previous_page': previous_page,
                'search_term': search_term,
                'search_letters': search_letters,
                'search_letter': search_letter,
                'disabled_letters': disabled_letters }

    return render(request, 'projects/projects.html', context = context)

def delete_project(request):
    project_for_delete = Project.objects.get(pk=request.GET['pk'])
    project_for_delete.delete()
    return redirect('/projects')


class ProjectCreateView(CreateView):
    model = Project
    fields = ['project_name', 'description', 'customer', 'lead']
    success_url = reverse_lazy("projects:projects")
