# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from uuid import uuid4
from datetime import datetime

class Mdg(models.Model):
    music_pk = models.AutoField(db_column='Music_pk', primary_key=True)  # Field name made lowercase.
    user_num = models.IntegerField(db_column='User_num')  # Field name made lowercase.
    artist = models.CharField(max_length=100)
    song = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    Site_Code = (
        ('M', 'Melon'),
        ('B', 'Bugs'),
        ('G', 'Genie'),
        ('F', 'FLO'),
        ('V', 'Vibe')
    )
    site_code = models.CharField(max_length=1, choices=Site_Code )
    genre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MDG'




class MdIntegratedM(models.Model):
    music_pk = models.AutoField(db_column='Music_pk', primary_key=True)  # Field name made lowercase.
    in_artist = models.CharField(max_length=50)
    in_song = models.CharField(max_length=50)
    in_album = models.CharField(max_length=100)
    in_genre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'MD_integrated_m'

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['post_file/', ymd_path, uuid_name])


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=100)
    password = models.IntegerField()
    post_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=45)
    post_contents = models.TextField(blank=True, help_text='Post Contents')
    post_like = models.IntegerField(default=0)
    post_hit = models.IntegerField(default=0)
    post_file = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    post_filename = models.CharField(max_length=100, null=True, verbose_name='첨부파일명')

    Table_num = (
        ('0', '국내'),
        ('1', '해외'),
        ('2', '기타'),
    )
    table_num = models.CharField(max_length=1, choices=Table_num)

    class Meta:
        managed = False
        db_table = 'Post'
        ordering = ['-post_id']

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('music:post_detail', args=[str(self.post_id)])

    def get_previous(self):
        return self.get_previous_by_post_date()

    def get_next(self):
        return self.get_next_by_post_date()




class Comment(models.Model):
    com_id = models.AutoField(primary_key=True)
    com_writer = models.CharField(max_length=100)
    com_password = models.IntegerField(default=0)     #비밀번호 일단 구현x
    com_date = models.DateTimeField(auto_now_add=True)
    com_contents = models.CharField(max_length=200)
    com_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        managed = False
        db_table = 'comment'
        ordering = ['-com_id']

