import socket
import time
import pywt
import numpy as np
import logging
import pickle
import os

# Creates a 'logs' directory in the current working directory
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

client_log_file = os.path.join(log_dir, 'client.log')

# Set up logging
logging.basicConfig(filename=client_log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_server(host, port):
    """
    Establishes a TCP connection to a specified server using a socket.

    Parameters:
    - host (str): The hostname or IP address of the server to connect to.
    - port (int): The port number on the server to connect to.

    Returns:
    - socket.socket: A socket object that is connected to the server.
    """
    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Set a timeout of 60 seconds for all socket operations
        client_socket.settimeout(60)
        # Connect the socket to the server's address
        client_socket.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        logging.info(f'Connected to server at {host}:{port}')
        return client_socket
    except socket.error as e:
        print(f'Failed to connect to server at {host}:{port}, error: {e}')
        logging.error(
            f'Failed to connect to server at {host}:{port}, error: {e}')
        raise


def request_and_receive_data(client_socket, data_size):
    """
    Sends a data size request to the server, receives compressed data,
    decompresses it using wavelet transforms, and measures the time taken.

    Parameters:
    - client_socket (socket.socket): The client socket to use for communication.
    - data_size (int): The size of the data requested from the server.

    Returns:
    - np.array: Decompressed data as a numpy array.
    """
    try:
        print(f"Requesting {data_size} MB of data from the server.")
        logging.info(f"Requesting {data_size} MB of data from the server.")
        # Send data request to the server
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)  # Set receive buffer to 1 MB
        client_socket.sendall(str(data_size).encode())
        # Receive the data from the server
        received_data = b''
        while True:
            # Adjust the buffer size if necessary
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            received_data += chunk
        print(f"Received data of size: {len(received_data)} bytes")
        logging.info(f'Received data of size: {len(received_data)} bytes')

        # Deserialize wavelet coefficients using pickle
        coeffs = pickle.loads(received_data)
        # Decompress data using wavelet transform
        decompressed_data = pywt.waverec(coeffs, 'haar')

        return decompressed_data
    except socket.timeout as e:
        print(f"Timed out while receiving {data_size} MB of data.")
        logging.error(f"Timed out while receiving {data_size} MB of data.")
        return None
    except Exception as e:
        print(f'Error during data reception or processing: {e}')
        logging.error(f'Error during data reception or processing: {e}')
        raise


def main():
    server_host = '127.0.0.1'  # Change to actual server IP if necessary
    server_port = 12345        # Change to actual server port if necessary

    # Establish connection to server
    client_socket = connect_to_server(server_host, server_port)
    try:
        # Request data and receive response
        for data_size in [1, 10, 100]:
            start_time = time.time()
            data = request_and_receive_data(client_socket, data_size)
            elapsed_time = time.time() - start_time
            if data is not None:
                throughput = data_size / elapsed_time
                logging.info(
                    f"Received {data_size} MB of data in {elapsed_time:.2f} seconds with throughput of {throughput:.2f} MB/s")
                print(
                    f"Data Size: {data_size} MB, Time: {elapsed_time:.2f} s, Throughput: {throughput:.2f} MB/s")
            else:
                logging.info(f"Failed to receive {data_size} MB of data.")
                print(f"Failed to receive {data_size} MB of data.")
    finally:
        # Clean up the connection
        client_socket.close()
        logging.info('Connection closed')
        print('Connection closed')


if __name__ == '__main__':
    main()
