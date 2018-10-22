from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm


def login_view(request):
    if request.method == 'POST':
        # 1. request.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username에 해당하는 값과 password에 해당하는 값을  각각
        #   username, password변수에 할당
        # 3. 사용자 인증을 수행
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # 인증 성공시
            login(request, user)
            return redirect('posts:post-list')
        else:
            # 인증 실패시
            pass

    else:
        form = LoginForm()
        context = {
            'form': form,
        }

        return render(request, 'members/login.html', context)


def logout_view(request):
    # URL: /members/logout/
    # Template: 없음

    # !POST요청일 때만 처리
    # 처리 완료 후 'posts:post-list'로 이동

    # base.html에 있는 'Logout'버튼이 이 view로의 POST요청을 하도록 함
    #  -> form을 구현해야 함
    #      'action'속성의 값을 이 view로
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    if request.method == 'POST':
        # 1. request.POST에 전달된 username, password1, password2를 각각 해당 이름의 변수에 할당
        # 2. -x에서는 HttpResponse에 문자열로 에러를 리턴해주기
        #   2-1 username에 해당하는 User가 이미 있다면
        #       사용자명 ({ usernama }) 이미 사용중입니다
        #   2-2 password1과 password2가 일치하지 않는다면
        #       비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다.
        # 3. 위의 두 경우가 아니라면
        #     새 User를 생성, 해당 User로 로그인 시켜준 후 'posts:post-list'로 redirect 처

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            return HttpResponse(f'사용자면({username})은 이미 사용중입니다.')
        if password1 != password2:
            return HttpResponse('비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다.')

        # create_user 메서드는 create와 달리 자동으로 해싱해줌
        user = User.objects.create_user(
            username=username,
            password=password1,
        )
        login(request, user)
        return redirect('posts:post-list')


        pass
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, 'members/signup.html', context)
