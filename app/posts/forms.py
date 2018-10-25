from django import forms

from posts.models import Post


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

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )
        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            post.comments.create(
                author=post.author,
                content=comment_content,
            )

        return post

class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        )
    )

    def save(self,post,**kwargs):
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs,
        )


