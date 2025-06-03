from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User, Message, Profile
from .forms import RoomForm, UserForm, ProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username.lower())
        except:    
            messages.error(request, "Username does not exist.")

        user = authenticate(request, username=username.lower(), password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')
    context = {'page':page,'title':'Login'}
    return render(request, 'base/register_login_form.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
                print(form)
                messages.error(request, 'An error occured during registration')
             
    context = {'page':page, 'title':'Register', 'form':form}
    return render (request, 'base/register_login_form.html', context)


@login_required(login_url='login')
def completeProfile(request):
    page = 'complete'
    user = request.user
    profile, created = Profile.objects.get_or_create(user=request.user)

    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('home')

    context = {'title':"Complete your profile", 'profile_form':profile_form, 'user_form':user_form, 'page':page }
    return render (request,'base/update_profile.html', context)
    


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q)|
                                Q(description__icontains=q)) 
    topics = Topic.objects.all()[0:5]
    if request.user.is_authenticated:
        profile_logged_in = Profile.objects.filter(user=request.user).first()
    else:
        profile_logged_in=False
    
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    context = {'title':'FunChat', 'rooms':rooms, 
               'topics':topics, 'room_count':room_count, 
               'room_messages':room_messages, 
               'profile_logged_in':profile_logged_in,
               }
    return render(request, 'base/home.html', context)


def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return render(request, 'base/error.html')
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    if request.user.is_authenticated:
        profile_logged_in = Profile.objects.filter(user=request.user).first()
    else:
        profile_logged_in=False
        
    
    context = {'title':room.name, 'room':room, 'room_messages':room_messages, 'participants':participants, 'profile_logged_in':profile_logged_in}
    return render(request, 'base/room.html', context)


def userProfile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return render(request, 'base/error.html')
    
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    profile = Profile.objects.filter(user=user).first()
    room_messages = user.message_set.all()[0:5]
    if request.user.is_authenticated:
        profile_logged_in = Profile.objects.filter(user=request.user).first()
    else:
        profile_logged_in=False

    context = {'user':user, 'title':f'{user.username}\'s profile', 
               'rooms':rooms, 'topics':topics, 
               'room_messages':room_messages,
               'profile':profile,
               'profile_logged_in':profile_logged_in
               }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    page = 'create'
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
       
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        
        room = Room.objects.create(

            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
        room.participants.add(request.user)
 
        return redirect('home')

    context = {'form':RoomForm, 'title':'Create Room', 'topics':topics,'page':page}
    return render (request, 'base/create_room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    page = 'update'
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        user = True
        return HttpResponse('You didnt make this post')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name.title())
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', room.id)

    context={'form':form, 'title':'Update Room', 'topics':topics, 'page':page, 'room':room}
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room =Room.objects.get(id=pk)

    if request.method=='POST':
        room.delete()
        return redirect('home')

    context = {'title':'Delete Room', 'obj':room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
   
    if request.method=='POST':
        message.delete()
        return redirect('room', message.room.id )

    context = {'title':'Delete Message', 'obj':message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    page = 'update'

    user = request.user
    profile = user.profile

    if profile == 'None':
        profile = Profile.objects.create(user=user)

    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()


    context = {'title':'Edit Profile', 'page':page, 'profile_form':profile_form, 'user_form':user_form,}
    return render (request, 'base/update_profile.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    context = {'title':'Topics', 'topics':topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()[0:3]

    context = {'title':'Recevt Activities', 'room_messages':room_messages}
    return render(request, 'base/activity.html', context)