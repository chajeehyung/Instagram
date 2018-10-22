from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from members.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        # 1. request.POST에 데이터가 옴
        # 2. 온 데이터 중에서 username에 해당하는 값과 password에 해당하는 값을  각각
        #   username, password변수에 할당
        #3. 사용자 인증을 수행
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #인증 성공시
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
