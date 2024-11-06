from django.shortcuts import render, redirect
from products.models import Product
from products.forms import ProductForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            context = {'products': Product.objects.all(), 'form': form}
            return render(request, 'products.html', context)
    else:
        context = {'products': Product.objects.all(), 'form': ProductForm()}
        return render(request, 'products.html', context)