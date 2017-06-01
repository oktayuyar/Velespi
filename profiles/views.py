from django.http.response import Http404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import(
 	login as auth_login,
 	logout as auth_logout
)
from django.contrib.auth import get_user_model

from profiles.forms import RegistrationForm,LoginForm
from  profiles.serializers import UserSerializer,UserLoginSerializer

def register(request):
    form=RegistrationForm()

    if request.method=="POST":
        form=RegistrationForm(request.POST)

        if form.is_valid(): # valid formdaki veriler geçerli mi dolumu
            form.save()

            messages.info(
                request,
                "Kayıt başarılı. Şimdi login olabilirsiniz"
            )
            return redirect("login")

    return render(request,"register.html",{
        "form" : form
    })


def login(request):
    form= LoginForm()

    if request.method=="POST":
        form =LoginForm(request.POST)

        if form.is_valid():
            auth_login(request, form.user)
            messages.info(
                request,
                "Giriş Yaptınız."
            )
            if request.GET.get("next"):
                return redirect(request.GET["next"])
            else:
                return  redirect("index")



    return render(request,"login.html",{
        "form" :form
    })



def logout(request):
    auth_logout(request)
    return redirect("/")

User=get_user_model()

class UserList(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = User.objects.all()
        serializer =UserSerializer (users, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSingle(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


    def post(self, request, format=None,*args,**kwargs):
        data=request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data=serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
