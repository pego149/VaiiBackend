from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

from api.models import Pouzivatel, Sprava, Miestnost, Post
from api.serializers import UserSerializer, MyTokenObtainPairSerializer, MessageSerializer, MiestnostSerializer, \
    PostSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PouzivatelViewSet(viewsets.ModelViewSet):
    queryset = Pouzivatel.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AllowAny]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class SpravaViewSet(viewsets.ModelViewSet):
    queryset = Sprava.objects.all()
    serializer_class = MessageSerializer


def message_view(request, sender, receiver):
    if request.method == "GET":
        messages = Sprava.objects.filter(
            Q(odosielatel_id=sender, prijmatel_id=receiver) | Q(odosielatel_id=receiver, prijmatel_id=sender)).order_by("-timestamp")[0:10]
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


def message_list(request, user):
    if request.method == "GET":
        messages = Sprava.objects.filter(Q(odosielatel_id=user) | Q(prijmatel_id=user)).order_by("-timestamp")
        messagelist = list(messages)
        newmessagelist = []
        myid = user
        othersids = []
        for s in iter(messagelist):
            if myid != s.odosielatel_id and s.odosielatel_id not in othersids:
                othersids.append(s.odosielatel_id)
            if myid != s.prijmatel_id and s.prijmatel_id not in othersids:
                othersids.append(s.prijmatel_id)
        for i in iter(messagelist):
            if i.odosielatel_id in othersids:
                newmessagelist.append(i)
                othersids.remove(i.odosielatel_id)
            if i.prijmatel_id in othersids:
                newmessagelist.append(i)
                othersids.remove(i.prijmatel_id)
        if not newmessagelist:
            return JsonResponse({}, safe=False)
        for s in iter(newmessagelist):
            if myid == s.odosielatel_id:
                s.odosielatel_id = s.prijmatel_id
            else:
                s.prijmatel_id = s.odosielatel_id
        serializer = MessageSerializer(newmessagelist, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


class MiestnostViewSet(viewsets.ModelViewSet):
    queryset = Miestnost.objects.all()
    serializer_class = MiestnostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def posts_view(request, miestnost):
    if request.method == "GET":
        posts = Post.objects.filter(miestnost_id=miestnost).order_by('-timestamp')[0:10]
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


def logout_view(request):
    return HttpResponse('<h1>Logout</h1>')
