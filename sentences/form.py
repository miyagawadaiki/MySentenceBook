#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models
from django.db.models import Q
from django.forms import ModelForm, SelectMultiple, CheckboxSelectMultiple
#from django.utils.translation import gettext_lazy as _
from .models import Category, Tag, Sentence


class SentenceForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(SentenceForm, self).__init__(*args, **kwargs)
        self.fields['sentence_text'] = forms.CharField(
            label='Sentence',
            max_length=300,
            required=True,
        )
        self.fields['comment_text'] = forms.CharField(
            label='Comments',
            max_length=200,
            required=False,
        )
        self.fields['category'] = forms.ModelChoiceField(
            label='Category',
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
            #initial=tag_initial,
        )
        #self.fields['tag'].choices = \
        #    [(None, 'None')] + list(self.fields['tag'].choices)

        self.fields['sentence_text'].widget.attrs["class"] = "input"
        self.fields['comment_text'].widget.attrs["class"] = "input"


    class Meta:
        model = Sentence
        fields = ['sentence_text', 'comment_text', 'category', 'tag']



class SentenceSearchForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(SentenceSearchForm, self).__init__(*args, **kwargs)
        self.fields['sentence_text'] = forms.CharField(
            label='Words',
            max_length=30,
            required=False,
        )
        self.fields['category'] = forms.ModelChoiceField(
            label='Category',
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
        self.fields['tag'].choices = \
             list(self.fields['tag'].choices) + [('None', 'None')]

        self.fields['sentence_text'].widget.attrs["class"] = "input"

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
