from django.contrib import admin
from music.models import *

# Register your models here.

class MusicDataGetAdmin(admin.ModelAdmin):
    list_display = ['music_pk', 'song', 'artist', 'album', 'genre', 'site_code', 'user_num']
    list_display_links = ['music_pk', 'user_num']

class MDIAdmin(admin.ModelAdmin):
    list_display = ['music_pk', 'in_song', 'in_artist', 'in_album', 'in_genre']
    list_display_links = ['music_pk']

admin.site.register(Mdg, MusicDataGetAdmin)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(MdIntegratedM, MDIAdmin)
