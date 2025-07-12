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

---

## Interview Answer

---

### ✅ Final Task Completion Table

| **Component**                            | **Description**                                                     | **Status** |
| ---------------------------------------- | ------------------------------------------------------------------- | ---------- |
| **CI/CD: Test Stage**                    | Runs Python tests using `pytest` in GitLab CI                       | ✅ Done     |
| **CI/CD: Build Stage**                   | Builds Docker image and pushes to GitLab Container Registry         | ✅ Done     |
| **CI/CD: Deploy Stage**                  | Runs `docker compose up -d` to start the stack on staging           | ✅ Done     |
| **Docker Compose Setup**                 | Defines `app`, `db`, and `nginx` services with volumes and networks | ✅ Done     |
| **PostgreSQL Service**                   | Configured and connected via environment variables                  | ✅ Done     |
| **FastAPI App Dockerfile**               | Functional REST API with Users and Posts                            | ✅ Done     |
| **NGINX Reverse Proxy**                  | Forwards HTTP traffic to FastAPI service at port `8000`             | ✅ Done     |
| **Nginx Configuration File**             | Includes reverse proxy and headers                                  | ✅ Done     |
| **GitLab Runner Tags**                   | Runner uses `tags: [stage]` to control deployment environment       | ✅ Done     |
| **Branch Restriction**                   | `only: [main]` ensures deploy only from main branch                 | ✅ Done     |
| **Test Coverage of API (curl / pytest)** | Manual and CI-tested with realistic endpoint calls                  | ✅ Done     |

---

### ✅ Pipeline Stages
![Pipeline](https://github.com/mhesfahani97/technical-devops/blob/main/images/pipeline.png?raw=true)

---

### ✅ Manual Curl Testing

- **test_api.sh**, manual testing commands by curl.
- **test_api_result.txt**, the result of manual testing commands.
