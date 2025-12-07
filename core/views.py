from django.shortcuts import render
def login_view(request):
    return render(request, 'auth/login.html')
def register_view(request):
    return render(request, 'auth/register.html')

