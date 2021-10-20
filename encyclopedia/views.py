from django.shortcuts import render, redirect

from . import util

import markdown2

from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    # Checks if received input from the layout search form
    if title == 'q':
        return search(request, request.POST.get('q'))

    # Checks if requested title is in the entries list
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html",{
            "msg": "The requested page was not found."
        })

    # Convert markdown to html
    html = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "html": html
    })


def search(request, entry):
    # Checks if received input from the search from is in the entries list
    if util.get_entry(entry) != None:
        return redirect("title", title=entry)

    # Creates a list containing the entries and a list that will
    # hold all entries that are similar to the input
    entries = util.list_entries()
    approx_entries = []

    for word in entries:
        if entry.lower() in word.lower():
            approx_entries.append(word)

    return render(request, "encyclopedia/search.html",{
        "entries": approx_entries
    })


def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")

    if request.method == "POST":
        if util.get_entry(request.POST.get("title")) != None:
            return render(request, "encyclopedia/error.html",{
                "msg": "This encyclopedia entry already exists."
            })
        
        print(request.POST.get("title"))
        util.save_entry(request.POST.get("title"), request.POST.get("content"))

        return redirect('title', title=request.POST.get("title"))


def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "content": util.get_entry(request.GET.get("title")),
            "title": request.GET.get("title")
        })

    if request.method == "POST":
        util.save_entry(request.POST.get("title"), request.POST.get("content"))

        return redirect("title", title=request.POST.get("title"))


def random(request):
    entries = util.list_entries()
    random_entry = choice(entries)

    return redirect("title", title=random_entry)
    
    