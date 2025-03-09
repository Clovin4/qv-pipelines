set-prod:
	@echo "Setting up the workshop API..."
	export PREFECT_API_URL="http://workflows.mlworkshop.space:4200/api"
	@echo "PREFECT_API_URL set to $$PREFECT_API_URL"

# Variables
IMAGE_NAME = your-username/your-repository
TAG = latest

# Default target
.PHONY: all
all: build

# Build the Docker image
.PHONY: build
build:
    docker build -t $(IMAGE_NAME):$(TAG) .

# Tag the Docker image
.PHONY: tag
tag:
    docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):$(TAG)

# Push the Docker image to Docker Hub
.PHONY: push
push: login
    docker push $(IMAGE_NAME):$(TAG)

# Log in to Docker Hub
.PHONY: login
login:
    docker login

# Clean up Docker images
.PHONY: clean
clean:
    docker rmi $(IMAGE_NAME):$(TAG)