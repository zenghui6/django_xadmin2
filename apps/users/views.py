from django.shortcuts import render
#导入，登入，和用户认证模块
from django.contrib.auth import login,authenticate
#邮箱登录
from django.contrib.auth.backends import ModelBackend   #继承ModelBackend类
from django.views.generic.base import View
from django.db.models import Q
from .form import LoginForm,RegistForm
#密码加密
from django.contrib.auth.hashers import make_password
#发送邮件
from utils.email_send import send_register_eamil
#?????为什么会出现这种情况咧？
from users.models import  UserProfile,EmailVerifyRecord
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


#注册,登录注册都是用的类
class RegisterView(View):
    '''用户注册'''
    def get(self,requset):
        #实例化
        register_form = RegistForm()
        return render(requset,'register.html',{'register_form':register_form})

    def post(self,requset):
        #带返回值request.POST的实例
        requset_form = RegistForm(requset.POST)
        #判断用户是否合法
        if requset_form.is_valid():
            #获取用户名，判断是否重名
            #form.cleaned_data[]，数据清洗
            user_name = requset_form.cleaned_data['email']
            #如果重名,则提示错误信息重名
            if UserProfile.objects.filter(email = user_name):
                return render(requset,'register.html',{'msg':'用户已存在','register_form':requset_form})

            pass_word = requset_form.cleaned_data['password']
            #创建新用户，这是方法之一
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            #默认为非激活状态，要邮箱验证后才激活
            user_profile.is_active = False
            #保存
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(requset,'login.html')
        else:
            return render(requset,'register.html',{'register_form':requset_form})


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效"})





