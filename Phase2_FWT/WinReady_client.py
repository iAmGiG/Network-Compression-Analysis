
import socket
import time
import pywt
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # Connect the socket to the server's address
        client_socket.connect((host, port))
        logging.info(f'Connected to server at {host}:{port}')
        return client_socket
    except socket.error as e:
        logging.error(f'Failed to connect to server at {host}:{port}, error: {e}')
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
        # Send data request to the server
        client_socket.sendall(str(data_size).encode())
        # Receive the data from the server
        received_data = client_socket.recv(1024)  # Adjust the buffer size if necessary
        logging.info(f'Received data of size: {len(received_data)}')

        # Decompress data using wavelet transform
        coeffs = pywt.wavedec(np.frombuffer(received_data, dtype=np.uint8), 'haar')
        decompressed_data = pywt.waverec(coeffs, 'haar')

        return decompressed_data
    except Exception as e:
        logging.error(f'Error during data reception or processing: {e}')
        raise

def main():
    server_host = '127.0.0.1'  # Change to actual server IP if necessary
    server_port = 12345        # Change to actual server port if necessary

    # Establish connection to server
    client_socket = connect_to_server(server_host, server_port)
    try:
        # Request data and receive response
        data_size = 5  # Change based on how much data is expected
        data = request_and_receive_data(client_socket, data_size)
        logging.info(f'Data processed successfully')
    finally:
        # Clean up the connection
        client_socket.close()
        logging.info('Connection closed')

if __name__ == '__main__':
    main()
