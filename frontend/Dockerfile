# Use the official node image as the base image
FROM --platform=linux/amd64 node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 3000
EXPOSE 5173

# Start the application
CMD ["npm", "run", "dev"]