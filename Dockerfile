FROM nginx:stable-alpine

# Copy all files to nginx html dir. Ensure your built `sc-datav` is present in the repo root.
COPY . /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
