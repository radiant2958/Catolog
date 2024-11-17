from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Category, Material
from .serializers import CategorySerializer, MaterialSerializer
import pandas as pd
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import OuterRef, Subquery

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class UploadExcelView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Загрузить Excel-файл для импорта данных",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Excel-файл для загрузки",
            )
        ],
        responses={200: openapi.Response("Данные успешно загружены")},
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Файл не найден!"}, status=400)

        try:
            data = pd.read_excel(file)

            for _, row in data.iterrows():
                required_columns = {'Category', 'Category Code', 'Material Name', 'Material Code', 'Cost'}
                if not required_columns.issubset(row.index):
                    return Response(
                        {"error": f"Отсутствуют обязательные столбцы в файле! Ожидаются: {', '.join(required_columns)}."},
                        status=400,
                    )

                category_name = str(row['Category']).strip()
                category_code = str(row['Category Code']).strip()
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'category_code': category_code}
                )

                if not created and category.category_code != category_code:
                    return Response(
                        {"error": f"Конфликт кодов категории: '{category.name}'. Указан код {category_code}, ожидается {category.category_code}."},
                        status=400,
                    )

                material_code = str(row['Material Code']).strip()
                material_name = str(row['Material Name']).strip()
                material_cost = float(row['Cost'])

                material, material_created = Material.objects.get_or_create(
                    material_code=material_code,
                    defaults={
                        'name': material_name,
                        'category': category,
                        'cost': material_cost
                    }
                )

                if not material_created:
                    material.name = material_name
                    material.category = category
                    material.cost = material_cost
                    material.save()

            return Response({"message": "Данные успешно загружены в БД!"})
        except ValueError as e:
            return Response({"error": f"Ошибка в данных: {e}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class FlatMaterialListView(APIView):
    def get(self, request, *args, **kwargs):
        materials = Material.objects.values(
            'id', 'name', 'material_code', 'cost', 'category__name', 'category__category_code'
        )
        
        result = [
            {
                "id": material['id'],
                "name": material['name'],
                "material_code": material['material_code'],
                "cost": material['cost'],
                "category_name": material['category__name'],
                "category_code": material['category__category_code'],
            }
            for material in materials
        ]
        
        return Response(result)

class CategoryTreeView(APIView):
    def get(self, request, *args, **kwargs):
        root_categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(root_categories, many=True)
        return Response(serializer.data)