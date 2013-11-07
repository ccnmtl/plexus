import factory
from plexus.main.models import Location
from plexus.main.models import OSFamily
from plexus.main.models import OperatingSystem
from plexus.main.models import IPAddress
from plexus.main.models import Server
from plexus.main.models import Alias
from plexus.main.models import VMLocation
from plexus.main.models import Contact
from plexus.main.models import AliasContact
from plexus.main.models import Technology
from plexus.main.models import Application


class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Location
    name = "test"
    details = "test location"


class OSFamilyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OSFamily
    name = "test os family"


class OperatingSystemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OperatingSystem
    family = factory.SubFactory(OSFamilyFactory)
    version = "1.0"


class ServerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Server
    name = "test server"
    virtual = False
    location = factory.SubFactory(LocationFactory)
    operating_system = factory.SubFactory(OperatingSystemFactory)


class IPAddressFactory(factory.DjangoModelFactory):
    FACTORY_FOR = IPAddress
    ipv4 = "127.0.0.1"
    mac_addr = "00:16:3e:e3:61:53"
    server = factory.SubFactory(ServerFactory)


class AliasFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Alias
    hostname = "foo.example.com"
    ip_address = factory.SubFactory(IPAddressFactory)
    status = "active"


class VMLocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = VMLocation
    dom_u = factory.SubFactory(ServerFactory)
    dom_0 = factory.SubFactory(ServerFactory)


class ContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact
    name = "anders"
    email = "anders@columbia.edu"
    phone = "4-1813"


class AliasContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AliasContact
    alias = factory.SubFactory(AliasFactory)
    contact = factory.SubFactory(ContactFactory)


class TechnologyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Technology
    name = "Django"


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application
    name = "Test Application"
    description = "A Description"
    technology = factory.SubFactory(TechnologyFactory)
    graphite_name = "foo"
    sentry_name = "foo"
    pmt_id = 123
