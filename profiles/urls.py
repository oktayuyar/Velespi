from django.conf.urls import url

from profiles import views

urlpatterns = [
    url(r"users$", views.UserList.as_view(),
       name="api-user-list"),


    url(r"user/(?P<pk>[0-9]+)$", views.UserSingle.as_view(),
        name="api-review-list"),

]