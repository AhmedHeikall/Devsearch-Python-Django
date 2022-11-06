from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.views import profile
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_project, paginate_projects





# Create your views here.

def projects(request):
    projects, search_query = search_project(request)
    projects, custom_range = paginate_projects(request, projects, 6)
 
    context = {
        "projects": projects, 
        "search_query": search_query,
        "custom_range": custom_range,
        }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    single_project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = single_project
            review.owner = request.user.profile
            review.save()

            """update project vote count"""

            single_project.get_vote_count


            messages.success(request, "Your review submitted succsessfully")
            return redirect("single-project-page", pk=single_project.id)

    context = {"single_project":single_project, "form": form , }
    return render(request, "projects/single_project.html", context)


@login_required(login_url="login-page")
def create_project(request): 
    profile = request.user.profile
    form = ProjectForm()

    if request.method =="POST":
        newtags = request.POST.get("newtags").replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
           project = form.save(commit=False)
           project.owner = profile
           project.save()

           for tag in newtags:
               tag, created = Tag.objects.get_or_create(name=tag)
               project.tags.add(tag)     
           messages.success(request, "Project created Succssefully")  
           return redirect("user-account-page")
    context = {"form":form,}
    return render(request, "projects/project_form.html", context)    


@login_required(login_url="login-page")
def ubdate_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method =="POST":
        newtags = request.POST.get("newtags").replace(',', " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, "Submit Succssefully")
            return redirect("user-account-page")
    context = {"form":form,}
    return render(request, "projects/project_form.html", context)    


@login_required(login_url="login-page")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project Delete Succssefully")
        return redirect("user-account-page")
    context = {"object": project}
    return render(request, "delete_form.html", context)
