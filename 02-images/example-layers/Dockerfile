FROM debian:bookworm-slim

WORKDIR /workdir

RUN dd if=/dev/zero of=test10 bs=1M count=10

RUN rm test10

RUN dd if=/dev/zero of=test20 bs=1M count=20 && rm test20

CMD ["ls", "-la"]
