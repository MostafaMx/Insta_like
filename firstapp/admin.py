from django.contrib import admin
from .models import Person, Blog, Reaction

class BlogInline(admin.TabularInline):  # or admin.StackedInline for a different style
    model = Blog
    extra = 0

class PersonAdmin(admin.ModelAdmin):
    inlines = [BlogInline]

admin.site.register(Person, PersonAdmin)
admin.site.register(Blog)
admin.site.register(Reaction)