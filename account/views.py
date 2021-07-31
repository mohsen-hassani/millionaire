from account.forms import ProfileForm, UserRegisterationForm
from django.shortcuts import redirect, render
from django.contrib.auth import login

# Create your views here.


# TODO: Edit this register module
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save()
            profile_form.save(user)
            login(request, user)
            return redirect('game:home')
    else:
        user_form = UserRegisterationForm()
        profile_form = ProfileForm()
    return render(request, 'form.html', {'forms': [user_form, profile_form]})

