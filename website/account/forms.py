from django import forms
from django.contrib import auth

from models import *



# ---------------------- FORMS -----------------------------------------

class InstanceAwareForm( forms.Form ):
	def __init__( self, *args, **kwargs ):
		self.instance = kwargs.pop( 'instance', None )
		super( InstanceAwareForm, self ).__init__( *args, **kwargs )
		self.populate( instance = self.instance )

	def populate( self, instance ):
		pass


# ---------------------- SPECIFIC FORMS --------------------------------


class RegistrationForm(InstanceAwareForm):
	first_name = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='First Name',
				)
	last_name = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='Last Name',
				)
	email_address = forms.EmailField(
						required=True,
						label='Email Address',
					)
	password1 = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='Password',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)
	password2 = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='Password again',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)

	def clean(self):
		cleaned_data = self.cleaned_data
		pass1 = cleaned_data.get("password1")
		pass2 = cleaned_data.get("password2")
		email_address = cleaned_data.get("email_address")

		if pass1 != pass2:
			msg = u"Password fields must match!"
			self._errors["password1"] = self.error_class([msg])
			self._errors["password2"] = self.error_class([msg])
			del cleaned_data["password1"]
			del cleaned_data["password2"]
			raise forms.ValidationError( 'The password fields must match' )

		luser = User.objects.filter( username = email_address )

		if luser.count() > 0:
			raise forms.ValidationError( 'An account with that email address already exists. Login, authenticate or reset your password.' );

		if len( self._errors ) > 0:
			raise forms.ValidationError( 'There were a few problems with your details. Please check your information.' )

		return cleaned_data



class LoginForm(InstanceAwareForm):
	email_address = forms.EmailField(
						required=True,
						label='Email Address',
					)
	password = forms.CharField(
					required=True,
					label='Password',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)

	def clean(self):
		email_address = self.cleaned_data[ "email_address" ]
		password = self.cleaned_data[ "password" ]

		luser = auth.authenticate( username = email_address, password = password )

		if luser is None:
			raise forms.ValidationError( 'Your username or password was incorrect. Remember, it\'s case sensitive.' )

		return self.cleaned_data



class EmailRequestForm( InstanceAwareForm ):
	email_address = forms.EmailField(
						required=True,
						label='Email Address',
					)

	def clean(self):
		myemail = self.cleaned_data[ "email_address" ]

		luser = User.objects.filter( email = myemail )
		if luser.count() != 1:
			raise forms.ValidationError( 'No such email address found in the system.' )

		return self.cleaned_data



class AuthenticationCodeForm( InstanceAwareForm ):
	authcode = forms.CharField(
					required=True,
					min_length=10,
					max_length=10,
					label='Authentication Code', 
				)

	def clean(self):
		mycode = self.cleaned_data[ "authcode" ]

		try:
			lauthcode = AuthenticationCode.objects.get( authentication_code = mycode )
		except AuthenticationCode.DoesNotExist:
			raise forms.ValidationError( 'That authentication code was not found in the system.' )

		return self.cleaned_data




class EditProfileForm(InstanceAwareForm):
	first_name = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='First Name',
				)
	last_name = forms.CharField(
					required=True,
					min_length=2,
					max_length=32,
					label='Last Name',
				)
	email_address = forms.EmailField(
						required=True,
						label='Email Address',
				)

	def populate( self, instance ):
		self.fields['email_address'].initial = instance.email
		self.fields['first_name'].initial = instance.first_name
		self.fields['last_name'].initial = instance.last_name

	def clean_email_address( self ):
		newname = self.cleaned_data['email_address']
		if self.instance.username != newname:
			if User.objects.filter( username = newname ).count() > 0:
				raise forms.ValidationError( 'Another account with that email address already exists. Please choose another!' )
		return newname


	def save( self ):
		cd = self.cleaned_data
		self.instance.email = cd[ 'email_address' ]
		self.instance.username = cd[ 'email_address' ]
		self.instance.first_name = cd[ 'first_name' ]
		self.instance.last_name = cd[ 'last_name' ]
		self.instance.save()
		return self.instance


class ChangePasswordForm(InstanceAwareForm):
	old_password = forms.CharField(
					required=True,
					label='Current Password',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)
	password1 = forms.CharField(
					required=True,
					label='Password',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)
	password2 = forms.CharField(
					required=True,
					label='Password Again',
					widget=forms.PasswordInput(
						render_value=True,
					)
				)

	def clean_old_password( self ):
		old_password = self.cleaned_data[ 'old_password' ]

		luser = authenticate( username = self.instance.username, password = old_password )

		if luser is None:
			raise forms.ValidationError( u"Your current password is incorrect. Please try again!" )
		return old_password



	def clean( self ):
		if self.cleaned_data['password1'] != self.cleaned_data['password2']:
			msg = u"Password fields must match!"
			self._errors["password1"] = self.error_class([msg])
			self._errors["password2"] = self.error_class([msg])
			del self.cleaned_data["password1"]
			del self.cleaned_data["password2"]

		return self.cleaned_data

	def save( self ):
		self.instance.set_password( self.cleaned_data[ 'password1' ] )
		self.instance.save()
		return self.instance


