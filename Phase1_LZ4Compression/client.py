import socket
import time
import lz4.frame


def connect_to_server(host, port):
    """
    Establishes a TCP connection to a specified server using a socket.

    Parameters:
    - host (str): The hostname or IP address of the server to connect to.
    - port (int): The port number on the server to connect to.

    Returns:
    - socket.socket: A socket object that is connected to the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


def receive_and_decompress_data(client_socket):
    """
    Receives compressed data from the server and decompresses it using LZ4 compression.

    Parameters:
    - client_socket (socket.socket): The client socket through which data is received.

    Returns:
    - bytes: Decompressed data received from the server.
    """
    compressed_data = bytearray()
    while chunk := client_socket.recv(4096):
        compressed_data.extend(chunk)
    data = lz4.frame.decompress(compressed_data)
    return data


def main():
    """
    Main execution function for the client. Connects to the server, requests data, receives compressed data, decompresses it, and measures the time taken for these operations.

    Process:
    - Connects to the server and requests data of predetermined sizes.
    - Receives and decompresses the data.
    - Prints the size of the requested data, received data, and the time taken.
    """
    server_host = '0.0.0.0'
    server_port = 5000

    with connect_to_server(server_host, server_port) as client_socket:
        for data_size in [1, 10, 100]:  # Sizes in MB
            start_time = time.time()
            client_socket.sendall(str(data_size).encode('utf-8'))
            data = receive_and_decompress_data(client_socket)
            elapsed_time = time.time() - start_time
            print(
                f"Requested {data_size}MB: Received {len(data) / (1024 * 1024)}MB in {elapsed_time} seconds")


if __name__ == '__main__':
    main()
