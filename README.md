[![Build Status](https://travis-ci.org/ccnmtl/plexus.png)](https://travis-ci.org/ccnmtl/plexus)

## plexus

Our little in-house app for keeping track of our servers.

### docker-compose

The easiest way to run this locally is with docker and
docker-compose. It's as easy as:

    $ make build
    $ docker-compose run web migrate # to set up database schema
    $ docker-compose up

And you should have a dev instance running on port 8000.

If you update the dependencies (in `requirements.txt` or
`package.json`), re-run `make build` to update the docker image.

You can re-run `docker-compose run web migrate` at any point if there
are migrations.

If you aren't using CAS, you'll want a local django superuser, so
create it with:

     $ docker-compose run web manage createsuperuser
