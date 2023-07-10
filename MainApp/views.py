from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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

def snippets_page(request):
    context = {'pagename': 'Просмотр сниппетов'}
    return render(request, 'pages/view_snippets.html', context)

def create_snippet(request):
   if request.method == "POST":
       form = SnippetForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect("redirect_url")
       return render(request,'pages/add_snippet.html',{'form': form})

