from django.shortcuts import render,redirect
from random import randint

from . import util
from markdown2 import Markdown
from django import forms

class SearchForm(forms.Form):
     title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )

class NewEntryForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":SearchForm()
    })

def entry(request,TITLE):
    if TITLE not in util.list_entries():
        return render(request,"encyclopedia/error.html")

    entry = util.get_entry(TITLE)
    return render(request,"encyclopedia/entry.html",{"entry":Markdown().convert(entry)

                                                       ,"title":TITLE})

def search(request):
    matches=[]
    lists=util.list_entries()
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]


            for i in lists:
                if  title in i and len(title)==len(i):
                    entry = util.get_entry(title)
                    return render(request,"encyclopedia/entry.html",{"entry":Markdown().convert(entry)

                                                                       ,"title":title})

                if title in i and len(title)!=len(i):
                    matches.append(i)
            return render(request,"encyclopedia/search.html",{"matches":matches})
            if title not in lists:
                return render(
            request,
            "encyclopedia/error.html",
            )
def editPage(request,title):
    mdcontents = util.get_entry(title)
    markdowner = Markdown()
    htmlcontents = markdowner.convert(mdcontents)


    return render(request, "encyclopedia/edit.html",{
        "title" : title,
        "mdcontent" : mdcontents
    })

def save_entry(request):
    title = request.POST['title']
    textarea = request.POST['textarea']
    f = open(f'C:/Users/HP/Desktop/wiki/entries/{title}.md','w+')

    f.write(textarea)
    f.close()
    markdowner = Markdown()
    htmlcontents = markdowner.convert(textarea)

    return render(request, "encyclopedia/get_entry.html",{
        "title" : title,
        "ent" : htmlcontents
    })

def new(request):
    if request.method == "GET":
        return render(
            request, "encyclopedia/new_page.html", {"form2": NewEntryForm()}
        )
    lists=util.list_entries()
    if request.method=='POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title  in  lists:
                return render(request,"encyclopedia/page_already_exist.html")
            if title not in lists:
                util.save_entry(title,content)
                entry = util.get_entry(title)
                return render(request,"encyclopedia/entry.html",{"entry":Markdown().convert(entry)

                                                   ,"title":title})
def random_entry(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]

    mdcontent = util.get_entry(title)
    content = Markdown().convert(mdcontent)
    return render(request,"encyclopedia/entry.html",{"entry":content

                                                       ,"title":title})
