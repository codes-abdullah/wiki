from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown, markdownify 


from django import forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def goto_entry(request, title):    
    entry_text = util.get_entry(title)
    if entry_text == None:
        return render(request, 'encyclopedia/not-found.html', {'entry':title});
    html = markdown.markdown(entry_text, extras=['fenced-code-blocks'])
    return render(request, 'encyclopedia/entry.html', {'title':title,'content':html})

def create_entry(request):    
    if request.method == 'GET':
        return render(request, 'encyclopedia/create.html')
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    if request.POST.get('edit') != None:
        return render(request, 'encyclopedia/create.html', {'title':title, 
        'content':markdownify.markdownify(content), 'edit':True})
    result = {'title':title, 
        'content':content, 
        'error':f'{title} already exists'}
    if util.get_entry(title) == None:
        util.save_entry(title, content)
        result = {'title':'', 
        'content':'', 
        'status':f'{title} created successfully'}
    return render(request, 'encyclopedia/create.html', result)