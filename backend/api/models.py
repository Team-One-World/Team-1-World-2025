from django.db import models

class Star(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ra = models.FloatField(null=True, blank=True)
    dec = models.FloatField(null=True, blank=True)
    sy_dist = models.FloatField(null=True, blank=True)
    star_temp = models.FloatField(null=True, blank=True)
    star_radius = models.FloatField(null=True, blank=True)
    user_inputted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Planet(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name='planets', null=True)
    name = models.CharField(max_length=100, unique=True, blank=True)
    orbital_period = models.FloatField(null=True, blank=True)
    radius = models.FloatField(null=True, blank=True)
    ra = models.FloatField(null=True, blank=True)
    dec = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    transit_depth = models.FloatField(null=True, blank=True)
    star_temp = models.FloatField(null=True, blank=True)
    star_radius = models.FloatField(null=True, blank=True)
    model_snr = models.FloatField(null=True, blank=True)
    semi_major_axis = models.FloatField(null=True, blank=True)
    user_inputted = models.BooleanField(default=False)

    classification = models.CharField(max_length=20)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name