import re
from users.models import User
from rest_framework.exceptions import ParseError, ValidationError
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
            raise ValidationError("이메일 형식으로 입력해주세요. ")
        else: return email
        
    def validate_username(self, username):
        if not username:
            raise ValidationError("닉네임을 입력해주세요.")
        else: return username

    def validate_password(self, password):
        if password:
            if not re.search(r"[a-z]", password):
                raise ValidationError("비밀번호는 영문 소문자를 포함해야 합니다.")
            if not re.search(r"[A-Z]", password):
                raise ValidationError("비밀번호는 영문 대문자를 포함해야 합니다.")
            if not re.search(r"[0-9]", password):
                raise ValidationError("비밀번호는 숫자를 포함해야 합니다.")
            if not re.search(r'[~!@#$%^&*()_+{}":;\']', password):
                raise ValidationError("비밀번호는 특수문자(~!@#$%^&*()_+{}\":;')를 포함해야 합니다.")
            if len(password) < 8 or len(password) > 16:
                raise ValidationError("비밀번호는 8자 이상 16자 이하이어야 합니다.")
            print(password)
        else:
            raise ParseError("비밀번호를 입력하세요.")
        return password    