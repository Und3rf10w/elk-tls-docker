ARG ELK_VERSION

FROM docker.elastic.co/beats/filebeat:${ELK_VERSION}

RUN filebeat modules enable threatintel
CMD  filebeat export template > filebeat.template.json \
    cat filebeat.template.json | curl -u "${ELASTIC_USERNAME}:${ELASTIC_PASSWORD}" -XPUT "${ELASTICSEARCH_HOSTS}/_template/filebeat-${ELK_VERSION}" -d @- --insecure
