import factory
from plexus.grainlog.models import GrainLog


class GrainLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = GrainLog

    sha1 = 'asdfasdfasdfasdf'
    payload = '{"foo": "bar"}'
