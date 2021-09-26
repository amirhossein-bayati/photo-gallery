from .models import Comment, Account
from django import forms

import re


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class AccountForm(forms.Form):
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('woman', 'Woman')
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=12, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    address = forms.CharField(max_length=500, widget=forms.Textarea, required=False)
    age = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if len(name) < 3:
            raise forms.ValidationError("your name at least should be 3 Chars")
        elif len(name) > 30:
            raise forms.ValidationError("your name shouldnt be morethan 30 Chars")
        else:
            return name

    def clean_last_name(self):
        last = self.cleaned_data['last_name']
        if len(last) < 3:
            raise forms.ValidationError("your name at least should be 3 Chars")
        elif len(last) > 50:
            raise forms.ValidationError("your name shouldnt be morethan 50 Chars")
        else:
            return last

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if phone.isalpha():
            raise forms.ValidationError("enter correct phone")

        elif len(phone) < 10 or len(phone) > 11:
            raise forms.ValidationError("enter correct phone")

        else:
            return phone

    def clean_email(self):
        email = self.cleaned_data['email']

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if (re.fullmatch(regex, email)):
            return email
        else:
            raise forms.ValidationError("Invalid Email, Enter correct one")


class ContactusForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    subject = forms.CharField(max_length=25, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone = forms.CharField(max_length=11, required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("your name at least should be 3 Chars")
        elif len(name) > 50:
            raise forms.ValidationError("your name shouldnt be more than 50 Chars")
        else:
            return name

    def clean_subject(self):
        sub = self.cleaned_data['subject']
        if len(sub) < 3:
            raise forms.ValidationError("your subject at least should be 3 Chars")
        elif len(sub) > 50:
            raise forms.ValidationError("your subject shouldnt be more than 25 Chars")
        else:
            return sub

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if phone.isalpha():
                raise forms.ValidationError("enter correct phone number")

            elif len(phone) < 10 or len(phone) > 11:
                raise forms.ValidationError("enter correct phone number")
            else:
                return phone

    def clean_email(self):
        email = self.cleaned_data['email']

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if (re.fullmatch(regex, email)):
            return email
        else:
            raise forms.ValidationError("Invalid Email, Enter correct one")

    def clean_message(self):
        msg = self.cleaned_data['message']
        if len(msg) < 10:
            raise forms.ValidationError("your message at least should be 10 Chars")
        elif len(msg) > 250:
            raise forms.ValidationError("your name shouldnt be more than 259 Chars")
        else:
            return msg


class SharePostForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if (re.fullmatch(regex, email)):
            return email
        else:
            raise forms.ValidationError("Invalid Email, Enter correct one")

class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, required=True)

