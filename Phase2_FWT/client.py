import socket
import time
import pywt
import numpy as np

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
    # Send data request to server
    client_socket.sendall(str(data_size).encode('utf-8'))

    # Start the timer
    start_time = time.time()

    received_data = []
    while True:
        # Receive data in chunks
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        received_data.append(chunk)

    # Stop the timer
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Decompress the received data
    compressed_data = b''.join(received_data)
    coeffs = [np.frombuffer(c, dtype='uint8') for c in np.split(
        compressed_data, np.array([len(c) for c in compressed_data.split(b'\x00')])[:-1])]
    decompressed_data = pywt.waverec(coeffs, 'haar')

    return decompressed_data, elapsed_time


def main():
    """
    runs the show
    """
    server_host = '0.0.0.0'
    server_port = 5000

    client_socket = connect_to_server(server_host, server_port)

    try:
        for data_size in [1, 10, 100]:  # Data sizes in MB
            decompressed_data, elapsed_time = request_and_receive_data(client_socket, data_size)
            decompressed_size = len(decompressed_data) / (1024 * 1024)  # Size in MB
            print(f"Requested {data_size}MB: Received {decompressed_size}MB in {elapsed_time} sec")

    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
