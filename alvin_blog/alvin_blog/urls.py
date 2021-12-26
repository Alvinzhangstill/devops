"""alvin_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
from django.views.static import serve
from alvin_blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('valid_code/', views.valid_code),
    path('register/', views.register),
    # path('nikon/', views.test),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    # 个人站点
    re_path(r'^(?P<username>\w+)$', views.home_site),

    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', views.home_site,
            name="personal_site"),

    # 文章详情页
    re_path(r'^(?P<username>\w+)/article/(?P<nid>\d+)/$',views.article_detail),

    # 点赞 踩灭
    path('digg/',views.digg)

]
