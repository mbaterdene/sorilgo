from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Системд нэвтрэх нэр', 
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'3-аас олон тэмдэгт оруулна!'})
    )
    first_name = forms.CharField(
        max_length = 100, 
        label = 'Өөрийн нэр',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Сурагчийн овог'})
    )
    last_name = forms.CharField(
        max_length = 100, 
        label = 'Овог',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Сурагчийн овог'})
    )
    email = forms.EmailField(
        max_length = 150, 
        label = 'Цахим хаяг (e-mail)',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Таны оруулсан цахим шуудан уруу бүртгэл баталгаажуулах холбоос явуулах тул анхааралтай зөв бөглөнө үү.'})
    )
    
    gender = forms.ChoiceField(
        choices = (('m', 'Эрэгтэй'), ('f', 'Эмэгтэй')),
        label = "Хүйс",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    grade = forms.ChoiceField(
        choices = (('fp', '5-р анги'), ('ef', '8-р анги'), ('tg','12-р анги')),
        label = "Анги",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    phone_number = forms.CharField(
        max_length = 150, 
        label = 'Холбоо барих дугаар',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Холбоо барих дугаар оруулна уу'})
    )
    add_info = forms.CharField(
        max_length = 150, 
        label = 'Сурдаг сургуулийнхаа нэрийг бичнэ үү.',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Одоо сурж байгаа сургуулийн талаар мэдээлэл оруула уу'})
    )
    password1 = forms.CharField(
        label='Нууц үг', 
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Нууц үг'})
    )
    password2 = forms.CharField(
        label='Нууц үгээ дахин оруулна уу!', 
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Нууц үгээ дахин оруулна уу!'})
    )
    

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'gender', 'grade', 'phone_number', 'add_info', 'username', 'email', 'password1', 'password2',)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Хэрэглэгчийн нэр давхцаж байна.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Энэ имэйл хаяг бүртгэлтэй байна.')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password1']
        password_again = self.cleaned_data['password2']
        if password != password_again:
            raise forms.ValidationError('Хоёр нууц үг хоорондоо таарахгүй байна.')
        return password_again