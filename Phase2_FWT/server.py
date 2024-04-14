import pywt
import numpy as np
import socket
import time
import os


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
    and sends the compressed data to the client.

    Parameters:
    - client_socket (socket.socket): The client socket to send data to.
    - data_size (int): The size of the data to generate and send in megabytes.

    Process:
    - The data is first converted to a numpy array.
    - A wavelet decomposition is performed on the array.
    - The wavelet coefficients are serialized and sent over the socket.

    Side Effects:
    - Sends compressed data through the socket.
    """
    data = generate_data(data_size)

    # Convert binary data to numpy array
    data_array = np.frombuffer(data, dtype='uint8')

    # Apply FWT compression
    coeffs = pywt.wavedec(data_array, 'haar', level=3)
    compressed_data = np.array([np.array(c).tobytes() for c in coeffs])

    # Send the compressed data
    client_socket.sendall(compressed_data)


def main():
    """
    Main server function that sets up a server socket, listens for connections, 
    and serves compressed data requests.

    Process:
    - Sets up the server socket and listens on a specified port.
    - Accepts connections and handles incoming data size requests from clients.
    - Generates the requested size of data, compresses it using wavelet transforms, 
    and sends the compressed data back to the client.
    """
    host = '0.0.0.0'
    port = 5000

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_socket.bind((host, port))
    print(f"Server is running on port {port}")

    # Listen for incoming connections
    server_socket.listen(5)

    try:
        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = server_socket.accept()
            print('connection from', client_address)

            try:
                # Receive the message from the client
                message = connection.recv(16).decode('utf-8')
                # Assuming the client sends the size as a string
                data_size = int(message)
                print(f"Requested data size: {data_size}MB")

                # Send the data
                send_data(connection, data_size)
            finally:
                # Clean up the connection
                connection.close()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server_socket.close()


if __name__ == '__main__':
    main()
