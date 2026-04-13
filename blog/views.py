from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        BlogPost.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])

        if obj.views_count == 100:
            try:
                send_mail(
                    subject='Статья набрала 100 просмотров',
                    message=f'Поздравляем! Статья "{obj.title}" достигла 100 просмотров.',
                    from_email=None,
                    recipient_list=['mr.tim.iv@gmail.com'],
                    fail_silently=True,
                )
            except Exception:
                pass

        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')