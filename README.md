## Interview Task: “Deploy a FastAPI Service with CI/CD”

### Scenario

You need to set up deployment for a simple FastAPI service that connects to PostgreSQL, with Nginx as a reverse proxy.

### Task Components

**Part 1: CI/CD Pipeline**

- Write a `.gitlab-ci.yml` file that:
  - Runs Python tests
  - Builds a Docker image for the FastAPI app
  - Deploys to a staging environment
  - Include at least 3 stages: test, build, deploy

**Part 2: Infrastructure Setup**

- Create a `docker-compose.yml` with:
  - FastAPI service
  - PostgreSQL database
  - Nginx reverse proxy
- Write an Nginx configuration for the FastAPI service
