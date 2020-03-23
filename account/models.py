from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from django.utils import timezone

from .mixins import PermissionsMixin
from .validators import UsernameValidator


class UserManager(BaseUserManager):
    """用户管理器"""
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """抽象用户模型"""
    username_validator = UsernameValidator()
    username = models.CharField('用户名', max_length=150, unique=True, validators=[username_validator],
                                help_text='必填。150个字符或者更少。包含字母，数字和仅有的/./+/-/_符号。',
                                error_messages={
                                    'unique': '已存在一位使用该名字的用户。',
                                })
    email = models.EmailField('电子邮件地址', unique=True, blank=False, null=False)
    is_active = models.BooleanField('有效', default=False, help_text='指明用户是否被认为是活跃的。以反选代替删除帐号。')
    date_joined = models.DateTimeField('加入日期', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        abstract = True


class User(AbstractUser):
    avatar = models.URLField('头像', null=True)
    last_login_ip = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-last_login']

