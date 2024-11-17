from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, MaterialViewSet, UploadExcelView, FlatMaterialListView, CategoryTreeView # Удалите 'MaterialVariantViewSet'


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'materials', MaterialViewSet, basename='material')


urlpatterns = [
    path('', include(router.urls)),  
    path('upload-excel/', UploadExcelView.as_view(), name='upload-excel'), 
    path('materials-flat/', FlatMaterialListView.as_view(), name='materials-flat'),  
    path('category-tree/', CategoryTreeView.as_view(), name='category-tree'),
]
