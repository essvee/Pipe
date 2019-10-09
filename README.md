## Installation

### Requirements
- [docker](https://docs.docker.com)
- [docker compose](https://docs.docker.com/compose/install)
- [git](https://git-scm.com)

### Process

1. Build the containers:

    ```sh
    git clone https://github.com/alycejenni/Pipe.git
    cd Pipe
    docker-compose up --abort-on-container-exit
    ```
   
2. Get & store Gmail credentials:

    ```sh
    docker run -it pipe_backend python /opt/app/deploy/auth.py --noauth_local_webserver
    ```
   
## Run

```sh
docker-compose up --abort-on-container-exit
```