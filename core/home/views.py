from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from home.models import Person
from home.serializers import PersonSerializer, LoginSerializer, RegisterSerializer


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])
        
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid credentials',
            }, status=status.HTTP_400_BAD_REQUEST)
                     
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status': True,
            'message': 'Login successful',
            'token': str(token)
        }, status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response({
            'status': True,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@api_view(['GET', 'POST'])
def index(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'django', 'FastApi'],
        'course_provider': 'Udemy'
    }
    if request.method == 'GET':
        print('YOU HIT GET METHOD')
        return Response(courses)
    elif request.method == 'POST':
        print('YOU HIT POST METHOD')
        return Response(courses)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'success'})
    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        obj = get_object_or_404(Person, id=request.data['id'])
        serializer = PersonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        obj = get_object_or_404(Person, id=request.data['id'])
        serializer = PersonSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        obj = get_object_or_404(Person, id=request.data['id'])
        obj.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PersonSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        obj = get_object_or_404(Person, id=request.data['id'])
        serializer = PersonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        obj = get_object_or_404(Person, id=request.data['id'])
        serializer = PersonSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj = get_object_or_404(Person, id=request.data['id'])
        obj.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data}, status=status.HTTP_200_OK)
