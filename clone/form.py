from django import forms
from django.contrib.auth.models import User
from .models import user

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password0 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    def clean_password1(self):
        password0 = self.cleaned_data.get('password0')
        password1 = self.cleaned_data.get('password1')

        # Check if passwords match
        if password0 and password1 and password0 != password1:
            raise forms.ValidationError("Passwords don't match.")
        return password1

    def save(self):
        # Create a new user if the form is valid
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password0')  # Use 'password0' here

        user = User.objects.create_user(username=username, email=email, password=password)
        return user

class AddRecordForm(forms.ModelForm):
     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}), label="")
     username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}), label="")
     
     class Meta:
        model = user  # Ensure Customer model exists and is imported
        fields = '__all__'