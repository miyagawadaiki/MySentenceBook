#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models
from django.forms import ModelForm, SelectMultiple, CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import Category, Tag, Sentence


class SentenceSearchForm(ModelForm):
    sentence_text = forms.CharField(
        label='Words',
        max_length=50,
        required=False,
    )
    tag = forms.ModelMultipleChoiceField(
        label='Tags',
        required=False,
        queryset=Tag.objects,
        #widget=SelectMultiple(attrs={'id="multiSelect"'})
    )

    class Meta:
        model = Sentence
        fields = ['sentence_text', 'category', 'tag']
        """
        labels = {
            'sentence_text': _('Words'),
        }
        widgets = {
            'tag': SelectMultiple(),#attrs={'style': 'color: black; background-color: white; min-width: 80px;'}),
        }
        """

"""
class SearchForm(forms.Form):
    #cate_choices = []
    #for cate in Catetory.objects.filter
    title = forms.CharField(
        initial='',
        label='word',
        required = False, # 必須ではない
    )
    category = forms.ChoiceField(   # forms.TypedChoiceField(
        label=
    )
    tags = forms.Multiple
"""
