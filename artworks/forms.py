from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Artwork, Review


class ArtworkForm(ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "title",
            "featured_image",
            "description",
            "topic",
            "demo_link",
            "source_link",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "comments"]

        labels = {
            "value": "Place your vote",
            "comments": "What works, needs work, what might work",
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
