from django.shortcuts import render
def delivery_list(request):
    return render(request, 'delivery/dashboard.html')
