from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeopleSerializers, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework import status  #for error status

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token #token authentication
from rest_framework.authentication import TokenAuthentication

#user model
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated          #for permissions
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        #If serializer is successful -- Token authentication
        user = authenticate(username =  serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'Invalid credentials!'
            }, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user = user)

        return Response({'status': True, 'message': "User Logged-In!", 'token': str(token)}, status.HTTP_201_CREATED)


class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        #If serializer is successfull
        serializer.save()
        return Response({'status': True, 'message': "User created!"}, status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])  #List method that api decorator will be able to accept
def index(request):
    courses = {
        'course_name' : 'Python',
        'learn' : ['flask', 'Django', 'Tornado', 'FastApi'],
        'course_provider': 'Scaler'
    }

    if request.method == 'GET':
        print("You HIT a GET method")
        return Response(courses)
    elif request.method == 'POST':
        data = request.data #To get the data from frontend which is passed in the form of JSON
        print('***************')
        print(data)
        print("You HIT a POST method")
        return Response(courses)

#Returning the data to frontend so response, instead of render.

@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message': 'Sucess!'})
    return Response(serializer.errors)

from django.core.paginator import Paginator  #Pagination
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        print(request.user)
        objs = Person.objects.filter(color__isnull=False)  # filter only displays the records with color values

        #Pagination
        page = request.GET.get('page', 1)
        page_size = 3  #able yo see only 3 records in one page
        paginator = Paginator(objs, page_size)
        print(paginator.page(page))

        serializer = PeopleSerializers(paginator.page(page), many=True)  # data can be more than 1 so we pass many
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PeopleSerializers(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Person deleted!'})


#API to get and create people:
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def people(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False) #filter only displays the records with color values
        serializer = PeopleSerializers(objs, many= True) #data can be more than 1 so we pass many
        serializer_context = {
            'request': (request),
        }
        context = serializer_context
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PeopleSerializers(obj, data=data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    # PUT -- Does not support partial updates
    # PATCH -- Supports partial updates

    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message': 'Person deleted!'})



#Model Viewsets:
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class =  PeopleSerializers
    queryset =  Person.objects.all()

    #To filter the names based on the search
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializers(queryset, many=True)
        return Response({'status': 200, 'data': serializer.data})