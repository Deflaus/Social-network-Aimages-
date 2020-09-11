from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import ImageForm
from .models import Image
from account.models import Profile


@login_required
def images_list(request):
    images = Image.objects.all()
    profiles = Profile.objects.all()
    return render(request,
                  'images/list_images.html',
                  {'section': 'images',
                   'images': images,
                   'profiles': profiles, })


@login_required
def adding_image(request):
    imageform = None
    created = False
    if request.method == 'POST':
        imageform = ImageForm(request.POST,
                              request.FILES)
        if imageform.is_valid():
            new_image = imageform.save(commit=False)
            new_image.image = request.FILES['image']
            new_image.user = request.user
            new_image.save()
            created = True
    else:
        imageform = ImageForm()
    return render(request,
                  'images/create_image.html',
                  {'addingimage': 'addingimage',
                   'imageform': imageform,
                   'created': created, })


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # create_action(request.user, 'лайкнул', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    profile = Profile.objects.get(user=image.user)
    return render(request,
                  'images/detail.html',
                  {'section': 'images',
                   'image': image,
                   'profile': profile, })


@login_required
def feed(request):
    user = request.user
    followers = user.following.all()
    profiles = Profile.objects.all()
    images = []
    for follower in followers:
        images.append(Image.objects.filter(user=follower))
    return render(request,
                  'images/feed.html',
                  {'section': 'feed',
                   'images': images,
                   'profiles': profiles, })
