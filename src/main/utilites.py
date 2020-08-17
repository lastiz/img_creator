from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

import requests
from datetime import datetime
import os
from PIL import Image


def download(url, path=settings.MEDIA_URL, chunk_size=2048):
    url = check_protocol(url)

    try:
        req = requests.get(url, stream=True)
    except requests.exceptions.RequestException:
        raise ValidationError('Некорректная ссылка!', code='invalid')

    if req.status_code == 200:
        file = req.content
        file_name = os.path.split(url)[-1]
        return SimpleUploadedFile(file_name, file)

    else:
        raise ValidationError('Некорректная ссылка', code='invalid')


def check_protocol(url):
    """Проверяет и в случае необходимости добавляет протокол"""
    if url.startswith(('http://', 'https://')):
        return url
    return 'http://' + url

def save_image_get_url(url_image, size):
    """Сохраняет картинку с новыми размерами и возвращает путь"""
    # манипуляции с путями
    abs_path = os.path.join(settings.BASE_DIR, url_image[1:])  # c url_image убираю первую косую черту
    img_name = os.path.split(url_image)[-1]  # имя (lol.png)
    new_url_image = settings.MEDIA_URL + 'new_' + img_name
    new_abs_path = os.path.join(settings.BASE_DIR, new_url_image[1:])
    format_img = get_format(url_image)

    # изменяю размер и сохраняю
    im = Image.open(abs_path)
    new_size = get_new_size(size, im)
    new_im = im.resize(new_size, Image.ANTIALIAS)
    new_im.save(new_abs_path, format_img)
    return new_url_image

def get_new_size(size, im):
    """Возвращает новые значения
    """
    if max(size.items(), key=lambda x: x[1])[0] == 'width':
        ratio = size['width'] / float(im.size[0])
        size['height'] = int(float(im.size[1] * float(ratio)))
        return size['width'], size['height']

    else:
        ratio = size['height'] / float(im.size[1])
        size['width'] = int(float(im.size[0] * float(ratio)))
        return size['width'], size['height']




def delete_changed_img(url_image):
    """Удаляет все измененные файлы"""
    img_name = os.path.split(url_image)[-1]
    url_image = url_image[1:] + 'new_' + img_name  # удаляю первый слэш и генерим url для измен. картинки
    changed_path = os.path.join(settings.BASE_DIR, url_image)
    try:
        os.remove(changed_path)
    except FileNotFoundError:
        return

def get_format(url_image):
    """Возвращает формат"""
    format_img = os.path.splitext(url_image)[-1].replace('.', '')  # достаю формат и удаляю точку

    if format_img.lower() == 'jpg':
        return 'JPEG'
    elif not format_img:
        return 'JPEG'
    else:
        return format_img
