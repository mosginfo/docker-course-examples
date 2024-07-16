FROM node:20.14-bookworm-slim AS development

USER node

WORKDIR /app

EXPOSE 5173

RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    --mount=type=bind,source=./package.json,target=package.json \
    --mount=type=bind,source=./package-lock.json,target=package-lock.json \
    npm ci

COPY --chown=node ./ ./

CMD ["npm", "run", "dev", "--", "--host"]


FROM development AS build

RUN npm run build


FROM nginx:1.27-bookworm AS production

COPY --from=build /app/dist /var/www
