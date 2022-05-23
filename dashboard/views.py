from multiprocessing import context
from typing import Generic
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import render
from . forms import *
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.generic.detail import DetailView
#from youtubesearchpython import VideosSearch
#youtube section new solution
import requests
from isodate import parse_duration
from django.conf import settings



def home(request):
    return render(request, 'dashboard/home.html')


# Notes

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            descrip = form.cleaned_data['description']
            notes = Notes(
                user=request.user, title=title, description=descrip)
            notes.save()
            messages.success(
                request, f"Notes Added from {request.user.username} Successfully")
            #return HttpResponseRedirect(reverse('thanks'))
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)



def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model= Notes 



# HomeWork

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST) 
        if form.is_valid():
            sub = form.cleaned_data['title']
            title = form.cleaned_data['title']
            descrip = form.cleaned_data['description']
            due = form.cleaned_data['due']
            done = form.cleaned_data['is_finished']
            try:
                finished = done
                if finished == 'on': 
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = sub,
                title = title,
                description = descrip,
                due = due,
                is_finished = finished

            )
            homeworks.save()
            messages.success(request,f'Homework Added from {request.user.username}!!')
    else: 
      form = HomeworkForm() 

    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
               'homeworks':homework,
               'homeworks_done':homework_done,
               'form':form,
               }
    return render(request,'dashboard/homework.html',context)





def update_homework(resuest, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework') 


def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")



# youtube function new solution 

def youtube(request):
          videos = [] 
          if request.method == 'POST':
             search_url = 'https://www.googleapis.com/youtube/v3/search'
             video_url = 'https://www.googleapis.com/youtube/v3/videos'

             search_params = {
              'part' : 'snippet',
              'q' : request.POST['search'],
              'key' : settings.YOUTUBE_DATA_API_KEY,
              'maxResults' : 9,
              'type' : 'video'
             }
            
             r = requests.get(search_url, params=search_params) 

             results = r.json()['items']

             video_ids = []
             for result in results:
              video_ids.append(result['id']['videoId'])
            
             if request.POST['submit'] == 'lucky':
                return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')


             video_params = {
              'key' : settings.YOUTUBE_DATA_API_KEY,
              'part' : 'snippet,contentDetails',
              'id' : ','.join(video_ids),
              'maxResults' : 9
            }

             r = requests.get(video_url, params=video_params)

             results = r.json()['items']
            
            
             for result in results:
              video_data = {
                  'title' : result['snippet']['title'],
                  'id' : result['id'],
                  'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                  'duration' : (parse_duration(result['contentDetails']['duration'])),
                  'thumbnail' : result['snippet']['thumbnails']['high']['url']
              }

              videos.append(video_data) 
            
             print(videos) 
           

          context = {

            'videos': videos 
          }

          return render(request, 'dashboard/youtube.html', context) 

           
# To DO

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                 finished = True 
                else: 
                    finished = False
            except:
                finished = False 
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"la tâche a été ajoutée avec succès depuis {request.user.username}!! ")
    else:        
     form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0 :
        todos_done = True
    else:
        todos_done = False

    context = {

        'form' : form,
        'todos':todo,
        'todos_done': todos_done
    }
    return render(request,"dashboard/todo.html", context)
      

def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.isfinshed = True
    todo.save()
    return redirect('todo')


def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


# Books

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url) 
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)

        context={
            'form':form,
            'results':result_list
        }
        return render(request,"dashboard/books.html", context)
    
    else:
     form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,"dashboard/books.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid(): 
            form.save() 
            username = form.cleaned_data.get('username')
            messages.success(request,f"Compte créé pour {username}")
            return redirect("login") 

    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,"dashboard/register.html",context) 


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)

    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    
    context = {
        'homeworks' : homeworks,
        'homework_done' : homework_done
    }

    return render(request, "dashboard/profile.html", context) 