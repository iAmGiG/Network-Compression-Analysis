# Overview

These scripts demonstrate a basic client-server architecture using Python's socket programming. The client script (client.py) connects to the server (server.py) and requests data packets of specific sizes. The server responds by generating and sending these data packets back to the client.

## Files

- client.py: Manages the client-side operations, including connecting to the server, requesting data, and handling the reception of data.
- server.py: Manages the server-side operations, including accepting client connections, generating requested data, and sending it to the client.

## Usage

## Server Script (server.py)

- The server sets up a TCP socket on a specified port and listens for incoming connections. Upon receiving a connection, it waits for the client to send a request for a specific amount of data, generates this data using random bytes, and then sends it back to the client.

***Key Functions***

```py
def generate_data(size_in_mb):
    """
    Generates a binary string of random bytes approximately equal to the specified size in megabytes.
    """

def send_data(client_socket, data_size):
    """
    Sends a specified amount of data to the connected client socket.
    """

def main():
    """
    Main server function that sets up a server socket, listens for connections, and serves data requests.
    """
```

## Client Script (client.py)

- The client connects to the server using a TCP socket. It sends a request for a specific size of data, receives the data, and measures the time taken to complete the transaction.

***Key Functions***

```py
def connect_to_server(host, port):
    """
    Establishes a TCP connection to a specified server using a socket.
    """

def request_and_receive_data(client_socket, data_size):
    """
    Requests a specific amount of data from a server and receives it in chunks.
    """

def main():
    """
    Main execution function for the client script.
    """

```

### Running with Docker

Docker can be used to containerize and run the scripts, ensuring that the environment is consistent and isolated. Below are the steps to set up Docker containers for both the server and the client.

1. Create Dockerfiles
Dockerfile for Server
Create a file named Dockerfile-server in the directory with your server.py script:

Dockerfile

```dockerfile

# Use an official Python runtime as a parent image

FROM python:3.8-slim

# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app

ADD . /app

# Run server.py when the container launches

CMD ["python", "server.py"]
Dockerfile for Client
Create a file named Dockerfile-client in the directory with your client.py script:
```

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim
# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
ADD . /app
# Run client.py when the container launches
CMD ["python", "client.py"]
```

2. Building Docker Images
Navigate to the directory of each script and build the Docker images:

```bash
# Build the server image
docker build -f Dockerfile-server -t server-image .
# Build the client image
docker build -f Dockerfile-client -t client-image .
```

3. Running Docker Containers
Run Server Container

```bash
# Run the server container
docker run -p 5000:5000 --name server-container server-image
```

This command runs the server container and maps port 5000 of the container to port 5000 on the host, allowing the client to connect to it.

Run Client Container

```bash
# Run the client container
docker run --name client-container --link server-container client-image
```

This command runs the client container and links it to the server container. Ensure that the client script is configured to connect to the server using the server container's name or IP.
