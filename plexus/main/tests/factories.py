import factory
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from plexus.main.models import (
    Location, OSFamily, OperatingSystem, IPAddress,
    Server, Alias, Contact, Technology, Application,
    ApplicationAlias, ApplicationContact, ServerContact,
    Lease)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Location

    name = "test"
    details = "test location"


class OSFamilyFactory(factory.DjangoModelFactory):
    class Meta:
        model = OSFamily

    name = "test os family"


class OperatingSystemFactory(factory.DjangoModelFactory):
    class Meta:
        model = OperatingSystem

    family = factory.SubFactory(OSFamilyFactory)
    version = "1.0"


class ServerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Server

    name = "test server"
    location = factory.SubFactory(LocationFactory)
    operating_system = factory.SubFactory(OperatingSystemFactory)


class IPAddressFactory(factory.DjangoModelFactory):
    class Meta:
        model = IPAddress

    ipv4 = "127.0.0.1"
    mac_addr = "00:16:3e:e3:61:53"
    server = factory.SubFactory(ServerFactory)


class AliasFactory(factory.DjangoModelFactory):
    class Meta:
        model = Alias

    hostname = "foo.example.com"
    ip_address = factory.SubFactory(IPAddressFactory)
    status = "active"


class ContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contact

    name = "anders"
    email = "anders@columbia.edu"
    phone = "4-1813"


class TechnologyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Technology

    name = "Django"


class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Application

    name = "Test Application"
    description = "A Description"
    technology = factory.SubFactory(TechnologyFactory)
    graphite_name = "foo"
    sentry_name = "foo"
    pmt_id = 123


class ApplicationAliasFactory(factory.DjangoModelFactory):
    class Meta:
        model = ApplicationAlias

    application = factory.SubFactory(ApplicationFactory)
    alias = factory.SubFactory(AliasFactory)


class ApplicationContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = ApplicationContact

    application = factory.SubFactory(ApplicationFactory)
    contact = factory.SubFactory(ContactFactory)


class ServerContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = ServerContact

    server = factory.SubFactory(ServerFactory)
    contact = factory.SubFactory(ContactFactory)


class LeaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Lease

    application = factory.SubFactory(ApplicationFactory)
    user = factory.SubFactory(UserFactory)
    start = factory.LazyFunction(lambda: datetime.now() - timedelta(weeks=6))
    end = factory.LazyFunction(lambda: datetime.now() + timedelta(weeks=6))
