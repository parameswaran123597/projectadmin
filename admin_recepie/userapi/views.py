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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangePassword(request):

    user = request.user

    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    # Check fields
    if not old_password or not new_password or not confirm_password:
        return JsonResponse({'message': 'All fields are required'})

    # Check old password
    if not user.check_password(old_password):
        return JsonResponse({'message': 'Old password is incorrect'})

    # Check new password match
    if new_password != confirm_password:
        return JsonResponse({'message': 'Passwords do not match'})

    # Set new password
    user.set_password(new_password)
    user.save()

    return JsonResponse({'message': 'Password changed successfully'}, status=200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipie.models import Recipie
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteRecipie(request):

    recipe_id = request.query_params.get("id")

    if not recipe_id:
        return Response({"error": "Recipe id is required"})

    try:
        recipe = Recipie.objects.get(id=recipe_id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 🔒 Check owner
    if recipe.user != request.user:
        return Response({"error": "Not allowed"}, status=HTTP_403_FORBIDDEN)

    recipe.delete()

    return Response({"message": "Recipe deleted successfully"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipie.models import Recipie

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_recipes(request):

    recipes = Recipie.objects.all().order_by('-date')

    data = []

    for r in recipes:
        data.append({
            "id": r.id,
            "title": r.title,
            "owner": r.user.name,
            "views": r.views,
            "images": request.build_absolute_uri(r.images.url) if r.images else None
        })

    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipie.models import Recipie
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recipe(request, id):

    try:
        recipe = Recipie.objects.get(id=id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 🔒 Only owner can view (optional, but recommended)
    if recipe.user != request.user:
        return Response({"error": "Not allowed"}, status=HTTP_403_FORBIDDEN)

    data = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "cooking_time": recipe.cooking_time,
        "difficulty_level": recipe.difficulty_level,
        "images": request.build_absolute_uri(recipe.images.url) if recipe.images else None
    }

    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipie.models import Recipie
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_200_OK

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_recipe(request, id):

    try:
        recipe = Recipie.objects.get(id=id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 🔒 Only owner can edit
    if recipe.user != request.user:
        return Response({"error": "Not allowed"}, status=HTTP_403_FORBIDDEN)

    # Update fields
    recipe.title = request.data.get("title", recipe.title)
    recipe.ingredients = request.data.get("ingredients", recipe.ingredients)
    recipe.steps = request.data.get("steps", recipe.steps)
    recipe.cooking_time = request.data.get("cooking_time", recipe.cooking_time)
    recipe.difficulty_level = request.data.get("difficulty_level", recipe.difficulty_level)

    # Update image if provided
    if request.FILES.get("images"):
        recipe.images = request.FILES.get("images")

    recipe.save()

    return Response({"message": "Recipe updated successfully"}, status=HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipie.models import Recipie

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyRecipies(request):

    recipes = Recipie.objects.filter(user=request.user).order_by('-date')

    data = []

    for r in recipes:
        data.append({
            "id": r.id,
            "title": r.title,
            "views": r.views,
            "images": request.build_absolute_uri(r.images.url) if r.images else None
        })

    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from recipie.models import Recipie
from rest_framework.status import HTTP_404_NOT_FOUND

@api_view(['GET'])
@permission_classes([AllowAny])
def RecipieDetails(request, id):

    try:
        recipe = Recipie.objects.get(id=id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 👁️ increase views
    recipe.views += 1
    recipe.save()

    data = {
        "id": recipe.id,
        "title": recipe.title,
        "owner": recipe.user.name,
        "views": recipe.views,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "cooking_time": recipe.cooking_time,
        "difficulty_level": recipe.difficulty_level,
        "images": request.build_absolute_uri(recipe.images.url) if recipe.images else None
    }

    return Response(data)