from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            messages.add_message(request, messages.INFO, 'your snippet add!')
        return render(request, "pages/add_snippet.html", {'form': form})


def snippets_page(request):

    snippets = Snippet.objects.all().filter(public=1)
    count= snippets.count
    pagename = 'Просмотр сниппетов'
    users = User.objects.all().annotate(num_snippets=Count('snippet')).filter(num_snippets__gte=1)

    username = request.GET.get('username')
    if username:
        filter_user = User.objects.get(username=username)
        snippets = snippets.filter(user=filter_user)
        count= snippets.count

    lang = request.GET.get("lang")
    if lang is not None:
        snippets = snippets.filter(lang=lang)
        count= snippets.count

    sort = request.GET.get("sort")
    if sort == 'name':
        snippets = snippets.order_by("name")
        sort = '-name'
        count= snippets.count
    elif sort == '-name' or sort == 'init':
        snippets = snippets.order_by("-name")
        sort = "name"
        count= snippets.count
    if sort is None:
        sort = "init"

    context = {
        'pagename': pagename,
        'snippets': snippets,
        'lang': lang,
        'sort': sort,
        'users': users,
        'count': count
    }
    return render(request, 'pages/view_snippets.html', context)

def my_snippet(request):

    snippets = Snippet.objects.all().filter(user=request.user)
    snippets = snippets.filter(hide = True)
    count= snippets.count
    pagename = 'Мои сниппеты'
    users = User.objects.all().annotate(num_snippets=Count('snippet')).filter(num_snippets__gte=1)

    username = request.GET.get('username')
    if username:
        filter_user = User.objects.get(username=username)
        snippets = snippets.filter(user=filter_user)
        count= snippets.count

    lang = request.GET.get("lang")
    if lang is not None:
        snippets = snippets.filter(lang=lang)
        count= snippets.count

    sort = request.GET.get("sort")
    if sort == 'name':
        snippets = snippets.order_by("name")
        sort = '-name'
        count= snippets.count
    elif sort == '-name' or sort == 'init':
        snippets = snippets.order_by("-name")
        sort = "name"
        count= snippets.count
    if sort == 'user_id':
        snippets = snippets.order_by("user_id")
        sort = '-user_id'
        count= snippets.count
    elif sort == '-user_id':
        snippets = snippets.order_by("-user_id")
        sort = "user_id"
        count= snippets.count
    if sort is None:
        sort = "init"

    context = {
        'pagename': pagename,
        'snippets': snippets,
        'lang': lang,
        'sort': sort,
        'users': users,
        'count': count
    }
    return render(request, 'pages/mysnippet.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    comment_form = CommentForm()
    comments = snippet.comments
    context = {
        'snippet': snippet,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'pages/snippet_detail.html', context)


@login_required
def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    if snippet.user != request.user:
        raise PermissionDenied()
    snippet.delete()
    return redirect("mysnippet")


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("username =", username)
        # print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            messages.add_message(request, messages.INFO, 'your success login!')
            pass
    return redirect('home')


def logout_page(request):
    auth.logout(request)
    return redirect('home')


def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # print(formm)
            messages.add_message(request, messages.INFO, 'your success registration!')
            return redirect('home')
        else:
            context = {
                'form': form
            }
            messages.add_message(request, messages.INFO, 'try again!')
            return render(request, 'pages/registration.html', context)



def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST["snippet_id"]
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
            messages.add_message(request, messages.INFO, 'your success add comment!!!')
            return redirect("snippet-detail", snippet_id)

    raise Http404

def reset_filters(request):
    if request.method == "RESET":
        return render(request, 'pages/registration.html')
    
def snippet_edit (request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    context = {
        'snippet': snippet,
        'name': snippet.name,
        'code': snippet.code,
        'creation_date':snippet.creation_date,
        'lang': snippet.lang,
        'user_id': snippet.user,
        'public': snippet.public
    }
    if request.method == "POST":
        snippet.name=request.POST['name_snippet']
        snippet.code=request.POST['code_snippet']
        snippet.save()
        messages.add_message(request, messages.INFO, 'your save your snippet!')
        return redirect("snippet-detail", snippet_id)
    
    return render(request, 'pages/snippet_detail_edit.html', context)

@login_required
def snippet_hide(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.hide = False
    print(snippet.hide)
    snippet.save(snippet.hide)
    messages.add_message(request, messages.INFO, 'snippet success hide!!!')
    return redirect("mysnippet")

def snippet_show(request):
    snippet=Snippet.objects.all()
    for snip in snippet:
        snip.hide="True"
        snip.save(update_fields=["hide"])
    messages.add_message(request, messages.INFO, 'snippets are showed!!!')
    return redirect("mysnippet")

def snippet_search(request):
    snippet_id = int(request.GET["snippet_id"])
    if Snippet.objects.filter(id=snippet_id).exists():
        snippet = Snippet.objects.get(id=snippet_id)
        snippet_id = snippet
        comment_form = CommentForm()
        comments = snippet.comments
        context = {
            'snippet': snippet,
            'comment_form': comment_form,
            'comments': comments,
        }
        messages.add_message(request, messages.INFO, 'search is success')
        return render(request, 'pages/snippet_detail.html', context)
    else: 
        messages.add_message(request, messages.INFO, 'Такого сниппета нет')
        return render (request, 'pages/index.html')

