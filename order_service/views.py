from django.shortcuts import render
def order_list(request):
    return render(request, 'client/orders.html')
