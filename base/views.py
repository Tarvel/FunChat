from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User, Message
from .forms import RoomForm
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
            user = User.objects.get(username=username)
        except:    
            messages.error(request, "Username does not exist.")

        user = authenticate(request, username=username, password=password)
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
            messages.error(request, 'An error occured during registration')
    
    context = {'page':page, 'title':'Register', 'form':form}
    return render (request, 'base/register_login_form.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q)|
                                Q(description__icontains=q)) 
    topics = Topic.objects.all()
    room_count = rooms.count()
    recent_messages = Message.objects.order_by('-created')
    context = {'title':'FunChat', 'rooms':rooms, 'topics':topics, 'room_count':room_count, 'recent_messages':recent_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
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
        
    
    context = {'title':'Room', 'room':room, 'room_messages':room_messages, 'participants':participants}
    
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':RoomForm, 'title':'Create Room'}
    return render (request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        user = True
        return HttpResponse('You didnt make this post')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room', room.id)

    context={'form':form, 'title':'Update Room'}
    return render(request, 'base/room_form.html', context)

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
def editMessage(request, pk):
    message = Message.objects.get(id=pk)
