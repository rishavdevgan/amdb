from rest_framework.serializers import ModelSerializer
from models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'short_bio', 'created_on', 'updated_on', 'email')