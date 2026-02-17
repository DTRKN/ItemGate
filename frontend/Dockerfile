# Stage 1: Build фронтенда
FROM node:18-alpine as builder

WORKDIR /app

# Копируем package файлы
COPY package.json package-lock.json ./

# Устанавливаем зависимости
RUN npm ci || npm install

# Копируем исходный код
COPY . .

# Собираем production build
RUN npm run build

# === Stage 2: Production образ с Nginx ===
FROM nginx:alpine

# Копируем собранные файлы из builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose порт
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
