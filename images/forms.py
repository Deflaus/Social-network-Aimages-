from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    class Meta():
        model = Image
        fields = ('image', 'title', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update(
            placeholder='Загрузите изображение',
        )
        self.fields['title'].widget.attrs.update(
            placeholder='Введите название изображения',
        )
        self.fields['description'].widget.attrs.update(
            placeholder='Введите описание изображения',
        )
