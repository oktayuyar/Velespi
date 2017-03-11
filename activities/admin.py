from django.contrib import admin
from  activities.models import (
    Activity,Category,Review,Media
)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0

class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name","user","route","category","review_count","description")
    list_editable = ("category",)
    actions = ("is_active",)  # , koymamızın sebebi tuple olması için (, koymazsak string olarak alıyor hata veriyor)
    search_fields = ("name","user__username")
    inlines = [MediaInline,
               ReviewInline
               ]

    def set_wifi_true(self,request,queryset):  # tüm wifi leri True yap
        queryset.update(has_wifi=True)
    set_wifi_true.short_description = "Tüm mekanların wifisi var yap"

admin.site.register(Activity,ActivityAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Media)


