from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            age = form.cleaned_data.get('age')
            bio = form.cleaned_data.get('bio')
            image = form.cleaned_data.get('image')
            Profile.objects.create(user=user,age=age,bio=bio,image=image)
            login(request,user)
            return redirect('profile_list') 

    else:
        form = SignupForm()
    return render(request,'profiles/signup.html',{'form':form})     

@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)

    min_age = request.GET.get('min_age')

    max_age = request.GET.get('max_age')

    if min_age and max_age and int(min_age) > int(max_age):
        error_message = "Minumum age cannot be greater than maximum age"

        return render(request,'profiles/profile_list.html', {'profiles': profiles, 'error_message':error_message})


    if min_age:
        profiles = profiles.filter(age__gte=min_age)

    if max_age:
        profiles = profiles.filter(age__lte=max_age)    

    return render(request, 'profiles/profile_list.html', {'profiles': profiles})


def chat(request,other_user_id):
    current_user_id = request.user.id
    room_name = f'{min(current_user_id, other_user_id)}_{max(current_user_id, other_user_id)}'
    return render(request,'profiles/chat.html',{
        'room_name':room_name,
    })