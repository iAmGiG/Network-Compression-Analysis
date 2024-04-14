import socket
import os
import lz4.frame

def generate_data(size_in_mb):
    """
    Generates a binary string of random bytes approximately equal to the specified size in megabytes.

    Parameters:
    - size_in_mb (int): The size of the data to generate in megabytes.

    Returns:
    - bytes: A bytes object containing random data of the specified size.
    """
    return os.urandom(size_in_mb * 1024 * 1024)

def compress_data(data):
    """
    Compresses data using LZ4 compression algorithm.

    Parameters:
    - data (bytes): The data to compress.

    Returns:
    - bytes: The compressed data.
    """
    return lz4.frame.compress(data)

def send_data(client_socket, data_size):
    """
    Generates data of the specified size, compresses it, and sends it to the client.

    Parameters:
    - client_socket (socket.socket): The client socket to send data to.
    - data_size (int): The size of the data to generate and send in megabytes.

    Side Effects:
    - Sends compressed data through the socket.
    """
    data = generate_data(data_size)
    compressed_data = compress_data(data)
    client_socket.sendall(compressed_data)

def main():
    """
    Main server function that sets up a server socket, listens for connections, and serves compressed data requests.

    Process:
    - Sets up the server socket and listens on a specific port.
    - Accepts connections, receives data size requests from clients, generates the requested size of data, compresses it, and sends the compressed data back to the client.
    """
    host = '0.0.0.0'
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        while True:
            connection, client_address = server_socket.accept()
            with connection:
                print('Connected by', client_address)
                message = connection.recv(16).decode('utf-8')
                data_size = int(message)
                send_data(connection, data_size)

if __name__ == '__main__':
    main()
