# Summary
Writes demo logs. Both JSON and String logs are emitted.  

# Options
The application operates in 3 modes
- Standard Out
- HTTP Post
- File

## Standard Out
Default mode, if no environement variables are present the logs will be emitted to stdout.

## HTTP Post
Controlled via ENV varaible: **HTTP_URL**
The application will post to that URL unauthenticated.

## File
Controlled via ENV varaible: **FILE_PATH**
Will create the required directories and write the logs to that path.

# Docker 
## Run
Stdout

```docker run -rm -d chadtsigler/training-data:v1.0```

HTTP Post

```docker run -rm -d -e HTTP_URL=https://exampleurl.com chadtsigler/training-data:v1.0```

File

```docker run -rm -d -v /var/docker/path:/var/mounted/path -e FILE_PATH=/var/mounted/path/log.txt chadtsigler/training-data:v1.0```

## Compose
Stdout

```docker compose -f https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/docker_compose/compose_stdout.yml up```

HTTP Post

```
wget https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/docker_compose/compose_http.yml
--update url
nano compose_http
docker compose -f compose_http.yml up
```

File

```
wget https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/docker_compose/compose_file.yml
--update mounts and paths
nano compose_file.yml
docker compose -f compose_file.yml up
```

# K8s
Stdout

```
kubectl create namespace logs
kubectl apply -f https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/k8s/k8s_stdout.yml -n logs
```

HTTP Post

```
kubectl create namespace logs
wget https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/k8s/k8s_http.yml
--update url
nano k8s_http.yml
kubectl apply -f k8s_http.yml -n logs
```

File

```
kubectl create namespace logs
wget https://raw.githubusercontent.com/csedgedelta/demo_data/refs/heads/main/k8s/k8s_file.yml
--update mounts and paths
nano k8s_file.yml
kubectl apply -f k8s_file.yml -n logs
```
