from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from movies.models import FilmWork

class MovieListView(View):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        movies = FilmWork.objects.prefetch_related('genres', 'persons').all()
        paginator = Paginator(movies, 10)  # 10 movies per page

        page_obj = paginator.get_page(page_number)

        response = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next': page_obj.next_page_number() if page_obj.has_next() else None,
            'results': [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'description': movie.description,
                    'creation_date': movie.creation_date,
                    'rating': movie.rating,
                    'type': movie.type,
                    'genres': [genre.name for genre in movie.genres.all()],
                    'actors': [person.full_name for person in movie.persons.filter(personfilmwork__role='actor')],
                    'directors': [person.full_name for person in movie.persons.filter(personfilmwork__role='director')],
                    'writers': [person.full_name for person in movie.persons.filter(personfilmwork__role='writer')],
                }
                for movie in page_obj
            ]
        }
        
        return JsonResponse(response, safe=False)

class MovieDetailView(View):
    def get(self, request, id):
        movie = get_object_or_404(FilmWork, id=id)
        response = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'creation_date': movie.creation_date,
            'rating': movie.rating,
            'type': movie.type,
            'genres': [genre.name for genre in movie.genres.all()],
            'actors': [person.full_name for person in movie.persons.filter(personfilmwork__role='actor')],
            'directors': [person.full_name for person in movie.persons.filter(personfilmwork__role='director')],
            'writers': [person.full_name for person in movie.persons.filter(personfilmwork__role='writer')],
        }
        
        return JsonResponse(response)
