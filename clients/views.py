from django.shortcuts import HttpResponseRedirect, render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import Client
import math
from .forms import UpdateForm




class UpdatingClient:
    def __init__(self, request):
        self.request = request

    def _updating_client(self):
        if self.method == "POST":
            client_for_update = Client.objects.get(pk=self.POST['pk'])
            form = UpdateForm(self.POST)
            if form.is_valid():
                client_for_update.client_name = form.cleaned_data['client_name']
                client_for_update.address = form.cleaned_data['address']
                client_for_update.city = form.cleaned_data['city']
                client_for_update.zip = form.cleaned_data['zip']
                client_for_update.country = form.cleaned_data['country']
                client_for_update.save()



# def _updating_client(request):
#     if request.method == "POST":
#         client_for_update = Client.objects.get(pk=request.POST['pk'])
#         form = UpdateForm(request.POST)
#         if form.is_valid():
#             client_for_update.client_name = form.cleaned_data['client_name']
#             client_for_update.address = form.cleaned_data['address']
#             client_for_update.city = form.cleaned_data['city']
#             client_for_update.zip = form.cleaned_data['zip']
#             client_for_update.country = form.cleaned_data['country']
#             client_for_update.save()

class DisabledLetters:
    def __init__(self):
        pass
        
    def _disabled_letters():
        search_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        disabled_letters = []
        for letter in search_letters:
            if not Client.objects.filter(client_name__istartswith = letter):
                disabled_letters.append(letter)
        return disabled_letters


# def _disabled_letters(search_letters):
#     disabled_letters = []
#     for letter in search_letters:
#         if not Client.objects.filter(client_name__istartswith = letter):
#             disabled_letters.append(letter)
#     return disabled_letters

class GetSearchAndPageData():
    def __init__(self, request):
        self.request = request

    def _get_search_and_page_data(self):
        try:
            search_letter = self.GET['search_letter']
        except:
            search_letter = 'D'
        try:
            page_number = int(self.GET['page_number'])
        except:
            page_number = 1
        try:
            search_term = self.GET['search_term']
        except:
            search_term = ""

        return [search_letter, page_number, search_term]

# def _get_search_and_page_data(request):
#     try:
#         search_letter = request.GET['search_letter']
#     except:
#         search_letter = 'D'
#     try:
#         page_number = int(request.GET['page_number'])
#     except:
#         page_number = 1
#     try:
#         search_term = request.GET['search_term']
#     except:
#         search_term = ""

#     return [search_letter, page_number, search_term]


class GetClientsAndPages():
    def __init__(self, search_letter, page_number, search_term):
        self.search_letter = search_letter
        self.page_number = page_number
        self.search_term = search_term


    def _get_clients_and_pages_with_just_search_letter(self):
        number_of_clients = Client.objects.filter(client_name__istartswith = self.search_letter).count()
        list_of_pages = list(range(1,math.ceil(number_of_clients/5)+1))
        number_of_pages = len(list_of_pages)
        clients = Client.objects.filter(client_name__istartswith = self.search_letter)[ self.page_number*5-5 : self.page_number*5 ]
        return [list_of_pages, number_of_pages, clients]

    def _get_clients_and_pages_with_searchterm_and_searchletter(self):
        number_of_clients = Client.objects.filter(client_name__istartswith = self.search_letter).filter(client_name__icontains = self.search_term).count()
        list_of_pages = list(range(1,math.ceil(number_of_clients/5)+1))
        number_of_pages = len(list_of_pages)
        clients = Client.objects.filter(client_name__istartswith = self.search_letter).filter(client_name__icontains = self.search_term)[ self.page_number*5-5 : self.page_number*5 ]
        return [list_of_pages, number_of_pages, clients]

    def _get_clients_and_pages(self):
            
        if self.search_term == "":
            list_of_pages, number_of_pages, clients = self._get_clients_and_pages_with_just_search_letter()
        else:
            list_of_pages, number_of_pages, clients = self._get_clients_and_pages_with_searchterm_and_searchletter()
        
        if self.page_number-1 < 0:
            previous_page = 0
        else:
            previous_page = self.page_number-1
        if self.page_number+1 > number_of_pages:
            next_page = 0
        else:
            next_page = self.page_number+1

        return [list_of_pages, number_of_pages, clients, previous_page , next_page]


# def _get_clients_and_pages_with_just_search_letter(search_letter, page_number):
#     number_of_clients = Client.objects.filter(client_name__istartswith = search_letter).count()
#     list_of_pages = list(range(1,math.ceil(number_of_clients/5)+1))
#     number_of_pages = len(list_of_pages)
#     clients = Client.objects.filter(client_name__istartswith = search_letter)[ page_number*5-5 : page_number*5 ]
#     return [list_of_pages, number_of_pages, clients]

