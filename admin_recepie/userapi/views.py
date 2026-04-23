from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

from recipie.models import User

@api_view(['POST'])
@permission_classes((AllowAny,))
def Signup(request):

    email = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")
    phone = request.data.get("phone")
    image = request.FILES.get("image")
  

    # Validation
    if not email or not password or not name:
        return JsonResponse({'message': 'All fields are required'})

    # Check duplicate
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    # Create user
    user = User.objects.create_user(
        email=email,
        password=password
    )

    # Save extra fields
    user.name = name
    user.phone_number = phone
    user.images = image
    user.save()

    return JsonResponse({'message': 'User created successfully'}, status=200)

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def UserLogin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from recipie.models import Recipie

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_recipe(request):
    title = request.data.get("title")
    ingredients = request.data.get("ingredients")
    steps = request.data.get("steps")
    cooking_time = request.data.get("cooking_time")
    difficulty_level = request.data.get("difficulty_level")
    images = request.FILES.get("images")

    if not all([title, ingredients, steps, cooking_time, difficulty_level]):
        return Response(
            {"error": "All fields are required"},
            status=HTTP_400_BAD_REQUEST
        )

    recipie = Recipie.objects.create(
        user=request.user,
        title=title,
        ingredients=ingredients,
        steps=steps,
        cooking_time=cooking_time,
        difficulty_level=difficulty_level,
        images=images
    )

    return Response(
        {
            "message": "Recipie created successfully",
            "id": recipie.id
        },
        status=HTTP_200_OK
    )