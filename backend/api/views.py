from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # Import status for HTTP status codes
from .models import Planet, Star
from .serializers import PlanetSerializer, StarSerializer
from .ai_model import classify

class PredictPlanet(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data
        classification, confidence = classify(data) # type: ignore

        star_name = data.get('star_name', 'Unknown Star')
        star, _ = Star.objects.get_or_create(
            name=star_name,
            defaults={
                'ra': data.get('ra'),
                'dec': data.get('dec'),
                'star_temp': data.get('star_temp'),
                'star_radius': data.get('star_radius'),
            }
        )

        planet = Planet.objects.create(
            star=star,
            name=data.get('name'),
            orbital_period=data.get('orbital_period'),
            radius=data.get('radius'),
            ra=data.get('ra'),
            dec=data.get('dec'),
            duration=data.get('duration'),
            transit_depth=data.get('transit_depth'),
            star_temp=data.get('star_temp'),
            star_radius=data.get('star_radius'),
            model_snr=data.get('model_snr'),
            classification=classification,
            confidence=confidence
        )
        serializer = PlanetSerializer(planet)
        return Response(serializer.data)

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