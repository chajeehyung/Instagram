import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm, UserProfileForm


def login_view(request):
    context = {}
    if request.method == 'POST':
        # 1. request.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username에 해당하는 값과 password에 해당하는 값을  각각
        #   username, password변수에 할당
        # 3. 사용자 인증을 수행

        # username, password를 밥는 무분을
        # LoginForm을 사용하도록 변경
        # 로그인에 실패했을경우, Template에 form.non_field_error를 사용해서 로그인이 실패했다는걸 출
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post-list')

    else:
        form = LoginForm()

    context['form'] = form
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
    # render하는 경우
    #  1. POST요청이며 사용자명이 이미 존재할 경우
    #  2. POST요청이며 비밀번호가 같지 않은 경우
    #  3. GET요청인 경우
    # redirect하는 경우
    #  1. POST요청이며 사용자명이 존재하지 않고 비밀번호가 같은 경우

    """
    if request.method가 POST면:
        if 사용자명이 존재하면:
            render1
        if 비밀번호가 같지 않으면:
            render2
        (else, POST면서 사용자명도없고 비밀번호도 같으면):
            redirect
    (else, GET요청이면):
        render
    if request.method가 POST면:
        if 사용자명이 존재하면:
        if 비밀번호가 같지 않으면:
        (else, POST면서 사용자명도없고 비밀번호도 같으면):
            return redirect
    (POST면서 사용자명이 존재하면)
    (POST면서 비밀번호가 같지않으면)
    (POST면서 사용자명이 없고 비밀번호도 같은 경우가 "아니면" -> GET요청도 포함)
    return render
    :param request:
    :return:
    """
    context = {}
    if request.method == 'POST':
        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 post-list화면으로 이동
        # (is_valid()가 True면 올바르다고 가정)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user = User.objects.create_user(
            #     username=form.cleaned_data['username'],
            #     password=form.cleaned_data['password1'],
            # )
            login(request, user)
            # form이 유효하면 여기서 함수 실행 종료
            return redirect('posts:post-list')
        # form이 유효하지 않을 경우, 데이터가 바인딩된 상태로 if-else구문 아래의 render까지 이동
    else:
        # GET요청시 빈 Form을 생성
        form = SignupForm()

    # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
    #  signup.html에
    #   빈 Form또는 올바르지 않은 데이터에 대한 정보가
    #   포함된 Form을 전달해서 동적으로 form을 렌더링
    context['form'] = form
    return render(request, 'members/signup.html', context)


@login_required
def profile(request):
    # GET요청시에는 현재 로그인한 유저의 값을 가진
    # form을 보여줌
    # POST요청시에는 현재 로그인한 유저의 값을
    # POST요청에 다시 담겨온 값을 사용해 수정
    # 이후 다시 form을 보여줌
    # f = Form(request.POST,
    #           request.FILES,
    #              instance==<수정할 인스턴스>
    # f.save()
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            # is_valid()를 통과하고 인스턴스 수정이 완료되면
            # message모듈을 사용해서 템플릿에 수정완료 메세지 표시
            messages.success(request, '프로필 수정이 완료되었습니다')

    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'members/profile.html', context)

def facebook_login(request):
    # URL : .members/facebook-login/
    # URL name: 'members:facebook-login'
    # request.GET에 전달된 'code'값을
    # 그대로 HttpResponse로 출력
    api_get_access_token = 'https://graph.facebook.com/v3.2/oauth/access_token'
    code = request.GET.get('code')

    param = {
        'client_id': 2116108165373949,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': '92ca158012c0c07459e8173ce2ec8a1&',
        'code': code,
    }

    response = requests.get(api_get_access_token, param)
    data = response.json()
    # response_object = json.loads(response.text)
    #
    # return HttpResponse('{}, {}'.format(
    #     response_object,
    #     type(response_object),
    # ))
    access_token = data['access_token']