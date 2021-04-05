FROM node:12.12.0

WORKDIR /frontend

COPY . /frontend

RUN yarn install

EXPOSE 80

# Run app.py when the container launches
CMD ["yarn", "run", "serve"]