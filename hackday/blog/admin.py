from hackday.blog.models import Entry, Category, Tag
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'create_date', 'pub_date')

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category)
admin.site.register(Tag)
