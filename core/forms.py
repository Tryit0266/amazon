from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Address1, CreditCardPayment, Address2, Otp, UploadImage
from django.utils.translation import gettext_lazy as _


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)


	class Meta:
		model = User
		help_texts = {
            'username': None,
        }
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class Address1Form(ModelForm):
    class Meta:
        model = Address1
        fields = ('fullname','phone', 'address1','address2', 'city', 'province', 'postalcode')

        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control', 'id':'fullname'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'address1':forms.TextInput(attrs={'class':'form-control', 'placeholder' : _('Street address or P.O.Box'), 'id' : 'address1'}),
			'address2':forms.TextInput(attrs={'class':'form-control', 'placeholder' : _('Apt, Suite, Unit, Building (optional)'), 'id' : 'address2'}),
            'city':forms.TextInput(attrs={'class':'form-control', 'id':'city'}),
            'province':forms.TextInput(attrs={'class':'form-control', 'id':'state'}),
            'postalcode':forms.NumberInput(attrs={'class':'form-control', 'id':'phone', 'type':'number'}),

        }

class CreditCardPaymentForm(ModelForm):
    class Meta:
        model = CreditCardPayment
        fields = ('CardNumber','ExpDate', 'NameOnCard', 'CVV')

        widgets = {
            'CardNumber':forms.TextInput(attrs={'class':'form-control', 'placeholder':'0000 0000 0000 0000', 'id':'target', 'onkeypress':'if(this.value.length==19) return false'}),
            'ExpDate':forms.TextInput(attrs={'class':'form-control', 'placeholder':'MM/YY', 'onkeyup':'formatString(event)', 'maxlength':'5'}),
            'NameOnCard':forms.TextInput(attrs={'class':'form-control', 'placeholder':'John Doe', 'id':'fullname'}),
            'CVV':forms.TextInput(attrs={'class':'form-control', 'placeholder':'000'}),
        }

class DeliveryForm(ModelForm):
    class Meta:
        model = Address2
        fields = ('fullname','phone', 'address1','address2', 'city', 'province', 'postalcode')

        widgets = {
            'fullname':forms.TextInput(attrs={'class':'form-control', 'id':'fullname'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'type':'number'}),
            'address1':forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Street address or P.O.Box', 'id' : 'address1'}),
			'address2':forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Apt, Suite, Unit, Building (optional)', 'id' : 'address2'}),
            'city':forms.TextInput(attrs={'class':'form-control', 'id':'city'}),
            'province':forms.TextInput(attrs={'class':'form-control', 'id':'state'}),
            'postalcode':forms.NumberInput(attrs={'class':'form-control', 'id':'phone', 'type':'number'}),

        }

class OtpForm(ModelForm):
    class Meta:
        model = Otp
        fields = ('otp',)

        widgets = {
            'otp':forms.TextInput(attrs={'class':'form-control','onkeypress':'if(this.value.length==6) return false'}),

        }

class UserImage(ModelForm):  
    class Meta:   
        model = UploadImage  
        fields = ['image',]
        file = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control form-control-lg','id':'formFileLg', 'type':'file'}))
