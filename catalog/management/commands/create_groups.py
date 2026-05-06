from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from catalog.models import Product

try:
    from blog.models import BlogPost
except Exception:
    BlogPost = None


class Command(BaseCommand):
    help = 'Создает группы и назначает права'

    def handle(self, *args, **options):
        moderator_group, _ = Group.objects.get_or_create(name='Модератор продуктов')
        moderator_permissions = Permission.objects.filter(
            content_type__app_label='catalog',
            codename__in=['delete_product', 'can_unpublish_product'],
        )
        moderator_group.permissions.set(moderator_permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" настроена.'))

        if BlogPost is not None:
            content_manager_group, _ = Group.objects.get_or_create(name='Контент-менеджер')
            blog_permissions = Permission.objects.filter(
                content_type__app_label='blog',
                codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost', 'view_blogpost'],
            )
            content_manager_group.permissions.set(blog_permissions)
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" настроена.'))
        else:
            self.stdout.write(self.style.WARNING(
                'Модель блога не найдена. Настрой блок blog вручную под свою модель публикации.'
            ))