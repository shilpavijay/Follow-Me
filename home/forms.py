from django import forms

class TweetForm(forms.Form):
	tweet_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'special','size':'91','title': 'Tweet'}))

class LoginForm(forms.Form):
	user_nm = forms.CharField(widget=forms.TextInput(attrs={'class': 'special','size':'25','title': 'Your Username','required': True}))
	user_pwd = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'special','size':'25','title': 'Password please','required': True}))