FROM node:22-slim
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev || npm install --omit=dev
COPY . .
ENV DATA_DIR=/data
VOLUME ["/data"]
EXPOSE 8080
CMD ["node", "index.mjs"]
