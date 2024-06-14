FROM mcr.microsoft.com/dotnet/sdk:6.0 as build

WORKDIR /usr/local/src/webone

ARG TEST_VAR=Hello World

ARG WEBONE_VERSION="0.16.3"
ARG WEBONE_BASE_URL="https://github.com/atauenis/webone/archive/refs/tags"

ADD ${WEBONE_BASE_URL}/v${WEBONE_VERSION}.tar.gz /tmp/webone.tar.gz

RUN tar --strip-components=1 -xzf /tmp/webone.tar.gz \
    && dotnet publish -r linux-x64 -c Release -o /opt/webone/ ./WebOne.csproj


FROM mcr.microsoft.com/dotnet/runtime:6.0

WORKDIR /opt/webone

EXPOSE 8080

RUN useradd -s /usr/sbin/nologin webone \
    && apt update && apt install -yq --no-install-recommends \
        imagemagick \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/webone .

USER webone

CMD ["./webone"]
