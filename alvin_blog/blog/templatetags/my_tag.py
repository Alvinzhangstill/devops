from django import template
from django.template import defaultfilters
from blog import models
from django.db.models import Count

register = template.Library()


@register.simple_tag
def test(x, y):
    return x * y


@register.inclusion_tag('classification.html')
def get_side_data(username):
    user = models.UserInfo.objects.filter(username=username).first()
    if user:
        blog = user.blog
        cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count('article__title')) \
            .values_list('title', 'c')

        tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count("article__nid")) \
            .values_list('title', 'c')

        date_list = models.Article.objects.filter(user=user).extra(
            select={"y_m_time": "date_format(create_time,'%%Y-%%m')"}).values('y_m_time').annotate(c=Count("nid")) \
            .values_list('y_m_time', 'c')

        return {"username": username, "blog": blog, "cate_list": cate_list,
                "tag_list": tag_list, "date_list": date_list}
