FROM mongo:4.2.14

COPY /docker/db/mongo/start.sh ./

RUN chmod 755 ./start.sh

CMD ["./start.sh"]