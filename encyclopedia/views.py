from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown2, markdownify 
import random as rand

from django import forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        , 'page_title':'Encyclopedia'
    })

def goto_entry(request, title):    
    entry_text = util.get_entry(title)
    if entry_text == None:
        return render(request, 'encyclopedia/not-found.html', {'title':title
                                                               ,'page_title':'Not Found'});
    html = markdown2.markdown(entry_text, extras=['fenced-code-blocks'])
    return render(request, 'encyclopedia/entry.html', {'title':title,'content':html, 'page_title':title})

def create_entry(request):    
    if request.method == 'GET':
        return render(request, 'encyclopedia/create.html', {'page_title':'Create'})
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    print("edit: "+ str(bool(request.POST.get('edit'))))
    print("update: "+str(bool(request.POST.get('update'))))

    

    if bool(request.POST.get('edit')):
        return render(request, 'encyclopedia/create.html', {'title':title, 
        'content':markdownify.markdownify(content, heading_style="ATX"), 'update':True, 
        'page_title':f"Edit {title}"})

    if util.get_entry(title) == None or bool(request.POST.get('update')):
        util.save_entry(title, content)
    return HttpResponseRedirect(f'wiki/{title}');


def search(request):
    q = request.POST.get('q')
    e = util.get_entry(q)
    if e != None:
        return goto_entry(request, q)
    list = util.list_entries()
    results = []
    for e in list:
        t = util.get_entry(e)
        if t.find(q) >= 0:
            results.append(e);
    if len(results) == 0:
        return render(request, 'encyclopedia/search-results.html', {
            'error':f"'{q}' is not exists in our entries"
            ,'page_title':'Search results'
        })        
    return render(request, 'encyclopedia/search-results.html', {
        'results':results,
        'page_title':'Search results'
    })


def random_entry(request):
    list = util.list_entries()
    e = list[rand.randrange(0, len(list))]
    return HttpResponseRedirect(f'wiki/{e}')