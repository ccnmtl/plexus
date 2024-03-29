import factory
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from plexus.main.models import (
    Location, IPAddress,
    Server, Alias, Contact, Technology, Application,
    ApplicationAlias, ApplicationContact, ServerContact,
    Lease)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    name = "test"
    details = "test location"


class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Server

    name = "test server"
    location = factory.SubFactory(LocationFactory)


class IPAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IPAddress

    ipv4 = "127.0.0.1"
    mac_addr = "00:16:3e:e3:61:53"
    server = factory.SubFactory(ServerFactory)


class AliasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Alias

    hostname = "foo.example.com"
    ip_address = factory.SubFactory(IPAddressFactory)
    status = "active"


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    name = "anders"
    email = "anders@columbia.edu"
    phone = "4-1813"


class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Technology

    name = "Django"


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application

    name = "Test Application"
    description = "A Description"
    technology = factory.SubFactory(TechnologyFactory)
    graphite_name = "foo"
    sentry_name = "foo"
    pmt_id = 123


class ApplicationAliasFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApplicationAlias

    application = factory.SubFactory(ApplicationFactory)
    alias = factory.SubFactory(AliasFactory)


class ApplicationContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApplicationContact

    application = factory.SubFactory(ApplicationFactory)
    contact = factory.SubFactory(ContactFactory)


class ServerContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServerContact

    server = factory.SubFactory(ServerFactory)
    contact = factory.SubFactory(ContactFactory)


class LeaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lease

    application = factory.SubFactory(ApplicationFactory)
    user = factory.SubFactory(UserFactory)
    start = factory.LazyFunction(lambda: datetime.now() - timedelta(weeks=6))
    end = factory.LazyFunction(lambda: datetime.now() + timedelta(weeks=6))
