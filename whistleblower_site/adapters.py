from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        #Call the parent method to ensure the default behavior
        super().pre_social_login(request, sociallogin)

        #Check if a user with the same email exists in Django admin users
        email = sociallogin.account.extra_data.get('email')
        User = get_user_model()

        if email:
            existing_user = User.objects.filter(email=email).first()
            if existing_user and existing_user.is_superuser:
                #If a superuser with the same email exists, log in the user
                login(request, existing_user)
                #Redirect the user to the desired page and cancel the social login process
                raise ImmediateHttpResponse(redirect('orgreport:home'))

        #If not a superuser, return None to allow the social login process to continue
        return None