# def _get_clients_and_pages_with_searchterm_and_searchletter(search_letter, page_number, search_term):
#     number_of_clients = Client.objects.filter(client_name__istartswith = search_letter).filter(client_name__icontains = search_term).count()
#     list_of_pages = list(range(1,math.ceil(number_of_clients/5)+1))
#     number_of_pages = len(list_of_pages)
#     clients = Client.objects.filter(client_name__istartswith = search_letter).filter(client_name__icontains = search_term)[ page_number*5-5 : page_number*5 ]
#     return [list_of_pages, number_of_pages, clients]

# def _get_clients_and_pages(search_letter, search_term, page_number):
#     if search_term == "":
#         list_of_pages, number_of_pages, clients = _get_clients_and_pages_with_just_search_letter(search_letter, page_number)
#     else:
#         list_of_pages, number_of_pages, clients = _get_clients_and_pages_with_searchterm_and_searchletter(search_letter, page_number, search_term)
    
#     if page_number-1 < 0:
#         previous_page = 0
#     else:
#         previous_page = page_number-1
#     if page_number+1 > number_of_pages:
#         next_page = 0
#     else:
#         next_page = page_number+1

#     return [list_of_pages, number_of_pages, clients, previous_page , next_page]

class GetFormDataForExistingClients():
    def __init__(self, clients, UpdateForm):
        self.clients = clients
        self.UpdateForm = UpdateForm

    def _get_form_data_for_existing_clients(self):
        forms = []
        for client in self.clients:
            forms.append(self.UpdateForm(initial={
                                            'client_name': client.client_name,
                                            'address': client.address,
                                            'city': client.city,
                                            'zip': client.zip,
                                            'country': client.country,
                                            'pk': client.pk }))
        return forms

# def _get_form_data_for_existing_clients(clients, UpdateForm):
#     forms = []
#     for client in clients:
#         forms.append(UpdateForm(initial={
#                                         'client_name': client.client_name,
#                                         'address': client.address,
#                                         'city': client.city,
#                                         'zip': client.zip,
#                                         'country': client.country,
#                                         'pk': client.pk }))
#     return forms

class ClientsView():
    
    def as_view():
        def clients_view(request):
            search_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            # _updating_client(request)
            UpdatingClient._updating_client(request)

            disabled_letters = DisabledLetters._disabled_letters()
            
            
            search_letter, page_number, search_term = GetSearchAndPageData._get_search_and_page_data(request)

            clients_and_pages = GetClientsAndPages(search_letter, page_number, search_term)
            list_of_pages, number_of_pages, clients, previous_page, next_page = clients_and_pages._get_clients_and_pages()

            getforms = GetFormDataForExistingClients(clients, UpdateForm)
            forms = getforms._get_form_data_for_existing_clients()

            clients_data = zip(clients, forms)

            context = { 'navbar': 'clients',
                        'clients_data': clients_data,
                        'list_of_pages': list_of_pages,
                        'number_of_pages': number_of_pages,
                        'page_number': page_number,
                        'next_page': next_page,
                        'previous_page': previous_page,
                        'search_term': search_term,
                        'search_letters': search_letters,
                        'search_letter': search_letter,
                        'disabled_letters': disabled_letters }

            return render(request, 'clients/clients.html', context = context)
        return clients_view


# def clients_view(request):
#     search_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#     # _updating_client(request)
#     UpdatingClient._updating_client(request)

#     disabled_letters = DisabledLetters._disabled_letters()
    
    
#     search_letter, page_number, search_term = GetSearchAndPageData._get_search_and_page_data(request)

#     clients_and_pages = GetClientsAndPages(search_letter, page_number, search_term)
#     list_of_pages, number_of_pages, clients, previous_page, next_page = clients_and_pages._get_clients_and_pages()

#     getforms = GetFormDataForExistingClients(clients, UpdateForm)
#     forms = getforms._get_form_data_for_existing_clients()

#     clients_data = zip(clients, forms)

#     context = { 'navbar': 'clients',
#                 'clients_data': clients_data,
#                 'list_of_pages': list_of_pages,
#                 'number_of_pages': number_of_pages,
#                 'page_number': page_number,
#                 'next_page': next_page,
#                 'previous_page': previous_page,
#                 'search_term': search_term,
#                 'search_letters': search_letters,
#                 'search_letter': search_letter,
#                 'disabled_letters': disabled_letters }

#     return render(request, 'clients/clients.html', context = context)

def delete_client(request):
    client_for_delete = Client.objects.get(pk=request.GET['pk'])
    client_for_delete.delete()
    return redirect('/clients')


class ClientCreateView(CreateView):
    model = Client
    fields = "__all__"
    success_url = reverse_lazy("clients:clients")
