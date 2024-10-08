from django.shortcuts import render, HttpResponseRedirect
from .forms import SigUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post

# Create your views here.

# Home view
def home(request):
  posts = Post.objects.all()
  return render(request, 'blog/home.html', {'posts':posts})

# About view
def about(request):
  return render(request, 'blog/about.html')

# Contact view
def contact(request):
  return render(request, 'blog/contact.html')

# Dashboard view
def dashboard(request):
  if request.user.is_authenticated:
    posts = Post.objects.all()
    return render(request, 'blog/dashboard.html', {'posts':posts})
  else:
     return HttpResponseRedirect('/login')
# Signup view
def user_signup(request):
  if request.method=='POST':
    form = SigUpForm(request.POST)
    if form.is_valid():
      messages.success(request, 'Congratulations!! You have become an Author :)')
      form.save()
  else:
    form = SigUpForm()
  return render(request, 'blog/signup.html', {'form':form})

# Login view
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully! ')
                    return HttpResponseRedirect('/dashboard')
        else:
          form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard')

# logout view
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

# Add new post
def add_post(request):
   if request.user.is_authenticated:
    if request.method == 'POST':
      form = PostForm(request.POST)
      if form.is_valid():
         title = form.cleaned_data['title']
         desc = form.cleaned_data['desc']
         pst = Post(title=title, desc=desc)
         pst.save()
         form = PostForm()
    else:
      form = PostForm()
      return render(request, 'blog/addpost.html', {'form':form})
   else:
      return HttpResponseRedirect('/login')
   
# Update new post
def update_post(request, id):
   if request.user.is_authenticated:
    return render(request, 'blog/updatepost.html')
   else:
      return HttpResponseRedirect('/login')
   
# Delete post
def delete_post(request, id):
   if request.user.is_authenticated:
    return HttpResponseRedirect('/dashboard')
   else:
      return HttpResponseRedirect('/login')
