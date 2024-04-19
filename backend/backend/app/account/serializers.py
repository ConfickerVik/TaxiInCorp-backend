from rest_framework import serializers
from .models import User, UserRole, Car


class UserCarSerializers(serializers.ModelSerializer):
    car_brand = serializers.CharField(max_length=50,  allow_blank=True)
    car_plate = serializers.CharField(max_length=9, allow_blank=True)

    class Meta:
        model = Car
        fields = ["car_brand", "car_model", "car_color", "car_plate"]


class UserSerializer(serializers.ModelSerializer):
    car = UserCarSerializers(required=False, write_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["phone_number", "first_name", "last_name", "about_info", "password", "fk_role", "car"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        data = super().validate(attrs)
        check_car = all(data.get("car").values()) if data.get("car") else dict()
        if not check_car and data.get("fk_role").role == UserRole.ROLE_CHOICES.drive:
            raise serializers.ValidationError("Введи данные о машине!")
        return data

    def create(self, validated_data):
        car_set = validated_data.pop("car", None)
        user = User.objects.create_user(**validated_data)
        print(user)
        if user and validated_data["fk_role"].role == UserRole.ROLE_CHOICES.drive:
            Car.objects.create(**car_set, fk_user=user)
        return user
