from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'search', 'placeholder':'Search Encyclopedia'}))

class TitleForm(forms.Form):
    title = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'placeholder':'Title of New Page'}))

class ContentForm(forms.Form):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={
                                                                    'placeholder':'Content of New Page',
                                                                    'style': 'height: 40em;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, title):
    entries = util.list_entries()

    if title in entries:
        view = f"entries/{title}.html"
        return render(request, view, {
            "title": title,
            "content": util.get_entry(title),
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/invalid_entry.html", {
            "title": title,
            "form": SearchForm()
        })
    
def search(request):
    form = SearchForm(request.GET)
    entries = util.list_entries()

    if form.is_valid():
        search = form.cleaned_data["search"]

        if search in entries:
            return HttpResponseRedirect(reverse("entry", kwargs={"title":search}))

        else:
            header = "No Results Found"
            returned = []
            for entry in entries:
                if search.lower() in entry.lower():
                    returned.append(entry)
            if len(returned) > 0:
                header = "Search Results"
            return render(request, "encyclopedia/search_results.html", {
                "entries": returned,
                "header": header,
                "form": SearchForm()
            })

def create(request):
    return render(request, "encyclopedia/create_page.html", {
        "form": SearchForm(),
        "title_form": TitleForm(),
        "content_form": ContentForm()
    })

def submit_creation(request):
    title_form = TitleForm(request.POST)
    content_form = ContentForm(request.POST)

    if title_form.is_valid() and content_form.is_valid():
        title = title_form.cleaned_data["title"]
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/duplicate.html", {
                        "form": SearchForm(),
                        "title": title})
        else:
            util.save_entry(title, content_form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("entry", kwargs={"title":title}))