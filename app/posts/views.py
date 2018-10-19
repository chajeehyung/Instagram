from django.shortcuts import render

def post_list(request):
    # request
    # -> config.urls('posts/')
    # -> posts.urls('')
    # -> posts.views.post_list
    #1. Post모델
    #    create_at (생성시간 저장)
    #       auto_now_add=True
    #   modified_at (수정시간 저장)
    #       auto_now=True
    #   두 필드 추가

    #2.Post 모델이 기본적으로 pk내림차수능로 정렬되도록 설정
    #3. 모든 Post 객체에 대한 QuerySet을
    #   render의 context인수로 전달(키:posts)
    #4. posts/post_list/html을 Template으로 사용
    # 템플릿에서는 posts값을 순회하며
    # 각 Post의 photo정보를 출력

    #5. url은 posts.urls 모듈을 사용
    #   config.urls에서 해당 모듈을 include
    #   posts.urls.app_name = 'posts'를 사용
    #   view의 URL은 비원둔다
    #   결과 : localhost:8080/posts/로 접근시 이 view가 처리하도록 함
    pass
