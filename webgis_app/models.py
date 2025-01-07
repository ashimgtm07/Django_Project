from django.contrib.gis.db import models
class MyLocation(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()  # Store latitude and longitude
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Location: {self.location}, Name: {self.name}"
    
class Hospital(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    location = models.PointField(srid=4326)

    def __str__(self):
        return self.name if self.name else "No Name"