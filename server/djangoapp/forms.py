from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import DealerReview, CarDealer


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateReviewForm(forms.Form):
    name = forms.CharField(label='name', max_length=200)
    review = forms.CharField(label='name', max_length=500)
    purchase = forms.BooleanField(required=False)

    def save():
        print('you did it!')
'''
class CreateCarDealerForm(forms.Form):
    address = forms.CharField(label='address', max_length=200)
    city = forms.CharField(label='address', max_length=200)
    full_name = forms.CharField(label='address', max_length=200)
    dealer_id = forms.IntegerField(label='dealer_id')
    lat = forms.FloatField(label='lat')
    long = forms.FloatField(label='lat')
    short_name = forms.CharField(label='short_name', max_length=200)
    st = forms.CharField(label='st', max_length=200)
    zip = forms.IntegerField(label='zip')
'''

class CreateCarDealerForm(forms.Form):
    class Meta:
        model = CarDealer
        fields = '__all__'
