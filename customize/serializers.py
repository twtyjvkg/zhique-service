#!/usr/bin/python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = 'xuzhao'
__email__ = 'xuzhao@zhique.design'

from rest_framework import serializers

from .models import SiteProfile, Carousel, SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    """社交账号序列化"""
    qrcode_url = serializers.SerializerMethodField()
    qrcode_image_id = serializers.IntegerField(write_only=True, source='qrcode_id', required=False)

    def get_qrcode_url(self, obj):
        return obj.qrcode.get_url(self.context['request']) if obj.qrcode else None

    class Meta:
        model = SocialAccount
        fields = ('qrcode_image_id', 'url', 'icon', 'title', 'id', 'qrcode_url')
        read_only_fields = ('is_active', 'qrcode_url')


class SiteProfileSerializer(serializers.ModelSerializer):
    """网站配置文件序列化"""
    social_accounts = serializers.SerializerMethodField(read_only=True)

    def get_social_accounts(self, _):
        return SocialAccountSerializer(
            SocialAccount.objects.all(),
            many=True,
            read_only=True,
            context=self.context
        ).data

    class Meta:
        model = SiteProfile
        fields = '__all__'
        read_only_fields = ('is_active',)


class CarouselSerializer(serializers.ModelSerializer):
    """轮播图序列化"""

    image_url = serializers.SerializerMethodField()
    image_id = serializers.IntegerField(write_only=True, source='attachment_id')

    def get_image_url(self, obj):
        return obj.attachment.get_url(self.context['request'])

    class Meta:
        model = Carousel
        fields = ('image_id', 'link', 'date_from', 'date_to', 'id', 'image_url')
        read_only_fields = ('is_active', 'image_url')

