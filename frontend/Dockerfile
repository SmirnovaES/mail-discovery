FROM node:9

RUN mkdir -p /app
WORKDIR /app

COPY ./package.json ./
RUN npm install

COPY ./ ./
