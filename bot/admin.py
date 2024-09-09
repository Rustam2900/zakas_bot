from django.contrib import admin
from bot.models import User, Image, NameRole, MandatoryUser,Video,OrderVideo


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name', 'username')
    search_fields = ('telegram_id', 'name', 'username')
    list_filter = ('name', 'username')


@admin.register(MandatoryUser)
class MandatoryUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'name', 'url', 'channel_id')
    search_fields = ('name', 'url', 'channel_id')
    list_filter = ('name',)

admin.site.register(NameRole)
admin.site.register(OrderVideo)
# @admin.register(NameRole)
# class RolesImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'roleimage_mandatory_id', 'name')
#     search_fields = ('name',)
#     list_filter = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_id', 'image')
    search_fields = ('role_id',)
    list_filter = ('role_id',)

admin.site.register(Video)