from django.shortcuts import redirect
from social_django.utils import psa
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Shop
from .serializer import ShopSerializer,RegisterSerializer,UserSerializer,LoginSerializer
from geopy.distance import geodesic
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import  status



# Register API
class RegisterAPI(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        
        })


class LoginAPI(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class LogoutApiView(APIView):
    def get(self, request, format=None):

        # simply delete the token to force a login
        request.user.jwt_token.delete()
        return Response(status=status.HTTP_200_OK)

# Create your views here.


class Shopget(APIView):
    def get(self, request , latitude, langitude,*arg,**kwarg):
        import pdb
        pdb.set_trace()
        shops = Shop.objects.all()
        user_location = (int(latitude), int(langitude))
        NearByShop = []
        for shop in shops:
            Shop.objects.all()
            shop_location = (shop.latitude, shop.langitude)
            distance = geodesic(user_location, shop_location).km
            if distance < 10 :
                NearByShop.append(shop)
                serializer = ShopSerializer(NearByShop, many=True)
            return Response(serializer.data)




class ShopUpdate(APIView):

    def get(self,request,*arg):
        shops = Shop.objects.all()
        serializer= ShopSerializer(shops,many=True)
        return Response(serializer.data)
    

    def post(self, request, *arg,**kwarg):
        serializer = ShopSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.error, status = 400)


class SocialAuthView(APIView):
    @psa('social:complete')
    def post(self, request, backend):
        return redirect('http://localhost:3000/home/')