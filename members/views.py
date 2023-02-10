from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Member
import math
from .forms import UpdateForm
from members.models import Member

def _updating_member(request):
    if request.method == "POST":
        member_for_update = Member.objects.get(pk=request.POST['pk'])
        member_for_update.member_name = request.POST['member_name']
        member_for_update.username = request.POST['username']
        member_for_update.email = request.POST['email']
        member_for_update.hours_per_week = request.POST['hours_per_week']
        member_for_update.status = request.POST['status']
        member_for_update.role = request.POST['role']
        member_for_update.save()

def _get_page_data(request):
    try:
        page_number = int(request.GET['page_number'])
    except:
        page_number = 1
    return page_number

def _get_projects_and_pages(page_number):
    number_of_members = Member.objects.all().count()
    list_of_pages = list(range(1,math.ceil(number_of_members/5)+1))
    number_of_pages = len(list_of_pages)
    members = Member.objects.all()[ page_number*5-5 : page_number*5 ]
    
    if page_number-1 < 0:
        previous_page = 0
    else:
        previous_page = page_number-1
    if page_number+1 > number_of_pages:
        next_page = 0
    else:
        next_page = page_number+1

    return [list_of_pages, number_of_pages, members, previous_page , next_page]

def _form_data(members, UpdateForm):
    forms = []
    
    members = Member.objects.all()
    
    for member in members:
        forms.append(UpdateForm(initial={
                                        'member_name': member.member_name,
                                        'username': member.username,
                                        'email': member.email,
                                        'hours_per_week': member.hours_per_week,
                                        'pk': member.pk,
                                        'status': member.status,
                                        'role': member.role }))

    return forms

def members_view(request):
    _updating_member(request)
    
    page_number = _get_page_data(request)
    
    list_of_pages, number_of_pages, members, previous_page, next_page = _get_projects_and_pages(page_number)

    forms = _form_data(members, UpdateForm)

    members_data = zip(members, forms)

    context = { 'navbar': 'members',
                'members_data': members_data,
                'list_of_pages': list_of_pages,
                'number_of_pages': number_of_pages,
                'page_number': page_number,
                'next_page': next_page,
                'previous_page': previous_page, }

    return render(request, 'members/members.html', context = context)

def delete_member(request, memberService):
    member_for_delete = Member.objects.get(pk=request.GET['pk'])
    member_for_delete.delete()
    return redirect('/members')


class MemberCreateView(CreateView):
    model = Member
    fields = ['member_name', 'username', 'email', 'hours_per_week', 'status', 'role']
    success_url = reverse_lazy("members:members")