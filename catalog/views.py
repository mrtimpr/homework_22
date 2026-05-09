from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView
from django.views.generic.list import ListView

from .forms import ProductForm
from .models import Category, Product
from .services import clear_product_cache, get_product_list, get_products_by_category


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_product_list()

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
        context['success_message'] = 'Сообщение успешно отправлено!'
        return self.render_to_response(context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        clear_product_cache(self.object.category_id)
        return response


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_product')


class OwnerOrDeletePermissionRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_product')


class ProductUpdateView(OwnerOrDeletePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def form_valid(self, form):
        old_category_id = self.get_object().category_id
        response = super().form_valid(form)

        clear_product_cache(old_category_id)

        if old_category_id != self.object.category_id:
            clear_product_cache(self.object.category_id)

        return response

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(OwnerOrDeletePermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        category_id = self.object.category_id
        response = super().form_valid(form)
        clear_product_cache(category_id)
        return response


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.is_published:
            product.is_published = False
            product.save(update_fields=['is_published'])
            clear_product_cache(product.category_id)

        return redirect('catalog:product_detail', pk=pk)


class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
