FROM ccnmtl/django.base
ADD wheelhouse /wheelhouse
RUN /ve/bin/pip install --no-index -f /wheelhouse -r /wheelhouse/requirements.txt \
&& rm -rf /wheelhouse
WORKDIR /app
COPY . /app/
RUN /ve/bin/flake8 /app/plexus/ --max-complexity=8
RUN /ve/bin/python manage.py test
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP plexus
ENTRYPOINT ["/run.sh"]
CMD ["run"]
