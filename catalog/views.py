from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def home(request):
    product_list = Product.objects.select_related('category').order_by('-created_at')
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'catalog/home.html',
        {
            'page_obj': page_obj,
            'products': page_obj.object_list,
        },
    )


def contacts(request):
    context = {}

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print('Имя:', name)
        print('Телефон:', phone)
        print('Сообщение:', message)

        context['success_message'] = 'Сообщение успешно отправлено!'

    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(
        request,
        'catalog/product_detail.html',
        {'product': product},
    )


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()

    return render(
        request,
        'catalog/product_form.html',
        {'form': form},
    )