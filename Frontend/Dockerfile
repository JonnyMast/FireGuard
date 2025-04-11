FROM node:18

WORKDIR /app

COPY Public ./Public

RUN npm install -g live-server

CMD ["live-server", "--port=8080", "--host=0.0.0.0", "Public"]
