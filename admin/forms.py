from django import forms

from staring.models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ["last_update", "create_date"]
