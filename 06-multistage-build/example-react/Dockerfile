FROM node:20.12-bookworm-slim as development

USER node

WORKDIR /app

EXPOSE 3000

COPY --chown=node ./package*.json ./

RUN npm ci

COPY --chown=node:node ./ ./

CMD ["npm", "start"]


FROM development as build

RUN npm run build


FROM nginx:1.25.4-alpine3.18

COPY ./virtual_host.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/build /var/www
