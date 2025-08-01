# API
API_IMAGE_NAME := fastapi-sentiment-app
API_PORT := 8000
# Monitoring
MONITORING_IMAGE_NAME := streamlit-monitoring-app
MONITORING_PORT := 8501
# VOLUME
LOG_VOLUME := logs

build:
	@echo "Building API Docker image: $(API_IMAGE_NAME)"
	docker build -t $(API_IMAGE_NAME) ./api

	@echo "Building Monitoring Docker image: $(MONITORING_IMAGE_NAME)"
	docker build -t $(MONITORING_IMAGE_NAME) ./monitoring

run:
	@echo "Creating Docker volume: $(LOG_VOLUME)"
	docker volume create $(LOG_VOLUME)

	@echo "Running API Docker container: $(API_IMAGE_NAME) on port $(API_PORT)"
	docker run --rm -d -v $(LOG_VOLUME):/logs -p $(API_PORT):8000 $(API_IMAGE_NAME)

	@echo "Running Monitoring Docker container on port $(MONITORING_PORT)"
	docker run --rm -d -v $(LOG_VOLUME):/logs -p $(MONITORING_PORT):$(MONITORING_PORT) $(MONITORING_IMAGE_NAME)

clean:
	@echo "Removing API Docker image: $(API_IMAGE_NAME)"
	docker rmi $(API_IMAGE_NAME) || true

	@echo "Removing Monitoring Docker image: $(MONITORING_IMAGE_NAME)"
	docker rmi $(MONITORING_IMAGE_NAME) || true

	@echo "Removing Docker volume: $(LOG_VOLUME)"
	docker volume rm $(LOG_VOLUME) || true