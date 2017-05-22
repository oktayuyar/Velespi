import json
from django.http.response import Http404

from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from  places.serializers import PlaceSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from  activities.models import Activity
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
    def get(self, request, format=None):
        activities = Activity.objects.all()
        serializer = PlaceSerializer(activities, many=True)

        return Response(serializer.data)


class ActivitySingle(APIView):

    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity = PlaceSerializer(activity)
        return Response(activity.data)
