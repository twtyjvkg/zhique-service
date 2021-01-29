#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework import serializers


class ArticleCategoryField(serializers.RelatedField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        tree = value.get_category_tree()
        return {
            'id': value.id,
            'name': value.name,
            'url': value.get_category_path(),
            'tree': list(map(lambda t: t.id, tree))[::-1]
        }


class ArticleAuthorField(serializers.RelatedField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return {'id': value.id,
                'name': value.__str__(),
                'avatar': '/api/v1/auth/user_avatar?user_id={user_id}&avatar_id={avatar_id}'.format(
                    user_id=value.id, avatar_id=value.avatar) if value.avatar else None}