import json
from django.http.response import Http404

from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status

from  activities.serializers import ActivitySerializer,ReviewSerializer,MediaSerializer,CategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from  activities.models import Activity,Review,Media,Category
from activities.forms import ActivityCreationForm, MediaCreationForm,ReviewCreationForm

def activity(request):
    activities = Activity.objects.all()
    activities = activities.filter(is_active=True)
    return render(
        request,
        "activity.html",
        {
            "activities": activities,
        }
    )
def activity_detail(request,id):
    return render(
        request,
        "activity_detail.html",
        {
            "activity": get_object_or_404(Activity,id=id),
        }
    )

def activity_comment(request,id):
    return render(
        request,
        "comments.html",
        {
            "activity": get_object_or_404(Activity,id=id),
        }
    )

@login_required(login_url='login')
def new_activity(request):
    form = ActivityCreationForm()

    if request.method == "POST":
        form = ActivityCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.info(
                request,
                'Tebrikler. Etkinliğiniz başarıyla oluşturuldu. '
                'Editör onayından geçtikten sonra yayınlanacaktır.'
            )
            return redirect('/')

    return  render(
        request,
        "new_activity.html",
        {
            "form" : form,
        }
    )
@login_required(login_url='login')
def activity_new_media(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    form = MediaCreationForm()

    if request.method == "POST":
        form = MediaCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.activity = activity
            form.save()
            return redirect(activity.get_absolute_url())

    return render(
        request,
        'activity_new_media.html',
        {
            'activity': activity,
            'form': form,
        }
    )


@login_required(login_url='login')
def activity_new_review(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    form = ReviewCreationForm()

    if request.method == "POST":
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.activity = activity
            form.save()
            return redirect(activity.get_absolute_url())

    return render(
        request,
        'new_review.html',
        {
            'activity': activity,
            'form': form,
        }
    )

@login_required(login_url="login")
def like_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.user in activity.likes.all():
        activity.likes.remove(request.user)
        action="unlike"

    else:
        activity.likes.add(request.user)
        action = "like"

    if request.is_ajax():
        return  HttpResponse(
            json.dumps({
                "count": activity.likes.count(),
                "action" :action,
            })
        )

    return redirect(activity.get_absolute_url())



class ActivityList(APIView):
    serializer_class = ActivitySerializer
    def get(self, request, format=None):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivitySingle(APIView):

    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity = ActivitySerializer(activity)
        return Response(activity.data)


class CategoryList(APIView):
    serializer_class = CategorySerializer

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
        reviews = Review.objects.filter(activity_id=pk)
        serializer =ReviewSerializer (reviews, many=True)
        return Response(serializer.data)


class MediaList(APIView):
    def get(self, request, format=None):
        medias = Media.objects.all()
        serializer =MediaSerializer (medias, many=True)
        return Response(serializer.data)

class MediaActivity(APIView):
    def get(self, request,pk, format=None):
        media = Media.objects.filter(activity_id=pk)
        serializer =MediaSerializer (media, many=True)
        return Response(serializer.data)

