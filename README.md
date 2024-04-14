# Network-Compression-Analysis

A comparative analysis of Fast Wavelet Transform (FWT) compression versus traditional compression methods on network performance, focusing on throughput and latency. This project aims to explore the effectiveness of FWT in modern digital communication environments.

## Steps for Running Baseline Tests

Prepare the Environment:

- Ensure both (client) and (server) scripts are properly set up and configured with the necessary software and scripts as previously discussed.
- Make sure that both machines are on the same network or configured such that they can communicate over the intended port (default is 5000).

## Start the Server on VM2

- Open a terminal window on VM2.
- Navigate to the directory containing server.py.
- Run the server script by typing:

```bash
python3 server.py
```

- There may be a need to use py, python.exe, python, depending on the platform or instaliation solution.
- Ensure the server starts successfully and is listening on the specified port.

## Run the Client

- Open a terminal/CMD (PS/Bash) window.
- Navigate to the directory containing client.py.
- Run the client script by typing:

```bash
python3 client.py
```

- Ensure the client is able to connect to the server and request data.

## Observe and Record Results

- On the client, observe the output in the client's terminal window. For each requested data size (1MB, 10MB, 100MB), the output should display:

```powershell
- The data size requested.
- The length of the received data (to verify that it matches the requested size).
- The latency (time taken in seconds to receive the data).
```

- It's crucial that the received data length matches the requested size to ensure that the network is transmitting data correctly.

## Repeat Tests

- To improve the reliability and accuracy of your results, repeat steps 3 and 4 multiple times. This helps in accounting for network variability and provides a more stable average for later analysis.
- Collect and record the data for each test run. You might want to automate this recording or manually log the outputs in a structured format (e.g., a spreadsheet).

## Analyze Baseline Data

- Once you have collected sufficient data, analyze the variations in latency and throughput across different test runs.
- This baseline performance will help you to better understand the impact of FWT compression.

## Docker setup and testing

1. Step 1: Install Docker

- First, ensure Docker is installed on your VM. If not, install it using:

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

2. Step 2: Create Docker Images

- You’ll need Docker images that include all the necessary software, like Python, iperf3, and any other tools or libraries your scripts depend on.

Build the Docker images by running:

```bash
docker build -t server-image -f Dockerfile.server .
docker build -t client-image -f Dockerfile.client .
```

3. Step 3: Run Containers
Launch the containers on your VM. You can use Docker’s network features to mimic a real network scenario.

```bash
# Start the server container
docker run -d --name server-container server-image

# Start the client container and link it to the server
docker run --name client-container --link server-container client-image
```

4. Step 4: Networking Considerations
When using Docker, you can customize the network settings to more accurately simulate different network conditions. Docker allows you to create custom networks which can help in emulating different latency, bandwidth, and packet loss scenarios:

```bash
# Create a custom network
docker network create --driver bridge custom-net

# Start containers on the custom network
docker run -d --network custom-net --name server-container server-image
docker run -d --network custom-net --name client-container client-image
```
