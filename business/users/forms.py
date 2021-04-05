from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
# from users.models import Profile

#form for signup
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField ()
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name']

#form for edit user profile
class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        for fieldname in ['password']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ['email','first_name','last_name',]

#form for changing password
class PasswordChangeManualForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeManualForm, self).__init__(*args, **kwargs)

        for fieldname in ['new_password1']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = '__all__'

#form for adding new user by admin
class NewUserRegisterForm(UserCreationForm):
    email = forms.EmailField ()
    def __init__(self, *args, **kwargs):
        super(NewUserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2','is_staff']:
            self.fields[fieldname].help_text = None
            
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name','is_staff','user_permissions']
        # fields='__all__'