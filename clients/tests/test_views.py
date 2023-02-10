from django.test import RequestFactory, TestCase
from clients.models import Client
from clients.views import _disabled_letters, _get_clients_and_pages_with_just_search_letter, _get_clients_and_pages, _get_clients_and_pages_with_searchterm_and_searchletter, _updating_client
from clients.forms import UpdateForm

class TestDisabledLetters(TestCase):

    def setUp(self):
        self.client1 = Client.objects.create(
            client_name="Vega",
            address="Futoska",
            city="Novi Sad",
            zip="21000",
            country="Srbija" )
        self.disabled_letters = []
        self.search_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
    def test_disabled_letters(self):
        self.disabled_letters = _disabled_letters(self.search_letters)
        self.assertEquals(self.disabled_letters, ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','W','X','Y','Z'])

class TestGetClientsAndPages(TestCase):

    def setUp(self):
        self.client1 = Client.objects.create(
            client_name="Vega",
            address="Futoska",
            city="Novi Sad",
            zip="21000",
            country="Srbija" )
        self.all_clients = Client.objects.all()
        self.search_letter = "V"
        self.page_number = 1
        self.search_term = "eg"
        
        
    def test_get_clients_and_pages(self):
        self.list_of_pages, self.number_of_pages, self.clients, self.previous_page , self.next_page = _get_clients_and_pages(self.search_letter, self.search_term, self.page_number)
        self.assertEquals(self.list_of_pages,[1])
        self.assertEquals(self.number_of_pages,1)
        self.assertQuerysetEqual(self.clients,self.all_clients)
        self.assertEquals(self.previous_page,0)
        self.assertEquals(self.next_page,0)

class TestUpdatingClient(TestCase):

    def setUp(self):
        self.client1 = Client.objects.create(
            client_name="Vega",
            address="Futoska",
            city="Novi Sad",
            zip="21000",
            country="Srbija" )
        self.request = RequestFactory()
        self.request = self.request.post(f"/clients/", {'client_name': "Vega2", 'address': 'Futoskaa', 'city': 'Novi Sadd', 'zip': '210000', 'country': "Srbijaa", 'pk': "1"})
       

    def test_updating_client(self):
        if self.request.method == "POST":
            client_for_update = Client.objects.get(pk=self.request.POST['pk'])
            
            
            client_for_update.client_name = self.request.POST['client_name']
            client_for_update.address = self.request.POST['address']
            client_for_update.city = self.request.POST['city']
            client_for_update.zip = self.request.POST['zip']
            client_for_update.country = self.request.POST['country']
            client_for_update.save()
        self.client1 = Client.objects.get(pk=self.request.POST['pk'])
        self.assertEquals(self.client1.client_name, "Vega2")
        self.assertEquals(self.client1.address, "Futoskaa")
        self.assertEquals(self.client1.city, "Novi Sadd")
        self.assertEquals(self.client1.zip, 210000)
        self.assertEquals(self.client1.country, "Srbijaa")
        self.assertEquals(self.client1.pk, 1)
        
        