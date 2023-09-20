FROM node:16-alpine

WORKDIR /usr/src/frontend

COPY . .

RUN npm ci --dev

CMD ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
