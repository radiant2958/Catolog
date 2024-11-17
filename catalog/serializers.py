from rest_framework import serializers
from .models import Category, Material

class MaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Material
        fields = ['id', 'name', 'category', 'category_name', 'material_code', 'cost']

class CategorySerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'category_code', 'materials', 'subcategories', 'total_cost']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories, many=True).data

    def get_total_cost(self, obj):
        return obj.get_total_cost()
