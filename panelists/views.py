from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, MessageForm
from .models import Profile, Message


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "panelists/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # # Makes sure the username is lowercase so it's not case-sensitive
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect("edit-account")

        else:
            messages.error(request, "An error has occurred during registration.")

    context = {"page": page, "form": form}
    return render(request, "panelists/login_register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "panelists/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {"profile": profile}
    return render(request, "panelists/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile

    artworks = profile.artwork_set.all()

    context = {"profile": profile, "artworks": artworks}
    return render(request, "panelists/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "panelists/profile_form.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "panelists/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "panelists/message.html", context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message has been submitted.")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "panelists/message_form.html", context)
