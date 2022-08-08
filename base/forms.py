from django.forms import ModelForm
from django.contrib.auth.models import User, Group

class regForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']

class loginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

class createGroup(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"