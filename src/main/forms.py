from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .models import Img
from .utilites import download


class ImgForm(forms.ModelForm):
    img = forms.FileField(required=False, label='Файл')
    link = forms.CharField(max_length=250, label='Ссылка', required=False)

    class Meta:
        model = Img
        fields = ('link', 'img')
    
    def clean(self):
        img, link = self.cleaned_data.get('img'), self.cleaned_data.get('link')
        print(img)

        if not img and not link:
            raise ValidationError('Необходимо заполнить хотя бы одно поле', code='invalid')
        if img and link:
            raise ValidationError('Необходимо заполнить только одно поле', code='invalid')
        elif link and not img:
            self.cleaned_data['img'] = download(link)


class ChangeImgForm(forms.Form):
    width = forms.IntegerField(required=False, label='Ширина')
    height = forms.IntegerField(required=False, label='Высота')

    def clean(self):
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if height and height <= 0:
            raise ValidationError('Необходимо ввести положительную величину', code='invalid')

        if width and width <= 0:
            raise ValidationError('Необходимо ввести положительную величину', code='invalid')

        if not width and not height:
            raise ValidationError('Необходимо заполнить хотя бы одно поле', code='invalid')
