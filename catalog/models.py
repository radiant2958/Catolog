from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True
    )
    category_code = models.CharField(max_length=50, unique=True)

    def get_total_cost(self):
        """
        Рекурсивно вычисляет сумму стоимости всех материалов в текущей категории
        и во всех дочерних категориях.
        """
        total_cost = sum(material.cost for material in self.materials.all())
        for child in self.subcategories.all():
            total_cost += child.get_total_cost()
        return total_cost

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='materials')
    material_code = models.CharField(max_length=50, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
