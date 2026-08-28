build:
    podman build -t wakebot .

run: build
    podman run  --network=host -it --env-file .env wakebot
