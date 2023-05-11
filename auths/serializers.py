from users.models import User
from rest_framework.exceptions import ParseError
from rest_framework.serializers import ModelSerializer

class RegisterSerializers(ModelSerializer):
    class Meta:
        model=User
        fields=(
            "email",
            "password",
            "username",
        )        

    def validate_email(self, email):
        if not email:
            raise ParseError("이메일 형식으로 입력해주세요. ")
        else: return email
        
    def validate_username(self, username):
        if not username:
            raise ParseError("닉네임을 입력해주세요.")
        else: return username