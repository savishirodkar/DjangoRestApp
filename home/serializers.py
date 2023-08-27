#Model Serializer -- Most Common type
from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username is taken!")

        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email is taken!")

        return data

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

#Create serializer to show django what data has to be displayed from the Model
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']
class PeopleSerializers(serializers.ModelSerializer):
    color = ColorSerializer()
    color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        # exclude = ['name'] --- to exclude the 'name' field
        fields = '__all__'
        # fields = ['name', 'age']
        # '__all__' to include all the fields of models

        # depth = 1  -- specifies how many levels of nested relationships should be included when serializing an object

    #To use the serializer method --- use 'get' prefix
    def get_color_info(self, obj):
        #fetching data from other table
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_name': color_obj.color_name, 'hex_code': '#000' }

        #Validation methods:
    def validate(self, data):
        special_characters = "!@#$%^&*()_+?_=,<>/"
        if any(c in special_characters for c in data['name']):
            raise  serializers.ValidationError("Name cannot contain special character!")
        if data['age'] < 18:
            raise serializers.ValidationError('Age should be greater than 18!')
        return data

