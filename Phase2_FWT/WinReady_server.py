import pywt
import numpy as np
import socket
import time
import os
import logging
import pickle  # Using pickle for serialization of complex objects

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_data(size_in_mb):
    """
    Generates a binary string of random bytes approximately equal to the specified size in megabytes.

    Parameters:
    - size_in_mb (int): The size of the data to generate in megabytes.

    Returns:
    - bytes: A bytes object containing random data of the specified size.
    """
    return os.urandom(size_in_mb * 1024 * 1024)

def send_data(client_socket, data_size):
    """
    Generates data, compresses it using Fast Wavelet Transform (FWT), 
    and sends the compressed data to the client using serialization.

    Parameters:
    - client_socket (socket.socket): The client socket to send data to.
    - data_size (int): The size of the data to generate and send in megabytes.

    Process:
    - The data is first converted to a numpy array.
    - A wavelet decomposition is performed on the array.
    - The wavelet coefficients are serialized using pickle and sent over the socket.

    Side Effects:
    - Sends data through a network socket.
    """
    try:
        # Generate random data
        data = generate_data(data_size)
        # Convert to numpy array and perform wavelet transform
        coeffs = pywt.wavedec(np.frombuffer(data, dtype=np.uint8), 'haar')
        # Serialize wavelet coefficients using pickle
        serialized_data = pickle.dumps(coeffs)
        # Send data to client
        client_socket.sendall(serialized_data)
        logging.info(f'Sent data of size: {len(serialized_data)} bytes')
    except Exception as e:
        logging.error(f'Error in generating or sending data: {e}')
        raise

def main():
    host = '0.0.0.0'  # Bind to all available interfaces
    port = 12345      # Port number for the server

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the server address
    try:
        server_socket.bind((host, port))
        logging.info(f'Server started and listening on {host}:{port}')
        server_socket.listen(5)

        while True:
            # Wait for a connection
            logging.info('Waiting for a connection')
            client_socket, addr = server_socket.accept()
            logging.info(f'Connection from {addr}')
            try:
                send_data(client_socket, 5)  # Sending 5MB of data; adjust as needed
            finally:
                client_socket.close()
                logging.info('Client connection closed')

    except socket.error as e:
        logging.error(f'Failed to bind or listen on {host}:{port}, error: {e}')
        raise
    finally:
        server_socket.close()
        logging.info('Server shutdown')

if __name__ == '__main__':
    main()
