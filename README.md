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

```docker compose -f compose_stdout.yml up```

HTTP Post

```s```

File

```s```

# K8s
Stdout

```kubectl apply -f ```

HTTP Post

```kubectl apply -f ```

File

```kubectl apply -f ```
