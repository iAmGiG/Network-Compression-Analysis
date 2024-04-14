import socket
import time


def connect_to_server(host, port):
    """
    create socket and connect to the host.
    """
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server's address
    client_socket.connect((host, port))
    return client_socket


def request_and_receive_data(client_socket, data_size):
    """
    Reques the data and waits for it.
    """
    # Send data request to server
    client_socket.sendall(str(data_size).encode('utf-8'))

    # Start the timer
    start_time = time.time()

    received_data = bytearray()
    while True:
        # Receive data in chunks
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        received_data.extend(chunk)

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    return received_data, elapsed_time


def main():
    """
    Connect to Server: The connect_to_server function establishes a 
    TCP connection to the server on a 
    specified IP and port.

    Request and Receive Data: The request_and_receive_data function sends a 
    request for data of a specific size, 
    starts timing, receives the data in chunks until no more data is available, 
    then stops the timer 
    and calculates the elapsed time.

    Timing Data Transfers: The client measures how long it takes to 
    receive the data from the server, 
    which is crucial for evaluating the impact of different 
    compression techniques on latency.

    Iterating Through Data Sizes: The main function connects 
    to the server and loops through a list of 
    predetermined data sizes (1MB, 10MB, 100MB). 
    For each size, it requests the data, receives it, 
    and prints out the size, received data length, and latency.

    Verifying Data Completeness: The script prints the amount of data received to help verify that 
    the full data packet has been correctly transmitted. 
    """
    server_host = '0.0.0.0'  # Replace with the actual server IP address
    server_port = 5000

    client_socket = connect_to_server(server_host, server_port)
    try:
        for data_size in [1, 10, 100]:  # Data sizes in MB
            received_data, elapsed_time = request_and_receive_data(
                client_socket, data_size)
            print(
                f"Requested {data_size}MB: Received {len(received_data) / (1024 * 1024)}MB in {elapsed_time} seconds")
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
