from django.shortcuts import render, redirect

# from members.models import User
from .models import Post
from .forms import PostCreateform


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
    }

    return render(request, 'posts/post_list.html', context)


def post_create(request):
    # 1. posts/post_create.html 구현
    # form 구현
    #   input[type=file]
    #   button[type=[submit]

    # 2. /posts/create/ URL에 이 view를 연결
    #   URL명은 'post-create'를 사용
    # 3. render를 적절히 사용해서 해달 템플릿을 return
    # 4. base.html의
    if not request.user.is_authenticated:
        return

    if request.method == 'POST':
        # request.FILES에 form에서 보내느 파일객체가 들어있다
        # 새로운 Post를 생성한다.
        # author는 User.objects.first()
        # photo는 request.FILE에 있는 내용을 저적히 꺼내서
        # 완료된 후 post:post-list 파일로 redirect
        post = Post(
            # author=User.objects.first(),
            author=request.user,
            photo=request.FIlES['photo'],
        )

        post.save()
        return redirect('posts:post-list')

    else:
        form = PostCreateform()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)
