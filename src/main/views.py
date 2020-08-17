from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView

from .forms import ImgForm, ChangeImgForm
from.models import Img
from .utilites import save_image_get_url, delete_changed_img


class IndexListView(ListView):
    model = Img
    template_name = 'main/index.html'
    context_object_name = 'images'


class AddImageView(CreateView):
    form_class = ImgForm
    template_name = 'main/add_image.html'
    success_url = '/detail/{id}'


def detail(request, pk):
    image = Img.objects.get(pk=pk)
    form = ChangeImgForm()

    if request.method == 'POST':
        form = ChangeImgForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            new_size = {'width': width if width else 0, 'height': height if height else 0}
            url_to_changed_image = save_image_get_url(url_image=image.img.url, size=new_size)
            return redirect('main:change_done', pk=image.pk, new_img_url=url_to_changed_image)
    
    delete_changed_img(image.img.url)  # удаляю уже сгенерированые пользователем картинки
    context = {'image': image, 'form': form}
    return render(request, 'main/change_img.html', context)


class ChangeDoneView(TemplateView):
    template_name = 'main/change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChangeImgForm()
        context['img_pk'] = self.kwargs.get('pk')
        context['new_img_url'] = self.kwargs.get('new_img_url')
        return context
    