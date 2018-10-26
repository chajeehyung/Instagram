from django import forms
from django.contrib.auth import authenticate, get_user_model

# from django.contrib.auth.models import User
# from members.models import User

#1. settings.AUTH_USER_MODEL의 값을 사용해서
# 사용자 모델 클래스를 반환
#2. 사용자 모델 클래스에 대한 관계를 설정할 때
# 관계필드(ForeignKey, ManyToMany, OneToOne)의 관계부분에
# settings.AUTH_USER_MODEL(문자열)을 사용
User = get_user_model()

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        # username이 유일한지 검사
        super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('사용자명 또는 비밀번호가 틀렸습니다')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증이 실패하였습니다')
        return self._user



class SignupForm(forms.Form):
    username = forms.CharField(
        # label='사용자명',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password1 = forms.CharField(
        # label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):
        # username이 유일한지 검사
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('이미 사용중인 유저입니다')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('비밀번호와 비밀번호 확인란이 다릅니다')
        return password2

    def save(self):
        if self.errors:
            raise ValueError('데이터 유효성 검증에 실했습니다')
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password2'],
        )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'last_name',
            'first_name',
            'img_profile',
            'site',
            'introduce',
        ]
