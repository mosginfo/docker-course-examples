FROM alpine:3.19.1

RUN apk update && apk add --no-cache \
        whois \
    && rm -rf /var/cache/apk/*

ENTRYPOINT ["whois"]

CMD ["--help"]
