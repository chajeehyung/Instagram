import re

from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        # <AppName,<ModelName> 임포트해서도 해도 된
        # 'members.User',
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )

    # auto_now_add:객체가 처음 생성될떄의 시간 저장
    # auto_now:객체가 save()가 호풀 될 때 마다 시간 저장
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'

    photo = models.ImageField('사진', upload_to='post')


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # 'members.User',
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    content = models.TextField('댓글내용')
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록'
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tags = [HashTag.objects.get_or_create(name=name)[0]
                for name in re.findall(self.TAG_PATTERN, self.content)]
        self.tags.set(tags)

    @property
    def html(self):
        re.sub(
            self.TAG_PATTERN,
            r'<a href="/explore/tags/\g<tag>/">#\g<tag></a>',
            self.content,
        )


        return ''


class HashTag(models.Model):
    name = models.CharField(
        '태그명',
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'



