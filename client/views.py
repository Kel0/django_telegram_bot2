from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, "blog/about.html", {"title": "About"})
