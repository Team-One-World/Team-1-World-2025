from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # Import status for HTTP status codes
from .models import Planet, Star
from .serializers import PlanetSerializer, StarSerializer
from .ai_model import classify


class PredictPlanet(APIView):
    print("PredictPlanet view initialized")
    authentication_classes = []
    permission_classes = []

    def clean_input(self, data):
        """Convert empty strings to None for cleaner validation."""
        return {
            k: (v if v not in ["", None, "null"] else None)
            for k, v in data.items()
        }

    def post(self, request):
        data = self.clean_input(request.data)
        print("Cleaned request data:", data)

        classification_fields = [
            "orbital_period", "radius", "duration",
            "transit_depth", "star_temp", "star_radius", "model_snr"
        ]

        save_fields = classification_fields + ["name", "ra", "dec", "star_name"]

        # Only require classification fields to exist and be non-null
        has_classification_fields = all(
            field in data and data[field] not in [None, ""]
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

        # Check if all save fields are filled in
        has_save_fields = all(
            field in data and data[field] not in [None, ""]
            for field in save_fields
        )

        if has_save_fields:
            # Save Star first
            star_name = data.get("star_name") + " (user inputted)"
            star, created = Star.objects.get_or_create(
                name=star_name,
                defaults={
                    "ra": data.get("ra"),
                    "dec": data.get("dec"),
                    "star_temp": data.get("star_temp"),
                    "star_radius": data.get("star_radius"),
                    "user_inputted": True,
                }
            )
            if not created:
                star.user_inputted = True
                star.save()

            # Save Planet
            planet = Planet.objects.create(
                user_inputted=True,
                star=star,
                name=data.get("name") + " (user inputted)",
                orbital_period=data.get("orbital_period"),
                radius=data.get("radius"),
                ra=data.get("ra"),
                dec=data.get("dec"),
                duration=data.get("duration"),
                transit_depth=data.get("transit_depth"),
                star_temp=data.get("star_temp"),
                star_radius=data.get("star_radius"),
                model_snr=data.get("model_snr"),
                classification=classification,
                confidence=confidence,
            )
            serializer = PlanetSerializer(planet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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