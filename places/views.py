import json
from django.http.response import Http404

from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status

from  places.serializers import PlaceSerializer,CategorySerializer,MediaSerializer,ReviewSerializer, PlaceNameSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


from  places.models import Place,Media,Review,Category
from places.forms import PlaceCreationForm, MediaCreationForm,ReviewCreationForm


def index(request):
    return render(
        request,
        "index.html",
        {
            "places": Place.objects.all(),
        }
    )

def detail(request,id):
    return render(
        request,
        "place.html",
        {
            "place": get_object_or_404(Place,id=id),
        }
    )
@login_required(login_url='login')
def new_place(request):
    form = PlaceCreationForm()

    if request.method == "POST":
        form = PlaceCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.info(
                request,
                'Tebrikler. Yer bildiriminiz başarıyla alındı. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect('/')

    return  render(
        request,
        "new_place.html",
        {
            "form" : form,
        }
    )
@login_required(login_url='login')
def new_media(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    form = MediaCreationForm()

    if request.method == "POST":
        form = MediaCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.place = place
            form.save()
            return redirect(place.get_absolute_url())

    return render(
        request,
        'new_media.html',
        {
            'place': place,
            'form': form,
        }
    )


@login_required(login_url='login')
def new_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    form = ReviewCreationForm()

    if request.method == "POST":
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.place = place
            form.save()
            return redirect(place.get_absolute_url())

    return render(
        request,
        'new_review.html',
        {
            'place': place,
            'form': form,
        }
    )

@login_required(login_url="login")
def like_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    if request.user in place.likes.all():
        place.likes.remove(request.user)
        action="unlike"

    else:
        place.likes.add(request.user)
        action = "like"

    if request.is_ajax():
        return  HttpResponse(
            json.dumps({
                "count": place.likes.count(),
                "action" :action,
            })
        )

    return redirect(place.get_absolute_url())


class PlaceList(APIView):
    serializer_class = PlaceSerializer

    def get(self, request, format=None):
        places = Place.objects.all()
        serializer = PlaceNameSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PlaceSingle(APIView):

    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        place = PlaceSerializer(place)
        return Response(place.data)

class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer =CategorySerializer (categories, many=True)
        return Response(serializer.data)


class CategorySingle(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        category = CategorySerializer(category)
        return Response(category.data)



class ReviewList(APIView):
    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer =ReviewSerializer (reviews, many=True)
        return Response(serializer.data)


class ReviewActivity(APIView):
    def get(self, request,pk, format=None):
        reviews = Review.objects.filter(place_id=pk)
        serializer =ReviewSerializer (reviews, many=True)
        return Response(serializer.data)


class MediaList(APIView):
    def get(self, request, format=None):
        medias = Media.objects.all()
        serializer =MediaSerializer (medias, many=True)
        return Response(serializer.data)

class MediaActivity(APIView):
    def get(self, request,pk, format=None):
        media = Media.objects.filter(place_id=pk)
        serializer =MediaSerializer (media, many=True)
        return Response(serializer.data)

