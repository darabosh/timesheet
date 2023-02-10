from django.shortcuts import render

def categories_view(request):
    navbar = {"navbar": "categories"}
    return render(request,'categories/categories.html', context = navbar)
