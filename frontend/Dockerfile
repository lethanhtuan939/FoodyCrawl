FROM node:18-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

# Sao chép file build từ stage trước
COPY --from=build /app/dist /usr/share/nginx/html

# Sao chép file cấu hình Nginx từ thư mục nginx
COPY ../nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Mở cổng 80
EXPOSE 80

# Chạy Nginx
CMD ["nginx", "-g", "daemon off;"]