from django.db import models
from django.utils.text import slugify

# ============================================
# Catégorie de plats
# ============================================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # nom de la catégorie
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # pour SEO

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ============================================
# Plat ou boisson du menu
# ============================================
class MenuItem(models.Model):
    name = models.CharField(max_length=200)  # nom du plat
    description = models.TextField(blank=True)  # description optionnelle
    price = models.DecimalField(max_digits=10, decimal_places=2)  # prix
    available = models.BooleanField(default=True)  # disponible ou non
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.name} ({self.category.name})"
