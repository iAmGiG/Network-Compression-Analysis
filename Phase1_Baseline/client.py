import socket
import time


def connect_to_server(host, port):
    """
    Establishes a TCP connection to a specified server using a socket.

    Parameters:
    - host (str): The hostname or IP address of the server to connect to.
    - port (int): The port number on the server to connect to.

    Returns:
    - socket.socket: A socket object that is connected to the server.
    """
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server's address
    client_socket.connect((host, port))
    return client_socket


def request_and_receive_data(client_socket, data_size):
    """
    Requests a specific amount of data from a server and receives it in chunks.

    Parameters:
    - client_socket (socket.socket): The client socket that is connected to the server.
    - data_size (int): The size of the data to request from the server in megabytes.

    Returns:
    - tuple: A tuple containing:
        - bytearray: The received data as a bytearray.
        - float: The total time elapsed during the data reception in seconds.
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
    Main execution function for the client script. Connects to a server, requests, and receives data in predefined sizes.

    Steps:
    - Establishes a connection to the server.
    - Iterates through a list of data sizes, requests data for each size, and measures the time taken to receive the data.
    - Displays the requested size, received data length, and the time taken for each transaction.

    Uses:
    - Useful for testing the latency and effectiveness of data transmission over a network.
    """
    server_host = '0.0.0.0'
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
