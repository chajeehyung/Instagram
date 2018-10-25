from django import forms

from posts.models import Post, Comment


class PostCreateform(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
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

    def save(self, post, **kwargs):
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs,
        )

class PostForm(forms.ModelForm):
    # 1. posts.views.post_create
    # 2. templates/posts/post_create.html

    comment = forms.CharField(
        label='내용',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'forms-control',
                'rows': 2,
            }
        )
    )

    # def save(self, *args, **kwargs):
    #     if 'author' not in kwargs:
    #         raise ValueError('PostForm.save()에는 반드시 author항목이 포합되어야 합니다')
    #     if kwargs.get('commit') is False:
    #         raise ValueError('PostForm은 반드시 commit=True 이어야합니다')
    #     # post인스턴스는 무조건 commit-True(db에 저장된 모델) 상태
    #     post = super().save(*args, **kwargs)
    #
    #     comment_content = self.cleaned_data['comment']
    #     if comment_content:
    #         post.comments.create(
    #
    #         )

    class Meta:
        model = Post
        fields = [
            'photo',
        ]
        widgets = {
            'photo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',

                }
            )
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                }
            )
        }