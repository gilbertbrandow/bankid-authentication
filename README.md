## Project Overview

### Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** React (Vite) with shadcn/ui  

## Deployment

This project can be deployed using **Docker** as two separate containers for the **backend** and **frontend**. Each service has its own **Dockerfile** for easy containerization.

### Local deployment
```
docker-compose build
docker-compose up
```