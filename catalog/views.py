from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site"""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available BookInstances
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # All is implied by default:
    num_authors =Author.objects.count()
    num_genres = Genre.objects.count()


    # Books Containing "The"
    num_books_with_the = Book.objects.filter(title__icontains='the').count()

    num_visits= request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_the': num_books_with_the,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)

class BookListView(ListView):
    model = Book
    paginate_by =10

class BookDetailView(DetailView):
    model = Book

class AuthorListView(ListView):
    model = Author
    paginate_by_=10

class AuthorDetailView(DetailView):
    model=Author

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10


    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
