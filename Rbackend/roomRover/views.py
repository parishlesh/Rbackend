from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from .models import Room, RoomImage

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
            room_images = room.images.all()
            image_urls = [image.image.url for image in room_images]

            room_info = {
                'id': room.id,
                'user_id': room.user.id,
                'property_name': room.property_name,
                'city': room.city,
                'state': room.state,
                'other_facilities': room.other_facilities,
                'description': room.description,
                'parking_available': room.parking_available,
                'bachelors_allowed': room.bachelors_allowed,
                'contact': room.contact,
                'rent': room.rent,
                'images': image_urls,
            }
            room_data.append(room_info)

        return JsonResponse(room_data, safe=False)
@api_view(['GET'])
@csrf_exempt
def get_room_by_id(request, room_id):
    if request.method == "GET":
        try:
            room = Room.objects.get(pk=room_id)
            images = room.images.all()  # Adjust this line to use the correct related_name
            image_urls = [image.image.url for image in images]

            room_data = {
                'id': room.id,
                'property_name': room.property_name,
                'city': room.city,
                'state': room.state,
                'other_facilities': room.other_facilities,
                'description': room.description,
                'parking_available': room.parking_available,
                'bachelors_allowed': room.bachelors_allowed,
                'contact': room.contact,
                'rent': room.rent,
                'images': image_urls,
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
        other_facilities = request.data.get('other_facilities')
        description = request.data.get('description')
        parking_available = request.data.get('parking_available') == 'true'
        bachelors_allowed = request.data.get('bachelors_allowed') == 'true'
        contact = request.data.get('contact')
        rent = request.data.get('rent')
        
        pictures = request.FILES.getlist('pictures')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User is not registered'}, status=404)

        room = Room.objects.create(
            user=user,
            property_name=property_name,
            city=city,
            state=state,
            other_facilities= other_facilities,
            description=description,
            parking_available=parking_available,
            bachelors_allowed=bachelors_allowed,
            contact=contact,
            rent=rent,
        )

        for picture in pictures:
            RoomImage.objects.create(room=room, image=picture)

        return JsonResponse({'message': 'Room created successfully', 'room_id': room.id}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
