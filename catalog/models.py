from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g Science Fiction)')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language")
    def __str__(self):
        return self.name

class Book(models.Model):
    """Model representing a book (but not a specific copy)"""
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character  <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text = 'Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """returns the url to access a detail record for this book"""
        return reverse('book-detail', args=[(str(self.id))])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in the Admin."""
        return ', '.join(genre.name for genre in self.genre.all())

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Model representing a specific copy of a book """
    id=models.UUIDField(primary_key=True, default =uuid.uuid4, help_text='Unique ID fo this particular book across the whole library')
    book=models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back= models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering=['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def display_id(self):
        return str(self.id)[:6]
    display_id.short_description = 'ID Stub'

    @property
    def is_overdue(self):
        if self.due_back and self.due_back > date.today():
            return True
        return False

class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


