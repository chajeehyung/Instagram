import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from members.models import User
from .models import Post, Comment, HashTag
from .forms import PostCreateform, CommentCreateForm, PostForm, CommentForm


def post_list(request):
    # request
    # -> config.urls('posts/')
    # -> posts.urls('')
    # -> posts.views.post_list
    # 1. Post모델
    #    create_at (생성시간 저장)
    #       auto_now_add=True
    #   modified_at (수정시간 저장)
    #       auto_now=True
    #   두 필드 추가

    # 2.Post 모델이 기본적으로 pk내림차수능로 정렬되도록 설정
    # 3. 모든 Post 객체에 대한 QuerySet을
    #   render의 context인수로 전달(키:posts)
    # 4. posts/post_list/html을 Template으로 사용
    # 템플릿에서는 posts값을 순회하며
    # 각 Post의 photo정보를 출력

    # 5. url은 posts.urls 모듈을 사용
    #   config.urls에서 해당 모듈을 include
    #   posts.urls.app_name = 'posts'를 사용
    #   view의 URL은 비원둔다
    #   결과 : localhost:8080/posts/로 접근시 이 view가 처리하도록 함
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentCreateForm(),
    }

    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    # 1. posts/post_create.html 구현
    # form 구현
    #   input[type=file]
    #   button[type=[submit]

    # 2. /posts/create/ URL에 이 view를 연결
    #   URL명은 'post-create'를 사용
    # 3. render를 적절히 사용해서 해달 템플릿을 return
    # 4. base.html의
    context = {}
    if request.method == 'POST':
        # request.FILES에 form에서 보내느 파일객체가 들어있다
        # 새로운 Post를 생성한다.
        # author는 User.objects.first()
        # photo는 request.FILE에 있는 내용을 저적히 꺼내서
        # 완료된 후 post:post-list 파일로 redirect
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=form.cleaned_data['comment']
                )
            return redirect('posts:post-list')
    else:
        form = PostCreateform()
    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    # post_pk에 해당하는 Post에 댓글을 생성하는 view
    # 'POST'메서드 요청만 처리
    #
    # 'content'키로 들어온 값을 사용해 댓글 생성, 작성자는 요청한 UserWarning
    # 댓글 생성 완료 후에는 posts-list로 redirect
    # param request:

    # 1. post_pk에 해당하는 Post 객체를 가져와 post변수에 할당
    # 2. request.POST에 전달된 'content'키의 값을 content변수에 할당
    # 3. Comment 생성
    #     author: 현재 요청의 User
    #     post: post_pk에 해당하는 Post객체
    #     content: request.POST로 전달된 'content'키의 값
    # 4. posts:post_list로 redirect하기
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # comment가 가진 content속성에서
            # 해시태그에 해당하는 문자열을 가져와서
            # HashTag객체를 가져오거나 생성(get-or-create)
            # 이후 comment.tags에 해당 객체를 추가
            # p = re.compile(r'#(?P<tag>\w+)')
            # tags = [HashTag.objects.get_or_create(name=name)[0]
            #         for name in re.findall(p, comment.content)]
            # comment.tags.set(tags)

            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    # Post중, 자신에세 속한 Comment가 가진 HashTag목록 중 tag_name이 name인 HashTag가 포함된
    # Post목록을 posts변수에 할당
    # context에 담아서 리턴 reader
    # HTMLㅣ: /post

    posts = Post.objects.filter(
        comments__tags__name=tag_name).distinct()
    context = {
        'posts': posts,
    }

    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)


def post_like_toggle(request, post_pk):
    pass
