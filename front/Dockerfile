FROM node:15.11.0-alpine3.10

WORKDIR /usr/src/app/frontend

COPY ./package*.json ./

RUN npm install

COPY . .

RUN npm run build