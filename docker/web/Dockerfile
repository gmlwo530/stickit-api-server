FROM nginx

RUN apt-get update -qq && apt-get -y install apache2-utils

ENV FASTAPI_ROOT /app/

WORKDIR $FASTAPI_ROOT

RUN mkdir log

# Copy over static assets
# COPY public public/

COPY /docker/web/nginx/nginx.conf /tmp/app.conf

EXPOSE 80

COPY docker/web/nginx/start.sh ./

RUN chmod 755 ./start.sh

CMD ["./start.sh"]