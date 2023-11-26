# simple-callback-server
Simple callback server for storing webhook callbacks

Run the Docker container: docker run -p 8000:5000 -d artemkqa/callback-server-qa Access the server at http://localhost:8000. Endpoints:

POST /webhook: Receive and store a callback. GET /webhook/{task_id}: Retrieve a callback by task ID. GET /webhook/all: Retrieve all stored callbacks. DELETE /webhook/delete-all: Delete all stored callbacks.

Docker Hub: https://hub.docker.com/repository/docker/artemkqa/callback-server-qa
