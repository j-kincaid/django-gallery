from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Artwork, Tag
from .forms import ArtworkForm, ReviewForm


# This is the path  http://127.0.0.1:8000/artworks/
def artworks(request):
    artworks = Artwork.objects.all()
    context = {"artworks": artworks}
    return render(request, "artworks/artworks.html", context)


# http://127.0.0.1:8000/artwork/1/
def artwork(request, pk):
    artworkObj = Artwork.objects.get(id=pk)
    tags = artworkObj.tags.all()
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.artwork = artworkObj
        review.owner = request.user.profile
        review.save()

        # The @property decorator in models.py allows you to run the calculation without it being a method().

        artworkObj.getVoteCount

        messages.success(request, "Your review was successfully submitted!")
        return redirect("artwork", pk=artworkObj.id)

    return render(
        request, "artworks/single-artwork.html", {"artwork": artworkObj, "form": form}
    )


@login_required(login_url="login")
def createArtwork(request):
    profile = request.user.profile
    form = ArtworkForm()

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.owner = profile
            artwork.save()
            return redirect("artworks")

    context = {"form": form}
    return render(request, "artworks/artwork_form.html", context)


@login_required(login_url="login")
def updateArtwork(request, pk):
    profile = request.user.profile
    artwork = profile.artwork_set.get(id=pk)
    form = ArtworkForm(instance=artwork)

    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            artwork = form.save()
            return redirect("artworks")

    context = {"form": form, "artwork": artwork}
    return render(request, "artworks/artwork_form.html", context)


@login_required(login_url="login")
def deleteArtwork(request, pk):
    profile = request.user.profile
    artwork = profile.artwork_set.get(id=pk)
    if request.method == "POST":
        artwork.delete()
        return redirect("artworks")
    context = {"object": artwork}
    return render(request, "artworks/delete_template.html", context)


def results(request):
    artworks = Artwork.objects.all()
    context = {"artworks": artworks}
    return render(request, "artworks/results.html", context)
