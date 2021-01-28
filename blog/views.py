from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from ZhiQue import permissions
from .models import Category


class CategoryBreadcrumbView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, version):
        breadcrumb_dict = {}
        for category in Category.objects.all():
            if len(category.get_sub_categories()) == 0:
                breadcrumb_dict[str(category.get_category_path())] = list(map(lambda c: ({
                    'id': c.id,
                    'name': c.name,
                    'url': c.get_category_path()
                }), category.get_category_tree()))[::-1]
        return JsonResponse(breadcrumb_dict, status=status.HTTP_200_OK)