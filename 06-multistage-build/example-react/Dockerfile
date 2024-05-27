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


FROM node:20.12-bookworm-slim as production

WORKDIR /var/www

EXPOSE 3000

RUN npm install -g serve

COPY --from=build /app/build ./

USER node

CMD ["serve", "-s", "-p", "3000", "."]


FROM nginx:1.25.4-alpine3.18

WORKDIR /var/www

COPY ./virtual_host.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build ./
