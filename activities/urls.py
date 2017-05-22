from django.conf.urls import url

from activities import views

urlpatterns = [
    url(r"activities$", views.ActivityList.as_view(),
       name="api-activity-list"),
    url(r"activities/(?P<pk>[0-9]+)$", views.ActivitySingle.as_view(),
        name="api-activity-single"),
]