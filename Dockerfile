# Use an official base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Create a simple hello world app
RUN echo 'console.log("Hello, World!");' > index.js
RUN echo '{"name":"hello-world","version":"1.0.0","scripts":{"start":"node index.js"}}' > package.json

# No need for npm install as we don't have dependencies

# Expose port that the app runs on
EXPOSE 3000

# Define the command to run the application
CMD ["npm", "start"]
