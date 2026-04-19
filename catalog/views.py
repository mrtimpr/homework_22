from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView, View
from django.views.generic.list import ListView

from .forms import ProductForm
from .models import Product


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['products'] = page_obj.object_list
        return context


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print('Имя:', name)
        print('Телефон:', phone)
        print('Сообщение:', message)

        context['success_message'] = 'Сообщение успешно отправлено!'
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(View):
    template_name = 'catalog/product_form.html'

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return self.render_form(form)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
        return self.render_form(form)

    def render_form(self, form):
        return render(self.request, self.template_name, {'form': form})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')