from django import forms
from django.contrib.auth.models import User
from blog.models import Tag


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, min_length=3)
    password = forms.CharField(required=True, min_length=3, max_length=50)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, min_length=2)
    password = forms.CharField(required=True, min_length=2, max_length=50)
    re_password = forms.CharField(required=True, min_length=2, max_length=50)
    email = forms.EmailField(required=True)

    def clean_re_password(self):
        password = self.cleaned_data["password"]
        re_password = self.cleaned_data["re_password"]

        if password != re_password:
            raise forms.ValidationError('Passwords don\'t match.')
        else:
            return re_password

    def clean_username(self):
        cd = self.cleaned_data
        username = cd["username"]


        try:
            user = User.objects.get(username=username)
        except:
            user = False

        if user:
            raise forms.ValidationError("This username has been exists")
        else:
            return username

    def clean_email(self):
        cd = self.cleaned_data
        email = cd["email"]

        try:
            user_email = User.objects.get(email=email)
        except:
            user_email = False

        if user_email:
            raise forms.ValidationError("This Email has been exists")
        else:
            return user_email


class ChangePass(forms.Form):
    last_password = forms.CharField(required=True, min_length=2, max_length=50)
    new_password = forms.CharField(required=True, min_length=2, max_length=50)
    re_password = forms.CharField(required=True, min_length=2, max_length=50)

    def clean_re_password(self):
        password = self.cleaned_data["new_password"]
        re_password = self.cleaned_data["re_password"]

        if password != re_password:
            raise forms.ValidationError('Passwords don\'t match.')
        else:
            return re_password

class AddPhotoForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=250, required=True)
    tag = forms.CharField(max_length=50, required=True)
    image = forms.FileField(required=False)

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError("title at least should be 3 Chars")
        elif len(title) > 50:
            raise forms.ValidationError("title shouldnt be more than 50 Chars")
        else:
            return title

    def clean_description(self):
        des = self.cleaned_data['description']
        if len(des) < 10:
            raise forms.ValidationError("description at least should be 10 Chars")
        elif len(des) > 250:
            raise forms.ValidationError("description shouldnt be more than 250 Chars")
        else:
            return des

    def clean_tag(self):
        tag = self.cleaned_data['tag']

        if tag == 'Select Category':
            raise forms.ValidationError("please enter correct categori")
        else:
            return tag

    # def clean_image(self):
    #     img = self.cleaned_data['image']
    #
    #     if img is None:
    #         raise forms.ValidationError("Upload Photo")
    #     else:
    #         return img