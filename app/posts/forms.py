from django import forms


class PostCreateform(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment =forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form.control',
            }
        ),
    )
