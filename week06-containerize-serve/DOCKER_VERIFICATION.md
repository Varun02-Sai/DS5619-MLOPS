# Docker verification

Fill this in after you build and run your container (see README.md,
"Part 2 — Dockerfile"). This is how we confirm your container actually works, since an
automated grader running in a sandbox may not always have Docker-in-Docker
available.

## Build

Paste the command you ran and its final output line (the one showing the
built image ID/tag):

```
docker build -t week6-detector .
naming to docker.io/library/week6-detector:latest done
```

## Run

Paste the command you used to start the container (should map a host port
to the container's 8080):

```
docker run --rm -p 8080:8080 week6-detector
```

## Verify

Paste the exact `curl` commands and their JSON output for both endpoints,
run against the running container (not against `python src/app.py` directly
— the point is to prove the *container* works):

```
curl http://localhost:8080/health
{"status":"ok"}

curl -F "image=@data/fixtures/camera_A_daylight/000.jpg" http://localhost:8080/detect
{"count":4,"detections":[{"bbox":[261,6,41,13],"category_id":1,"id":0,"image_id":0,"score":0.836},{"bbox":[273,10,43,17],"category_id":3,"id":1,"image_id":0,"score":0.98},{"bbox":[111,84,29,21],"category_id":7,"id":2,"image_id":0,"score":0.98},{"bbox":[17,138,21,25],"category_id":7,"id":3,"image_id":0,"score":0.98}]}
```
