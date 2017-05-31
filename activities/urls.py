from django.conf.urls import url

from activities import views

urlpatterns = [
    url(r"activities$", views.ActivityList.as_view(),
       name="api-activity-list"),

    url(r"activity/(?P<pk>[0-9]+)$", views.ActivitySingle.as_view(),
        name="api-activity-single"),

    url(r"activityreviews", views.ReviewList.as_view(),
        name="api-review-list"),

    url(r"activityreview/(?P<pk>[0-9]+)$", views.ReviewActivity.as_view(),
        name="api-review-list"),


    url(r"activitymedias", views.MediaList.as_view(),
        name="api-media-list"),

    url(r"activitymedia/(?P<pk>[0-9]+)$", views.MediaActivity.as_view(),
        name="api-media-single"),

    url(r"activitycategories", views.CategoryList.as_view(),
        name="api-category-list"),

    url(r"activitycategory/(?P<pk>[0-9]+)$", views.CategorySingle.as_view(),
        name="api-category-single"),

]