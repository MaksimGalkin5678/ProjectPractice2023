from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm
from .models import Snippet


#Отвечает за поиск по номеру
def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

#Для открытия странички создания сниппета
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета', 'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pages/view_snippets.html")
        return render(request, 'pages/add_snippet.html', {'form': form})

#для просмотра всех сниппетов
def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов'}
    return render(request, 'pages/view_snippets.html', context)

#Для создания сниппета на страничеке создания
# def create_snippet(request):
#    if request.method == "POST":
#        form = SnippetForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('view_snippets') #вписать URl на созданную страницу сниппета
#        return render(request,'pages/add_snippet.html',{'form': form})

#для просмотра отдельного сниппета
def view_snipp(request):
    return render (request, 'snippets/1.html', )


#для просмотра отдельного сниппета
# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
#     return render(request, 'blog/post/detail.html', {'post': post})


