from django.db import models
from django.conf import settings
from django.utils.encoding import smart_text

class Category(models.Model):
    name=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return smart_text(self.name)

class ActivityManager(models.Manager): # filtreleme kısmı çok fazla kullanacagımız fonksiyonları manager yaratıp onun
    # içine yazıyoruz her seferinde tekrar yazmamak için
    def get_queryset(self):
        gets=super(ActivityManager,self).get_queryset()
        return gets.filter(user__is_active=True)

    def active_activities(self):
        return self.get_queryset().filter(
            is_active=True,
            user__is_active=True
        )

class Activity(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name="added_activities")# kullanıının eklediği etkinlikleri getiriyor
    name=models.CharField(max_length=255)
    route=models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    is_active= models.BooleanField(default=False)
    category= models.ForeignKey(Category,blank=True,null=True) # blank True web sayfasında veri girerken boş bırakma
    telephone=models.CharField(max_length=255,blank=True,null=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   blank=True,
                                   related_name = 'liked_activities') # kullanıının begendigi etkinlikleri getiriyor

    objects=ActivityManager()
    all_objects=models.Manager()

    def __str__(self):
        return smart_text(self.name)

    @models.permalink
    def get_absolute_url(self):   # değişiklik yaptıgımızda hata almamak için
        return ("activity_detail",(self.id,))

    def review_count(self):
        return self.review_set.count()

class Review(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,related_name="added_review")
    activity = models.ForeignKey(Activity)
    comment = models.TextField(blank=True,null=True)



class Media(models.Model):
    activity = models.ForeignKey(Activity)
    image = models.ImageField(upload_to="activities")

    class Meta:
        verbose_name_plural = "Media"

    def __str__(self):
        return smart_text(self.image.url)

