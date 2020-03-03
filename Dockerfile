FROM node:lts-alpine3.9
WORKDIR /app
COPY ./package.json /app/package.json
COPY ./ /app/
RUN apk add git && npm install
ENV PATH /app/node_modules/.bin:$PATH
RUN ng build --prod


FROM pierrezemb/gostatic:latest
COPY --from=0 /app/dist/vrt-demo /srv/http
EXPOSE 8043

#FROM node:lts-alpine3.9
#WORKDIR /app
#RUN npm install @angular/cli
#COPY --from=0 /app/ /app
#COPY package*.json /app/
#ENV PATH /app/node_modules/.bin:$PATH
#EXPOSE 4200
#WORKDIR /app/dist/vrt-demo
#ENTRYPOINT ["ng",  "serve",  "--disable-host-check", "--host",  "0.0.0.0" ]
