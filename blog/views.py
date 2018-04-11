from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, ContatoForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.visitas+=1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def contato(request):
    if request.method == 'GET':
        email_form = ContatoForm()
    else:
        email_form = ContatoForm(request.POST)
        if email_form.is_valid():
            emissor = email_form.cleaned_data['emissor']
            assunto = email_form.cleaned_data['assunto']
            msg = email_form.cleaned_data['msg']

            try:
                send_mail(assunto, msg, emissor, ['maikonsx@gmail.com'])
            except BadHeaderError:
                return HttpResponse("Erro =/")
            return redirect('obg')
    return render(request, 'blog/email.html', {'form': email_form})

def obg(request):
    return HttpResponse("<h2>Obrigado pela mensagem!!!</h2>")

