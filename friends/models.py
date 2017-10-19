from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core import validators
from common.fields_ext import AutoMD5SlugField, genHashKey
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    SEX_CHOICE = ((1, "男"), (2, "女"), (3, "未知"))

    slug = AutoMD5SlugField(
        verbose_name="唯一标识符",
        hash_key=genHashKey,
        populate_from='id',
        max_length=8,
        unique=True,
    )
    username = models.CharField(
        'username', max_length=150, unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                '用户名无效，请输入合法的用户名(中英文字符以及 @/./+/-/_)',
                'invalid'
            )
        ],
        error_messages={
            'unique': "该用户名已存在。",
            "invalid": "用户名不合法。",
            "null": "用户名不能为空。",
            "blank": "用户名不能为空。"
        })
    avatar = models.URLField(max_length=256, verbose_name='头像', blank=True, null=True)
    phone = models.CharField(
        max_length=11, verbose_name='手机', unique=True, blank=True, null=True,
        error_messages={'unique': '该手机号已存在', "invalid": "无效的手机号。"})
    thumbnail = models.URLField(max_length=256, verbose_name='头像', blank=True)
    sex = models.PositiveSmallIntegerField(default=1, choices=SEX_CHOICE)
    desc = models.CharField(max_length=64, verbose_name='个性描述', blank=True)
    region = models.CharField(max_length=32, verbose_name='地区', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.slug} {self.username}"


class Interests(models.Model):

    user = models.ForeignKey(User, verbose_name="用户")
    update_time = models.DateTimeField(verbose_name="时间", auto_now=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


    class Meta:
        verbose_name = verbose_name_plural = '兴趣'

    def __str__(self):
        return f"{self.user.slug} {self.user.username}"
