from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from images.models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/list_people.html',
                  {'section': 'people',
                   'users': users})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            # create_action(new_user, 'создал аккаунт')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(id=user.id - 1)
    images = Image.objects.filter(user=user)
    return render(request,
                  'account/profile_view.html',
                  {'user': user,
                   'profile': profile,
                   'images': images, })


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form, })


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


@login_required
def followers_of_user(request, username):
    user = User.objects.get(username=username)
    followers = user.following.all()
    return render(request,
                  'account/list_people.html',
                  {'section': 'people',
                   'users': followers})
