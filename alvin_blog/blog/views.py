from django.shortcuts import render, HttpResponse, redirect
from blog import get_valid_code
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import F
from blog import models
from blog.models import UserInfo
# Create your views here.
from blog.myform import UserRegForm, UserLoginForm
from django.db.models import Count
from blog.templatetags.my_tag import get_side_data
import json


def index(request):
    if request.user.is_authenticated:
        article_list = models.Article.objects.all()

        return render(request, 'base_index.html', {'article_list': article_list})
    else:
        return redirect('/login')


def valid_code(request):
    valid_img = get_valid_code.get_valid(request)
    return HttpResponse(valid_img)


def login(request):
    if request.method == "GET":
        user_info = UserLoginForm(auto_id=True)
        return render(request, 'base_login.html', {"user_info": user_info})

    if request.method == "POST":
        response = {"user": None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        valid = request.POST.get('valid_code')

        print(user, pwd)

        if valid.upper() == request.session.get("valid_code").upper():
            login_user = auth.authenticate(username=user, password=pwd)
            if login_user:
                auth.login(request, login_user)
                response['user'] = login_user.username

            else:
                response['msg'] = "Username or password error!"
        else:
            response["msg"] = "Valid code error!"
        return JsonResponse(response)
    return render(request, 'base_login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')


def register(request):
    user_reg = UserRegForm(auto_id=True)
    if request.method == "GET":
        return render(request, 'register.html', {'user_info': user_reg})
    if request.method == "POST":
        print('进来了')
        msg = {"user": None, 'msg': None}
        # 校验字段
        user_reg_info = UserRegForm(request.POST)

        if user_reg_info.is_valid():
            pwd = user_reg_info.cleaned_data.get("password")
            re_pwd = user_reg_info.cleaned_data.get("re_password")
            if pwd == re_pwd:
                user = user_reg_info.cleaned_data.get('username')
                pwd = user_reg_info.cleaned_data.get('password')
                email = user_reg_info.cleaned_data.get('email')
                telephone = user_reg_info.cleaned_data.get('telephone')
                avatar_obj = request.FILES.get('avatar')

                msg['user'] = user
                extra = {}
                if avatar_obj:
                    extra['avatar'] = avatar_obj
                    UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=telephone, **extra)

                return JsonResponse(msg)
            else:

                msg['msg'] = user_reg_info.errors

                return JsonResponse(msg)
        else:
            msg['msg'] = user_reg_info.errors
            return JsonResponse(msg)


def home_site(request, username, **kwargs):
    user = models.UserInfo.objects.filter(username=username).first()
    # if not user:
    #     return render(request, 'not_found.html')

    article_list = models.Article.objects.filter(user=user)

    if kwargs:
        print("kwargs:", kwargs)
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'category':
            article_list = article_list.filter(category__title=param)
        elif condition == "tag":
            article_list = article_list.filter(tags__title=param)

        else:
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    return render(request, 'base_site_home.html', {"username": username, "article_list": article_list})


def article_detail(request, username, nid):
    user = models.UserInfo.objects.filter(username=username).first()
    context = get_side_data(username)
    article = models.Article.objects.filter(user=user).filter(nid=nid).first()
    context.update({"article": article})

    return render(request, 'base_article_detail.html', locals())


def digg(request):
    print(request.POST)
    print('进来了')

    is_up = json.loads(request.POST.get('is_up'))
    article_id = request.POST.get("article_id")
    user_id = request.user.pk
    res = {'state': True}
    try:
        ud_obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()

        if not ud_obj:
            models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
            article_obj = models.Article.objects.filter(nid=article_id)
            if is_up:
                article_obj.update(up_count=F('up_count') + 1)
            else:
                article_obj.update(down_count=F('down_count') + 1)
        else:
            res['state'] = False
            res['handled'] = ud_obj.is_up
    except Exception as e:
        res['state'] = False
        res['Exception'] = str(e)
    return JsonResponse(res)
