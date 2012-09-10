from annoying.decorators import render_to
from plexus.main.models import Server, Alias

@render_to('main/index.html')
def index(request):
    return dict(servers=Server.objects.all(),
                aliases=Alias.objects.all())
