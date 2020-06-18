from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from music import views, move_csv
#from music import mdgCrawling

app_name = 'music'

urlpatterns = [
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('postlist/', views.PostListView.as_view(), name='post_list'),
    path('mdglist/', views.MDGListView.as_view(), name='mdg_list'),
    path('mdglist/delete/', views.MDGDelete, name="mdg_delete"),
    #path('mdglist/delete/<int:randuser>', views_re.MDGDelete, name="mdg_delete"),
    #path('mdglist/delete/<int:pk>', views.MDGDelete, name="mdg_delete"),
    path('', views.SiteMain, name='SiteMain'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/write', views.post_write, name='post_write'),
    path('post/update/<int:pk>', views.post_update, name='post_update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('mdgget/', views.mdg_get, name='mdg_get'),
    path('mdgup/', views.mdg_up, name='mdg_up'),
    #path('result/', move_csv.move_to_genie, name='result'),
    path('re_result/', views.Recmd, name='re_result'),
    path('post/<int:pk>/comment/', views.comment_write, name='comment_write'),
    path('post/download/<int:pk>', views.post_download_view, name="post_download"),
    path('user_guide/', views.user_guide, name="user_guide"),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)