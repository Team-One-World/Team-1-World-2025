from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Planet, Star
from .serializers import PlanetSerializer, StarSerializer
from .ai_model import classify


class PredictPlanet(APIView):
    print("PredictPlanet view initialized")
    authentication_classes = []
    permission_classes = []

    def clean_input(self, data):
        """Convert empty strings to None for cleaner validation."""
        # Use a list of values to consider as "empty"
        empty_values = ["", None, "null", "undefined"] # Added "undefined" just in case frontend sends it
        return {
            k: (v if v not in empty_values else None)
            for k, v in data.items()
        }

    def post(self, request):
        data = self.clean_input(request.data)
        print("Cleaned request data:", data)

        classification_fields = [
            "orbital_period", "radius", "duration",
            "transit_depth", "star_temp", "star_radius", "model_snr"
        ]

        # All fields that might be saved to Star or Planet models
        save_fields = classification_fields + [
            "name", "ra", "dec", "star_name",
            "sy_dist",          # ✅ New: Star System Distance
            "semi_major_axis",  # ✅ New: Planet Semi-Major Axis
        ]

        # Only require classification fields to exist and be non-null for classification
        has_classification_fields = all(
            field in data and data[field] is not None
            for field in classification_fields
        )

        if not has_classification_fields:
            return Response(
                {"error": "Missing one or more fields required for classification."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Run ML model classification
        try:
            classification, confidence = classify(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("❌ Classification error:", e)
            return Response({"error": "Error during classification."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if all relevant save fields are present/not None for saving purposes.
        # We'll save if star_name and planet name are provided,
        # otherwise just return classification.
        can_save_star_and_planet = data.get("star_name") and data.get("name") # Only save if both names are provided

        if can_save_star_and_planet:
            # Save Star first
            star_name = data["star_name"] + " (user inputted)"
            star, created = Star.objects.get_or_create(
                name=star_name,
                defaults={
                    "ra": data.get("ra"),
                    "dec": data.get("dec"),
                    "star_temp": data.get("star_temp"),
                    "star_radius": data.get("star_radius"),
                    "sy_dist": data.get("sy_dist"), # ✅ Save sy_dist to Star
                    "user_inputted": True,
                }
            )
            if not created:
                # If star already exists, update user_inputted flag and sy_dist if provided
                star.user_inputted = True
                if data.get("ra") is not None: star.ra = data["ra"]
                if data.get("dec") is not None: star.dec = data["dec"]
                if data.get("star_temp") is not None: star.star_temp = data["star_temp"]
                if data.get("star_radius") is not None: star.star_radius = data["star_radius"]
                if data.get("sy_dist") is not None: star.sy_dist = data["sy_dist"] # ✅ Update sy_dist
                star.save()

            # Save Planet
            planet = Planet.objects.create(
                user_inputted=True,
                star=star,
                name=data.get("name") + " (user inputted)",
                orbital_period=data.get("orbital_period"),
                radius=data.get("radius"),
                ra=data.get("ra"), # Planet RA/Dec might be slightly different than Star's, keep for now
                dec=data.get("dec"), # Assuming it means the planet's apparent RA/Dec or star's
                duration=data.get("duration"),
                transit_depth=data.get("transit_depth"),
                star_temp=data.get("star_temp"), # These are properties of the star, but might be duplicated for planet data completeness
                star_radius=data.get("star_radius"),
                model_snr=data.get("model_snr"),
                semi_major_axis=data.get("semi_major_axis"), # ✅ Save semi_major_axis to Planet
                classification=classification,
                confidence=confidence,
            )
            serializer = PlanetSerializer(planet)
            # Add classification and confidence to the serialized data if not already there
            response_data = serializer.data
            response_data['classification'] = classification
            response_data['confidence'] = confidence
            return Response(response_data, status=status.HTTP_201_CREATED)

        # Otherwise — only return the classification
        return Response(
            {"classification": classification, "confidence": confidence},
            status=status.HTTP_200_OK
        )


class PlanetList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        planets = Planet.objects.all().select_related('star')

        classification = request.query_params.get('classification')
        if classification:
            planets = planets.filter(classification=classification)

        search = request.query_params.get('search')
        if search:
            planets = planets.filter(name__icontains=search)

        serializer = PlanetSerializer(planets, many=True)
        return Response(serializer.data)

class StarList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        stars = Star.objects.all()
        serializer = StarSerializer(stars, many=True)
        return Response(serializer.data)

class StarPlanetList(APIView):
    """
    View to list all planets for a specific star.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, star_id):
        try:
            # Find the star by its primary key (id)
            star = Star.objects.get(pk=star_id)
        except Star.DoesNotExist:
            # If the star doesn't exist, return a 404 Not Found response
            return Response(
                {"error": "Star not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all planets related to this star using the 'related_name' from the model
        planets = star.planets.all()

        # Serialize the list of planets
        serializer = PlanetSerializer(planets, many=True)

        # Return the serialized data in the response
        print(serializer.data)
        return Response(serializer.data)