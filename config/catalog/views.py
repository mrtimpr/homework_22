from django.shortcuts import render

from .models import Product


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    print(list(latest_products))
    return render(request, 'catalog/home.html', {'products': latest_products})


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