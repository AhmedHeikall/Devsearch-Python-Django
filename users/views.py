from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Message
from .utils import search_profile, paginate_profiles





# Create your views here.

def login_page(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles-page")


    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
           messages.error(request, "Username does not exist!")

        user = authenticate(request, username=username, password=password)    

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles-page')
        else:
            messages.error(request, "Username OR Password is Not Correct!")   
            
   
    return render(request, "users/login.html")


def logout_page(request):
    logout(request)
    messages.success(request, "User Logout Successfully")
    return redirect("login-page")


def register_page(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            messages.success(request, "User Account Created Sccssesfully")
            return redirect("edit-account-page")
        else:
            messages.success(request, "An Error Occur During The Registeration")    

    context = {"page":page, "form":form}
    return render(request,  "users/login.html", context)


def profiles(request):
    profiles, search_query = search_profile(request)
    profiles, custom_range = paginate_profiles(request, profiles, 6)

    context = {
        "profiles":profiles, 
        "search_query":search_query,
        "custom_range": custom_range,
        }
    return render(request, "users/profiles.html", context)


def profile(request, pk):
    profile= Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(describtion__exact="")
    other_skills = profile.skill_set.filter(describtion="")
    context = {"profile": profile,
                "topskills": top_skills,
                "otherskills": other_skills,
            }
    return render(request, "users/profile.html", context)    


@login_required(login_url="login-page")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = { "profile": profile,
                "skills": skills,
                "projects":projects,
            }
    return render(request, "users/account.html", context)


@login_required(login_url="login-page")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user-account-page")

    context = {"form":form}
    return render(request, "users/profile_form.html", context)    


@login_required(login_url="login-page")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill Added Successfully")
            return redirect("user-account-page")


    context = {"form": form}
    return render(request, "users/skills.html", context)   


@login_required(login_url="login-page")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance= skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance= skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill Updated Successfully")
            return redirect("user-account-page")

    context = {"form": form}
    return render(request, "users/skills.html", context)   


@login_required(login_url="login-page")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill Deleted Successfully")
        return redirect("user-account-page")
    context = {"object": skill,}
    return render(request, "delete_form.html", context)


@login_required(login_url="login-page")
def inbox(request):
    profile = request.user.profile
    messagesReuests = profile.messages.all()
    unreadCount = messagesReuests.filter(is_read=False).count()
    
    context = {"messagesReuests":messagesReuests, "unreadCount":unreadCount,}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login-page")
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()
        
    context = {"message":message}
    return render(request, "users/message.html", context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, " Your Message Sent Successfully")    
            return redirect("profile-page", pk=recipient.id)


    context = {"recipient":recipient, "form": form}
    return render(request, "users/message_form.html", context)    
