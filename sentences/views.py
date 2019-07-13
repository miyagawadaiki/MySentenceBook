from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Category, Sentence, Tag
from .form import SentenceForm, SentenceSearchForm


##############################################
# main views
##############################################

class IndexView(generic.ListView):
    template_name = 'sentences/index.html'
    paginate_by = 5
    context_object_name = 'sentence_list'

    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('sentence_text', None),
            self.request.POST.get('category', None),
            self.request.POST.getlist('tag', None), # get as list
        ]
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        sentence_text = ''
        category = None
        tag = None
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            sentence_text = form_value[0]
            category = form_value[1]
            tag = form_value[2]
        default_data = {'sentence_text': sentence_text,   # 検索ワード
                        'category': category,   # カテゴリー
                        'tag': tag,   # タグ
                        }
        test_form = SentenceSearchForm(self.request.user, initial=default_data) # 検索フォーム
        # test_form = SentenceSearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        return context

    def get_queryset(self):
        #return Sentence.objects.filter(author=self.request.user).order_by('-updated_date')[:50]
        #return Sentence.objects.all().order_by('-updated_date')

        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            sentence_text = form_value[0]
            category = form_value[1]
            print(category)
            tag = form_value[2]
            print(tag)

            # 検索条件
            condition_author = Q(author=self.request.user)
            condition_text = Q()
            condition_cate = Q()
            condition_tags = Q()
            if len(sentence_text) != 0 and sentence_text[0]:
                condition_text = Q(sentence_text__contains=sentence_text)
            else:
                condition_text = Q(sentence_text__contains=' ')
            if category != None and category != '':
                condition_cate = Q(category__pk=category)
                
            q = Sentence.objects.select_related().filter(
                        condition_author &
                        condition_text & 
                        condition_cate 
            )
            if len(tag) != 0:# and tag[0] != 'All':
                for tid in tag:
                    if tid != 'None':
                        q = q.filter(tag__pk=int(tid))
                    else:
                        q = q.filter(tag=None)
            return q.order_by('-updated_date')
        else:
            return Sentence.objects.filter(author=self.request.user).order_by('-updated_date')[:50]


class DetailView(generic.DetailView):
    model = Sentence
    template_name = 'sentences/detail.html'
    context_object_name = 'sentence'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tagname_list'] = [tag.name for tag in self.get_object.tag.all()]
        context['tagnames'] = self.object.tag_names()
        if context['tagnames'] == '':
            context['tagnames'] = 'None'
        return context

    """
    def get_queryset(self):
        Excludes any questions that aren't published yet. 
        return Sentence.objects.filter(created_date__lte=timezone.now())
    """


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Sentence
    template_name = 'sentences/form.html'
    fields = ['sentence_text', 'comment_text', 'category', 'tag']  # '__all__'
    #context_object_name = 'sentence'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sentence_text = ''
        comment_text = 'No commenet.'
        category = None
        tag = None
        default_data = {'sentence_text': sentence_text,   # 検索ワード
                        'comment_text': comment_text,     # コメント
                        'category': category,   # カテゴリー
                        'tag': tag,   # タグ
                        }
        test_form = SentenceForm(self.request.user, initial=default_data)
        context['form'] = test_form
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        print(form.instance)
        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error")
        #print(form.instance)
        print("category:", form.instance.category)
        print("tag:", form.instance.tag)
        return super(CreateView, self).form_valid(form)


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Sentence
    template_name = 'sentences/form.html'
    fields = ['sentence_text', 'comment_text', 'category', 'tag']  # '__all__'
    #context_object_name = 'sentence'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sentence_text = self.get_object().sentence_text
        comment_text = self.get_object().comment_text
        category = self.get_object().category
        #print(self.object.tag)
        tag = [self.get_object().tag]
        default_data = {'sentence_text': sentence_text,   # 検索ワード
                        'comment_text': comment_text,     # コメント
                        'category': category,   # カテゴリー
                        'tag': tag,   # タグ
                        }
        test_form = SentenceForm(self.request.user, initial=default_data)
        context['form'] = test_form
        return context

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super(UpdateView, self).dispatch(request, *args, **kwargs)


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Sentence
    success_url = reverse_lazy('sentences:index')
    template_name = 'sentences/confirm_delete.html'
    context_object_name = 'sentence'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')

        return super(DeleteView, self).dispatch(request, *args, **kwargs)



##############################################
# category views
##############################################

class CategoryIndexView(generic.ListView):
    template_name = 'categories/index.html'
    paginate_by = 5
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.filter(
            Q(is_public=True) |
            Q(author=self.request.user)
        ).distinct().order_by('-created_date')[:50]
        #return Category.objects.all().order_by('-created_date')


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'categories/detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Category
    template_name = 'categories/form.html'
    fields = ['name', 'description']  # '__all__'
    #context_object_name = 'sentence'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Category
    template_name = 'categories/form.html'
    fields = ['name', 'description']  # '__all__'
    #context_object_name = 'sentence'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user and not(obj.is_public):
            raise PermissionDenied('You do not have permission to edit.')

        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Category
    success_url = reverse_lazy('sentences:cate_index')
    template_name = 'categories/confirm_delete.html'
    context_object_name = 'category'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user and not(obj.is_public):
            raise PermissionDenied('You do not have permission to delete.')

        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)



##############################################
# category views
##############################################

class TagIndexView(generic.ListView):
    template_name = 'tags/index.html'
    paginate_by = 5
    context_object_name = 'tag_list'

    def get_queryset(self):
        return Tag.objects.filter(author=self.request.user).order_by('-used_date')[:50]
        #return Category.objects.all().order_by('-created_date')


class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'tags/detail.html'
    context_object_name = 'tag'


class TagCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Tag
    template_name = 'tags/form.html'
    fields = ['name']  # '__all__'
    #context_object_name = 'sentence'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        return super(TagCreateView, self).form_valid(form)


class TagUpdateView(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Tag
    template_name = 'tags/form.html'
    fields = ['name']  # '__all__'
    #context_object_name = 'sentence'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super(TagUpdateView, self).dispatch(request, *args, **kwargs)


class TagDeleteView(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Tag
    success_url = reverse_lazy('sentences:tag_index')
    template_name = 'tags/confirm_delete.html'
    context_object_name = 'tag'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')

        return super(TagDeleteView, self).dispatch(request, *args, **kwargs)
