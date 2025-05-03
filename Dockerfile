FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG APPDIR=/app
ARG SRC=grafana_api

# ENV TZ=America/Chicago
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# target directories are created automatically if they don't already exist
COPY ${SRC}/*.py ${SRC}/*.sh requirements.txt ${APPDIR}/
COPY ${SRC}/conf/ ${APPDIR}/conf/
RUN pip install --no-cache-dir -r ${APPDIR}/requirements.txt

WORKDIR ${APPDIR}
ENTRYPOINT [ "./entrypoint.sh" ]
