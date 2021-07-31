from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import SetPasswordForm
from account.models import Profile
from account.forms import UserForm, ProfileForm


@staff_member_required
def user_list(request):
    ''' List of all users '''
    users = User.objects.all()
    return render(request, 'account/list.html', {'users': users})


@staff_member_required
def user_create(request):
    ''' Create a user '''
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            profile = profile_form.save(user)
            profile.save()

            return redirect('account:user_list')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'form.html', {'forms': [user_form, profile_form]})

@staff_member_required
def user_password(request, id):
    ''' Set or change user password '''
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('account:user_list')
    else:
        form = SetPasswordForm(user)
    return render(request, 'form.html', {'forms': [form]})

@staff_member_required
def user_edit(request, id):
    ''' Edit a user '''
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save(user)
            return redirect('account:user_list')
    else:
        user_form = UserForm(instance=user)
        # You can use user.profile to obtain user_profile,
        # but it throw an error if no profile assigned to user
        profile, created = Profile.objects.get_or_create(user=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'form.html', {'forms': [user_form, profile_form]})


@staff_member_required
def user_delete(request, id):
    ''' Delete a user '''
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('account:user_list')