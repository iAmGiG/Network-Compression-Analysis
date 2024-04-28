import pywt
import numpy as np
import socket
import time
import os
import logging
import pickle  # Using pickle for serialization of complex objects

# Creates a 'logs' directory in the current working directory
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

server_log_file = os.path.join(log_dir, 'server.log')

# Set up logging
logging.basicConfig(filename=server_log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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
        print(f"Generating {data_size} MB of data.")
        logging.info(f"Generating {data_size} MB of data.")
        # Generate random data
        data = generate_data(data_size)
        # Convert to numpy array and perform wavelet transform
        coeffs = pywt.wavedec(np.frombuffer(data, dtype=np.uint8), 'haar')
        # Serialize wavelet coefficients using pickle
        serialized_data = pickle.dumps(coeffs)
        print(f"Sending {len(serialized_data)} bytes of compressed data.")
        logging.info(
            f"Sending {len(serialized_data)} bytes of compressed data.")
        # Send data to client
        total_sent = 0
        while total_sent < len(serialized_data):
            sent = client_socket.send(serialized_data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent
        print("Completed sending data.")
        logging.info("Completed sending data.")
    except Exception as e:
        logging.error(f'Error in generating or sending data: {e}')
        raise

def main():
    host = '127.0.0.1'  # Bind to all available interfaces
    port = 12345      # Port number for the server

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    # Bind the socket to the server address
    try:
        server_socket.bind((host, port))
        print(f'Server started and listening on {host}:{port}')
        logging.info(f'Server started and listening on {host}:{port}')
        server_socket.listen(5)

        while True:
            # Wait for a connection
            logging.info('Waiting for a connection')
            client_socket, addr = server_socket.accept()
            logging.info(f'Connection from {addr}')
            print(f'Connection from {addr}')
            try:
                # Receive data size request from the client
                data_size_str = client_socket.recv(1024).decode()
                data_size = int(data_size_str)
                # Send the requested data size
                send_data(client_socket, data_size)
            except socket.error as e:
                logging.error(f'Socket error occurred: {e}')
            finally:
                client_socket.close()
                print('Client connection closed')
                logging.info('Client connection closed')

    except socket.error as e:
        print(f'Failed to bind or listen on {host}:{port}, error: {e}')
        logging.error(f'Failed to bind or listen on {host}:{port}, error: {e}')
        raise
    finally:
        server_socket.close()
        logging.info('Server shutdown')


if __name__ == '__main__':
    main()
