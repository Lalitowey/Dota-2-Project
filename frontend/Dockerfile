# Stage 1: Build the Nuxt app
FROM node:18-alpine as build-stage

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock if you use yarn)
# Source path is relative to the build context (Dota-2-Project/frontend/)
# So, we need to specify the 'dota2project' subdirectory
COPY dota2project/package*.json ./

# Install dependencies
# npm will look for package.json in the current WORKDIR (/app)
RUN npm install

# Copy the rest of the Nuxt project source code from the dota2project subdirectory
COPY dota2project/. ./

# Build the Nuxt application for production
# Nuxt's build command is typically 'npm run build'
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine

# Nuxt 3 default output directory for a static build is .output/public
# In the build-stage, our WORKDIR was /app, so the files are in /app/.output/public
COPY --from=build-stage /app/.output/public /usr/share/nginx/html

# For a Nuxt SPA, you need proper Nginx configuration to handle client-side routing.
# Create a file named 'nginx.conf' in your 'frontend/dota2project/' directory (see content below)
# This nginx.conf will be copied to /app/nginx.conf in the build-stage by "COPY dota2project/. ./"
# Then we copy it from the build-stage to the Nginx config directory.
COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]