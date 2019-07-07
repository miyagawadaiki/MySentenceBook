#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models
from django.db.models import Q
from django.forms import ModelForm, SelectMultiple, CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import Category, Tag, Sentence


class SentenceSearchForm(ModelForm):
    """
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
    """

    def __init__(self, user, *args, **kwargs):
        super(SentenceSearchForm, self).__init__(*args, **kwargs)
        self.fields['sentence_text'] = forms.CharField(
            label='Words',
            max_length=30,
            required=False,
        )
        self.fields['category'] = forms.ModelChoiceField(
            label='Tags',
            required=False,
            queryset=Category.objects.filter(
                Q(author=user) |
                Q(is_public=True)
            ),
        )
        self.fields['tag'] = forms.ModelMultipleChoiceField(
            label='Tags',
            required=False,
            queryset=Tag.objects.filter(
                Q(author=user) |
                Q(is_public=True)
            ),
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
