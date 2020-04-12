from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from .forms import ProfileEditForm, UserRegistrationForm
from .models import Profile

class UserRegisterView(View):

    def post(self,request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password2'])
            new_user.save()
            Profile.objects.create(user=new_user)
        return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})

    def get(self,request):
        user_form = UserRegistrationForm()
        return render(request,
                      'registration/registration_form.html',
                      {'user_form': user_form})

class EditProfileView(View,LoginRequiredMixin):

    def post(self,request):
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return render(request,'profiles/edit_profile.html',{'profile_form':profile_form})


    def get(self,request):
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,'profiles/edit_profile.html',{'profile_form':profile_form})

class DetailProfileView(View,LoginRequiredMixin):

    def get(self,request,*args,**kwargs):
        user_id = self.kwargs['pk']
        object = get_object_or_404(Profile, user_id=user_id)
        return render(request,'profiles/profile_detail.html',{'object':object})



