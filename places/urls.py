from django.conf.urls import url

from places import views

urlpatterns = [
    url(r"places$", views.PlaceList.as_view(),
       name="api-place-list"),
    url(r"place/(?P<pk>[0-9]+)$", views.PlaceSingle.as_view(),
        name="api-place-single"),

    url(r"placereviews", views.ReviewList.as_view(),
        name="api-review-list"),

    url(r"placereview/(?P<pk>[0-9]+)$", views.ReviewActivity.as_view(),
        name="api-review-list"),

    url(r"placemedias", views.MediaList.as_view(),
        name="api-media-list"),

    url(r"placemedia/(?P<pk>[0-9]+)$", views.MediaActivity.as_view(),
        name="api-media-single"),

    url(r"placecategories", views.CategoryList.as_view(),
        name="api-category-list"),

    url(r"placecategory/(?P<pk>[0-9]+)$", views.CategorySingle.as_view(),
        name="api-category-single"),

]