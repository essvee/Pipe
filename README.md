## Installation

### Requirements
- [docker](https://docs.docker.com)
- [docker compose](https://docs.docker.com/compose/install)
- [git](https://git-scm.com)

### Process

1. Build the containers:

    ```sh
    git clone https://github.com/NaturalHistoryMuseum/annette.git
    cd annette
    docker-compose up --abort-on-container-exit
    ```
   
2. Get & store Gmail credentials:

    ```sh
    docker run -it annette_backend python /opt/app/deploy/auth.py --noauth_local_webserver
    ```
   
## Run

```sh
docker-compose up --abort-on-container-exit
```
