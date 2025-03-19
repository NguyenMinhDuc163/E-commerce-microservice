# serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Account, User, Address, Fullname

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }


    def create(self, validated_data):
        # Xử lý trường profile trước
        username = validated_data.pop('username', None)

        try:
            password = validated_data.pop('password')  # Lấy mật khẩu từ dữ liệu validated
            hashed_password = make_password(password)  # Mã hóa mật khẩu
            # Kiểm tra dữ liệu hợp lệ trước khi tạo đối tượng
            if not hashed_password:
                raise serializers.ValidationError("Password is required.")

            account = Account.objects.create(password=hashed_password, username=username)
            return account
        except Exception as e:
            raise serializers.ValidationError(e)

class FullnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fullname
        fields = ['first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='fullname.first_name', required=False, write_only=True)
    last_name = serializers.CharField(source='fullname.last_name', required=False, write_only=True)
    address_ = serializers.CharField(source='address.address', required=False, write_only=True)
    username = serializers.CharField(source='account.username', write_only=True)
    password = serializers.CharField(source='account.password', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'account', 'email', 'phone', 'fullname', 'address','address_','first_name', 'last_name', 'username', 'password']
        depth = 1

    def create(self, validated_data):
        print(validated_data)
        address_data = validated_data.pop('address', None)
        fullname_data = validated_data.pop('fullname', None)
        account_data = validated_data.pop('account', None)

        try:
            serializer = AccountSerializer(data=account_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializers.errors)
            else:
                account = serializer.save()

        except Exception as e:
            raise serializers.ValidationError(e)

        address = Address.objects.create(address=address_data['address'])
        fullname = Fullname.objects.create(first_name=fullname_data['first_name'], last_name=fullname_data['last_name'])

        user = User.objects.create(account=account, address=address, fullname=fullname, **validated_data)
        return user




