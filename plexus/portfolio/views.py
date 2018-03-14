from django.shortcuts import render
from django.views.generic.base import View
from wagtail.wagtailsearch.models import Query

from .models import Entry
from plexus.main.views import LoggedInMixin


class Search(LoggedInMixin, View):
    def get(self, request):
        # Search
        search_query = request.GET.get('query', None)
        if search_query:
            search_results = Entry.objects.live().search(search_query)

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()
        else:
            search_results = Entry.objects.none()

        # Render template
        return render(request, 'portfolio/search_results.html', {
            'search_query': search_query,
            'search_results': search_results,
        })
