# Hits
Demo app for my video tutorial on load balancing an application. The app simply counts and displays page hits. Each app instance should be given a unique id (INSTANCE_ID) so that you can easily see how the load balancer works.

## Dev setup
- Clone/download this repo
- Install Docker and Docker Compose
- Create *.env* from *.env.example* and make necessary changes
- Run `docker-compose up` in project root

## Prod setup
- Provision a server
- Install Git and clone this repo
- Install Docker and Docker Compose
- Create *.env* from *.env.example* and make necessary changes
- Run `docker-compose -f docker-compose.prod.yml up --build -d` in project root