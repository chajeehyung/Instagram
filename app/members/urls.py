from django.urls import path

from . import views

# 이 urls모듈의 app_name에 'members'를 사용
# reverse또는 템플릿의 {% url %}태그에서 사용
app_name = 'members'

urlpatterns = [
    # members.urls내의 패턴들은, prefix가 '/members/'임
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]