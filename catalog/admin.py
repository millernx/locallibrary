from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

class BookInline(admin.StackedInline):
    model=Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines= [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower',  'due_back', 'display_id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
                        'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
                        'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
#admin.site.register(Book, BookInstance)
#admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Language)
