from django.contrib import admin

from .models import Sentence, Category, Tag



class SentenceAdmin(admin.ModelAdmin):
    fields = ['sentence_text', 'category', 'tag']
    list_display = ('sentence_text', 'category', 'tag_names')
    list_filter = ['updated_date', 'category']
    search_fields = ['sentence_text']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'is_public']
    list_display = ('name', 'description', 'is_public')


class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'is_public']
    list_display = ('name', 'is_public')



admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
