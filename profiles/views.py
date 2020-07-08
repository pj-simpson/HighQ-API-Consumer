from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from actions.utils import create_action

from .forms import ProfileEditForm, UserRegistrationForm
from .models import Profile


class UserRegisterView(View):
    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        second_line_auto = Group.objects.get(name="Second Line")
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password2"])
            new_user.save()
            Profile.objects.create(user=new_user)
            second_line_auto.user_set.add(new_user)
            new_user = authenticate(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],
            )
            login(request, new_user)
            create_action(request.user, "joined the system.", new_user)
        return render(
            request, "registration/register_done.html", {"new_user": new_user}
        )

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(
            request, "registration/registration_form.html", {"user_form": user_form}
        )


class EditProfileView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(Profile, user_id=request.user.id)
        profile_form = ProfileEditForm(
            instance=profile, data=request.POST, files=request.FILES
        )
        if profile_form.is_valid():
            profile_form.save()
            create_action(request.user, "updated their profile.", profile)
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
        return redirect("profiles:profile_detail", pk=request.user.id)

    def get(self, request):
        profile = get_object_or_404(Profile, user_id=request.user.id)
        profile_form = ProfileEditForm(instance=profile)
        return render(
            request, "profiles/edit_profile.html", {"profile_form": profile_form}
        )


class DetailProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs["pk"]
        object = get_object_or_404(Profile, user_id=user_id)

        return render(request, "profiles/profile_detail.html", {"object": object})
