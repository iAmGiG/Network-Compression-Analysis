import socket
import time
import json
import lz4.frame
import logging

# Configure logging
logging.basicConfig(filename='client.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def connect_to_server(host, port):
    """
    Establishes a TCP connection to a specified server using a socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket


def receive_and_decompress_data(client_socket):
    """
    Receives compressed data from the server and decompresses it using LZ4 compression.
    """
    compressed_data = bytearray()
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        compressed_data.extend(chunk)
    # Check if the received data is sufficient for decompression
    try:
        data = lz4.frame.decompress(compressed_data)
        return data
    except RuntimeError as e:
        print(f"Decompression error: {e}")
        print(f"Received data size: {len(compressed_data)} bytes")
        return None


def main():
    """
    Main execution function for the client.
    """
    server_host = '172.17.0.2'
    server_port = 5000

    with connect_to_server(server_host, server_port) as client_socket:
        for data_size in [1, 10, 100]:  # Data sizes in MB
            logging.info(f"Requesting {data_size}MB of data from the server.")

            # Send request
            client_socket.sendall(str(data_size).encode('utf-8'))

            # Receive and decompress data
            start_time = time.time()
            data = receive_and_decompress_data(client_socket)
            elapsed_time = time.time() - start_time
            throughput = data_size / elapsed_time

            logging.info(
                f"Received {data_size}MB of data in {elapsed_time:.2f} seconds with throughput of {throughput:.2f}MB/s")

            # Output the result to the console
            print(
                f"Data Size: {data_size}MB, Time: {elapsed_time:.2f}s, Throughput: {throughput:.2f}MB/s")


if __name__ == '__main__':
    main()
