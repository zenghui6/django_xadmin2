from django.shortcuts import render
#导入，登入，和用户认证模块
from django.contrib.auth import login,authenticate
#邮箱登录
from django.contrib.auth.backends import ModelBackend   #继承ModelBackend类
from django.views.generic.base import View
from django.db.models import Q
from .form import LoginForm
#?????为什么会出现这种情况咧？
from users.models import  UserProfile
#用户登录方法
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
        # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'login_form':login_form})

#增加邮箱登录
#用户名和邮箱都可登录

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            if user.check_password(password):
                return user
        except Exception as e:
            return None

        #git    版本控制尝试


#注册,登录注册都是用的类
class RegisterView(View):
    '''用户注册'''
    def get(self,requset):
        return render(requset,'register.html')
