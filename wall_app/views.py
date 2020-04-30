from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from .models import Post
from .models import Comment
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.login_validator(request.POST)
    print(request.POST)
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)

        request.session['userid'] = user.id
        return redirect('/wall')
            
    return redirect('/')
    
def login(request):
        user = User.objects.filter(email = request.POST['email'])
        print(user)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/wall')
            else:
                messages.error(request, "Email/password is incorrect.")
        else:
            messages.error(request, "Email isnt registered yet.")
        return redirect('/')


def wall(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            "user" : User.objects.get(id = request.session['userid']),
            "allposts" : Post.objects.all().order_by('post')
        }
    
        return render(request, 'wall.html', context)

def make_post(request):
    Post.objects.create(post = request.POST['post'], user = User.objects.get(id = request.session['userid']))
    return redirect('/wall')
    
def delete_post(request, post):
    c = Post.objects.get(id=post)
    c.delete()

    #return HttpResponse('not the user')
    return redirect ('/wall')

def make_comment(request, post):

    Comment.objects.create(comment = request.POST['comment'],posting = Post.objects.get(id = post),users_comments = User.objects.get(id = request.session['userid'])) 

    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')
