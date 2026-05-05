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

    recipie_id = request.query_params.get("id")

    if not recipie_id:
        return Response({"error": "Recipe id is required"})

    try:
        recipie = Recipie.objects.get(id=recipie_id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipie not found"}, status=HTTP_404_NOT_FOUND)

    # 🔒 Check owner
    if recipie.user != request.user:
        return Response({"error": "Not allowed"}, status=HTTP_403_FORBIDDEN)

    recipie.delete()

    return Response({"message": "Recipie deleted successfully"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipie.models import Recipie

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_recipes(request):

    recipies = Recipie.objects.all().order_by('-date')

    data = []

    for r in recipies:
        data.append({
            "id": r.id,
            "title": r.title,
            "owner": r.user.name,
            "views": r.views,
            "difficulty_level": r.difficulty_level,
            "date": r.date,
            "images": request.build_absolute_uri(r.images.url) if r.images else None
        })

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
        recipie = Recipie.objects.get(id=id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 🔒 Only owner can edit
    if recipie.user != request.user:
        return Response({"error": "Not allowed"}, status=HTTP_403_FORBIDDEN)

    # Update fields
    recipie.title = request.data.get("title", recipie.title)
    recipie.ingredients = request.data.get("ingredients", recipie.ingredients)
    recipie.steps = request.data.get("steps", recipie.steps)
    recipie.cooking_time = request.data.get("cooking_time", recipie.cooking_time)
    recipie.difficulty_level = request.data.get("difficulty_level", recipie.difficulty_level)

    # Update image if provided
    if request.FILES.get("images"):
        recipie.images = request.FILES.get("images")

    recipie.save()

    return Response({"message": "Recipe updated successfully"}, status=HTTP_200_OK)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipie.models import Recipie

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyRecipies(request):

    recipies = Recipie.objects.filter(user=request.user).order_by('-date')

    data = []

    for r in recipies:
        data.append({
            "id": r.id,
            "title": r.title,
            "views": r.views,
            "date": r.date,
            "difficulty_level": r.difficulty_level,        
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
        recipie = Recipie.objects.get(id=id)
    except Recipie.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    # 👁️ increase views
    recipie.views += 1
    recipie.save()

    data = {
        "id": recipie.id,
        "title": recipie.title,
        "owner": recipie.user.name,
        "views": recipie.views,
        "ingredients": recipie.ingredients,
        "steps": recipie.steps,
        "cooking_time": recipie.cooking_time,
        "difficulty_level": recipie.difficulty_level,
        "images": request.build_absolute_uri(recipie.images.url) if recipie.images else None
    }

    return Response(data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateProfile(request):

    user = request.user

    name = request.data.get("name")
    email = request.data.get("email")

    if name:
        user.name = name
    if email:
        user.email = email

    user.save()

    return Response({"message": "Profile updated successfully"})    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    user = request.user

    return Response({
        "name": user.name,
        "email": user.email
    })    