from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


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