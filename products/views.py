from django.shortcuts import render
from products.models import Product


# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def products(request):
    context = {'products': Product.objects.all()}
    return render(request, 'products.html', context)