from django.db import models
from .geojsonfield import GeoJSONSchemaField
import uuid

# Create your models here.
class ProviderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phoneNumber = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mozio"
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.name

class ServiceAreaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    geoJson = GeoJSONSchemaField(
        schema='schemas/geojson_schema.json', default=dict, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-createdAt']

        def __str__(self) -> str:
            return self.name