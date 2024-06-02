from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from .models import Room

@api_view(['POST'])
@csrf_exempt
def userRegister(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if email and password:  # Ensure email and password are provided
            if not User.objects.filter(email=email).exists():  # Check if email already exists
                user = User.objects.create_user(username=username, password=password, email=email)
                return JsonResponse({'message': 'User created successfully', 'success':True}, status=201)
            else:
                return JsonResponse({'error': 'Email already exists','success':False}, status=400)
        else:
            return JsonResponse({'error': 'Email and password are required','success':False}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed','success':False}, status=405)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['POST'])
@csrf_exempt
def userLogin(request):
    if request.method == 'POST':
        print(request.body)
        email = request.data.get('email')
        password = request.data.get('password')
        # email = request.POST.email
        # password = request.POST.password
        print(request.data.get('email'))
        print(email)
        # Check if a user with the provided email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=400)
        
        # Authenticate the user using email and password
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful','token':token})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid email or password'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)

@api_view(['GET'])
@csrf_exempt
def get_all_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        room_data = []
        for room in rooms:
            room_dict = {
                'id': room.id,
                'property_name': room.property_name,
                'city': room.city,
                'state': room.state,
                'size': room.size,
                'description': room.description,
                'parking_available': room.parking_available,
                'bachelors_allowed': room.bachelors_allowed,
                'contact': room.contact,
                'rent': room.rent,
                'image': room.picture.url if room.picture else None,
            }
            room_data.append(room_dict)
        return JsonResponse({'rooms': room_data})
    
@api_view(['GET'])
@csrf_exempt
def get_room_by_id(request, room_id):
    if request.method == "GET":
        print(room_id)
        try:
            room = Room.objects.get(pk=room_id)
            room_data = {
                'id': room.id,
                'property_name': room.property_name,
                'city': room.city,
                'state': room.state,
                'size': room.size,
                'description': room.description,
                'parking_available': room.parking_available,
                'bachelors_allowed': room.bachelors_allowed,
                'contact': room.contact,
                'rent': room.rent,
                'image': room.picture.url if room.picture else None,
            }
            return JsonResponse(room_data)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room not found'}, status=404)
        
@api_view(['POST'])
@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        email = request.data.get('email')
        property_name = request.data.get('property_name')
        city = request.data.get('city')
        state = request.data.get('state')
        size = request.data.get('size')
        description = request.data.get('description')
        parking_available = request.data.get('parking_available') == 'true'
        bachelors_allowed = request.data.get('bachelors_allowed') == 'true'
        contact = request.data.get('contact')
        rent = request.data.get('rent')
        
        picture = request.FILES.get('picture')
        
        # Fetch the user object
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Create the room object
        room = Room.objects.create(
            user=user,
            property_name=property_name,
            city=city,
            state=state,
            size=size,
            description=description,
            parking_available=parking_available,
            bachelors_allowed=bachelors_allowed,
            contact=contact,
            rent=rent,
            picture=picture,
        )
        
        return JsonResponse({'message': 'Room created successfully', 'room_id': room.id}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)