FROM debian:bookworm-slim AS compiler

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt update && apt install -yq --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN g++ -static -o ipclassifier main.cpp


FROM scratch

COPY --from=compiler /app/ipclassifier /

ENTRYPOINT ["/ipclassifier"]
