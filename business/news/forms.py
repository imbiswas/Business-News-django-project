from django import forms
from .models import *


#for form of child data 
class NewsForm(forms.ModelForm):
    class Meta:
        model = news
        exclude = ('filled_by','slug')
        # fields = '__all__'
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)


