from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown
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
    return render(request, 'encyclopedia/entry.html', {'entry_text':html})

def create_entry(request):
    return render(request, 'encyclopedia/create.html')