import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreatePostForm
from .models import Post, Comment, Mdg, MdIntegratedM
from django.contrib import messages
import datetime, random
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import urllib
import mimetypes
from . import move_csv, new_crawling


class MDGListView(generic.ListView):
    model = Mdg
    context_object_name = 'mdgs'


class AgreementView(generic.View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'music/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            if request.POST.get('yes'):
                return HttpResponse('<script type="text/javascript">window.close()</script>')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'music/agreement.html')

def MDGDelete(request):
    selected = Mdg.objects.all()
    putmusic = MdIntegratedM.objects.all()
    count = 0
    for i in range(len(selected)): # MdIntegratedM에 데이터 저장 및 중복 확인
        for j in range(len(putmusic)):
            if putmusic[j].in_song == selected[i].song and putmusic[j].in_album == selected[i].album and selected[i].site_code == 'M':
                #print(selected[i].song, selected[i].site_code)
                count += 1
        if count == 0 and selected[i].site_code == 'M':
            MdIntegratedM.objects.create(in_artist=selected[i].artist, in_song=selected[i].song, in_album = selected[i].album, in_genre=selected[i].genre)
           # print(selected[i].song, selected[i].site_code)
        count = 0

    selected.delete()
    return redirect('music:SiteMain')


def mdg_get(request):
    #url = request.POST.get('url')
    id = request.POST.get('id')
    password = request.POST.get('password')
    site = request.POST.get('site')
    #randuser = new_crawling.get_music(site, id, password)
    context = {'randusers': new_crawling.get_music(site, id, password)}
    print(context)
    #return render(request, 'music/mdg_list.html', context)
    return redirect('music:mdg_list')



def mdg_up(request):
    if request.FILES.__len__() == 0:
        message = "no file."
        return JsonResponse({"message": message})
    uploadFile = request.FILES['file'];
    # csv파일이 아니라면 작업을 멈추고 리턴합니다.
    if uploadFile.name.find('csv') < 0:
        message = "wrong file"
        return JsonResponse({"message": message})
    read = uploadFile.read().decode('UTF-8')
    # 줄바꿈이 생기는 것을 기준으로 배열
    list = []
    id = request.POST.get('id')
    password = request.POST.get('password')
    site = request.POST.get('site')
    readLine = read.split('\r\r\n')
    for line in readLine:
        list.append([line.replace("\\", " - ")])
    if site == 'genie':
        context = {'notfounds': move_csv.move_to_genie(id, password, list)}
        return render(request, 'music/result.html', context)
    if site == 'melon':
        context = {'notfounds': move_csv.move_to_melon(id, password, list)}
        return render(request, 'music/result.html', context)
    if site == 'flo':
        context = {'notfounds': move_csv.move_to_flo(id, password, list)}
        return render(request, 'music/result.html', context)
    if site == 'bugs':
        context = {'notfounds': move_csv.move_to_bugs(id, password, list)}
        return render(request, 'music/result.html', context)
    if site == 'vibe':
        context = {'notfounds': move_csv.move_to_vibe(id, password, list)}
        return render(request, 'music/result.html', context)
    else:
        return redirect('music:SiteMain')


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(generic.DetailView):
    model = Post


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('music:post_list')


