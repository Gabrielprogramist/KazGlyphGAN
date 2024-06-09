# image_processing/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import Publication
from pathlib import Path
import os
import subprocess
import shutil

def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('image')
            model_type = request.POST.get('modelSelect')
            uploads_dir = Path(f'media/uploads/{model_type}')
            uploads_dir.mkdir(parents=True, exist_ok=True)

            for image in uploaded_files:
                image_path = uploads_dir / image.name
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            run_inference(uploads_dir, model_type)
            return JsonResponse({'status': 'success'})
    else:
        form = ImageUploadForm()
    return render(request, 'image_processing/index.html', {'form': form})

def find_images(request):
    if request.method == 'POST':
        letters = request.POST.get('letters', '')
        model_type = request.POST.get('modelSelect')
        letters_unicode = [ord(letter) for letter in letters.replace(' ', '')]

        result_images = []
        if model_type == 'vqfont':
            result_dir = Path(f'media/results/{model_type}/vqfont/images')
            for unicode_value in letters_unicode:
                if chr(unicode_value).islower():
                    image_path = result_dir / f'{unicode_value}.jpg'
                    if image_path.exists():
                        result_images.append(str(image_path))
                else:
                    image_path = result_dir / f'{unicode_value}.png'
                    if image_path.exists():
                        result_images.append(str(image_path))
        elif model_type == 'mxfont':
            result_dir = Path(f'media/results/{model_type}')
            for letter in letters:
                if letter.islower():
                    image_path = result_dir / f'lower_{letter}.png'
                else:
                    image_path = result_dir / f'upper_{letter}.png'
                if image_path.exists():
                    result_images.append(str(image_path))

        return JsonResponse({'result_images': result_images})

def about(request):
    return render(request, 'image_processing/about.html')

def publications(request):
    publications = Publication.objects.all()
    return render(request, 'image_processing/publications.html', {'publications': publications})

def run_inference(images_folder, model_type):
    result_dir = Path(f'media/results/{model_type}')
    result_dir.mkdir(parents=True, exist_ok=True)

    if model_type == 'vqfont':
        args = [
            'python', 'vqfont/inference.py',
            'vqfont/cfgs/custom.yaml',
            '--weight', 'vqfont/last.pth',
            '--content_font', 'vqfont/data/content/arial',
            '--img_path', str(images_folder),
            '--saving_root', str(result_dir)
        ]
    elif model_type == 'mxfont':    
        args = [
            'python', 'mxfont/inference.py',
            '--weight', 'mxfont/last.pth',
            '--img_path', str(images_folder),
            '--saving_root', str(result_dir)
        ]

    try:
        result = subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Inference output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during inference:", e.stderr)
        raise e

def reset_folders(request):
    if request.method == 'POST':
        uploads_dir = Path('media/uploads')
        results_dir = Path('media/results')

        if uploads_dir.exists():
            shutil.rmtree(uploads_dir)
        if results_dir.exists():
            shutil.rmtree(results_dir)

        uploads_dir.mkdir(parents=True, exist_ok=True)
        results_dir.mkdir(parents=True, exist_ok=True)

        return JsonResponse({'status': 'Folders have been reset'})
