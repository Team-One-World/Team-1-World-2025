from rest_framework import serializers
import math
from .models import Star, Planet

class SafeFloatField(serializers.FloatField):
    def to_representation(self, value):
        if value is None:
            return None
        # Handle NaN and Inf specifically
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return super().to_representation(value)

class StarSerializer(serializers.ModelSerializer):
    ra = SafeFloatField()
    dec = SafeFloatField()
    star_temp = SafeFloatField()
    star_radius = SafeFloatField()
    sy_dist = SafeFloatField() # ✅ Explicitly define sy_dist

    class Meta:
        model = Star
        fields = "__all__"

class PlanetSerializer(serializers.ModelSerializer):
    orbital_period = SafeFloatField()
    radius = SafeFloatField()
    ra = SafeFloatField()
    dec = SafeFloatField()
    duration = SafeFloatField()
    transit_depth = SafeFloatField()
    model_snr = SafeFloatField()
    semi_major_axis = SafeFloatField() # ✅ Explicitly define semi_major_axis

    class Meta:
        model = Planet
        fields = "__all__"