from django.conf.urls import url

from places import views

urlpatterns = [
    url(r"places$", views.PlaceList.as_view(),
       name="api-place-list"),
    url(r"places/(?P<pk>[0-9]+)$", views.PlaceSingle.as_view(),
        name="api-place-single"),
]