def post_write(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            if request.FILES:
                if 'post_file' in request.FILES.keys():
                    post.post_filename = request.FILES['post_file'].name
                    if post.post_filename.find('csv') < 0:
                        title = post.post_title
                        content = post.post_contents
                        name = post.writer
                        password = post.password
                        table_num = post.table_num
                        form = CreatePostForm(initial={'post_title': title, 'post_contents': content, 'writer': name, 'password': password, 'table_num': table_num, })
                        return render(request, 'music/write_post.html', {'form': form})

            post.save()
            return redirect('music:post_list')
    else:
        form = CreatePostForm()
    return render(request, 'music/write_post.html', {'form': form})


def post_update(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        context = {'post' : post, }
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        #old_password = post.password
        #form_old = CreatePostForm(initial={'password': old_password, })
        #form.password = request.password

        #if form.password != form_old.password:
        #    messages.info(request, 'you are not allowed')
        #    return HttpResponseRedirect(reverse_lazy('music:post_list'))

        if form.is_valid():
            post = form.save(commit=False)
            if request.FILES:
                if 'post_file' in request.FILES.keys():
                    post.post_filename = request.FILES['post_file'].name
                    if post.post_filename.find('csv') < 0:
                        title = post.post_title
                        content = post.post_contents
                        name = post.writer
                        password = post.password
                        table_num = post.table_num
                        form = CreatePostForm(initial={'post_title': title, 'post_contents': content, 'writer': name, 'password': password, 'table_num': table_num, })
                        return render(request, 'music/write_post.html', {'form': form})
            post.post_date = datetime.datetime.now()
            post.save()
            return render(request, 'music/post_detail.html', context=context )
    else:
        title = post.post_title
        content = post.post_contents
        name = post.writer
        password = post.password
        table_num = post.table_num
        form = CreatePostForm(initial={'post_title': title, 'post_contents': content, 'writer': name, 'password': password, 'table_num': table_num, })
    return render(request, 'music/write_post.html', {'form': form})


def comment_write(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
       # password = request.POST.get('password')
        writer = request.POST.get('writer')

        Comment.objects.create(com_post=post, com_writer=writer, com_contents=content)  # com_password=password,
        return HttpResponseRedirect(resolve_url('music:post_detail', pk=post.pk))


def post_download_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    url = 'media/'+post.post_file.decode("utf-8")
    file_url = urllib.parse.unquote(url)
    #print(file_url, 999)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(post.post_filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404


def SiteMain(request):
    return render(request, 'music/SiteMain.html')


def Recmd(request):
    re_genre = request.POST.get('re_genre').upper()
    #print(re_genre)
    get_indb = MdIntegratedM.objects.all()
    recmds=[]
    if re_genre == '알앤비':
        re_genre = 'R&B'
    if re_genre == 'JAZZ':
        re_genre = '재즈'
    if re_genre == 'OST':
        re_kor_m = '국내영화'
        re_fore_m = '해외영화'
        re_kor_d = '국내드라마'
        re_fore_d = '해외드라마'
        for i in range(len(get_indb)):
            if re_kor_m in get_indb[i].in_genre or re_fore_m in get_indb[i].in_genre or re_kor_d in get_indb[i].in_genre or re_fore_d in get_indb[i].in_genre:
                recmds.append(get_indb[i].in_song + ' - ' + get_indb[i].in_artist + ', [' + get_indb[i].in_genre + ']')
        if len(recmds) > 10:
            randomList = random.sample(recmds, 10)
            #for recmd in randomList:
                #print(recmd)
            context = {'recmds': randomList}
            return render(request, 'music/re_result.html', context)
        elif len(recmds) == 0:
            recmds.append('선택한 장르의 곡들이 없습니다.')
            context = {'recmds': recmds}
            return render(request, 'music/re_result.html', context)
        else:
            #for recmd in recmds:
                #print(recmd)
            context = {'recmds': recmds}
            return render(request, 'music/re_result.html', context)
    else:
        for i in range(len(get_indb)):
            if re_genre in get_indb[i].in_genre.upper():
                recmds.append(get_indb[i].in_song + ' - ' + get_indb[i].in_artist + ', [' + get_indb[i].in_genre + ']')
        if len(recmds) > 10:
            randomList = random.sample(recmds, 10)
            #for recmd in randomList:
                #print(recmd)
            context = {'recmds': randomList}
            return render(request, 'music/re_result.html', context)
        elif len(recmds) == 0:
            recmds.append('선택한 장르의 곡들이 없습니다.')
            context = {'recmds': recmds}
            return render(request, 'music/re_result.html', context)
        else:
            #for recmd in recmds:
                #print(recmd)
            context = {'recmds': recmds}
            return render(request, 'music/re_result.html', context)


def user_guide(request):
    return render(request, 'music/user_guide.html')

# Create your views here.
