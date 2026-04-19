from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


FORBIDDEN_WORDS = (
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите название товара',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание товара',
            }
        )
        self.fields['image'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )
        self.fields['category'].widget.attrs.update(
            {
                'class': 'form-select',
            }
        )
        self.fields['price'].widget.attrs.update(
            {
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Введите цену',
            }
        )

    @staticmethod
    def _contains_forbidden_words(value: str) -> list[str]:
        value_lower = value.lower()
        return [word for word in FORBIDDEN_WORDS if word in value_lower]

    def clean_name(self):
        name = self.cleaned_data['name']
        found_words = self._contains_forbidden_words(name)
        if found_words:
            raise ValidationError(
                f"Название содержит запрещенные слова: {', '.join(found_words)}."
            )
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        found_words = self._contains_forbidden_words(description)
        if found_words:
            raise ValidationError(
                f"Описание содержит запрещенные слова: {', '.join(found_words)}."
            )
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            return image

        max_size = 5 * 1024 * 1024
        allowed_extensions = {'.jpg', '.jpeg', '.png'}
        allowed_content_types = {'image/jpeg', 'image/png'}

        extension = Path(image.name).suffix.lower()

        if extension not in allowed_extensions:
            raise ValidationError(
                'Допустимы только изображения формата JPEG или PNG.'
            )

        content_type = getattr(image, 'content_type', None)
        if content_type and content_type not in allowed_content_types:
            raise ValidationError(
                'Допустимы только изображения формата JPEG или PNG.'
            )

        if image.size > max_size:
            raise ValidationError('Размер изображения не должен превышать 5 МБ.')

        return image