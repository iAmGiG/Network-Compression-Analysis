import socket
import time
import lz4.frame

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def receive_and_decompress_data(client_socket):
    compressed_data = bytearray()
    while chunk := client_socket.recv(4096):
        compressed_data.extend(chunk)
    data = lz4.frame.decompress(compressed_data)
    return data

def main():
    server_host = 'localhost'  # Change to your server IP if not local
    server_port = 5000

    with connect_to_server(server_host, server_port) as client_socket:
        for data_size in [1, 10, 100]:  # Sizes in MB
            start_time = time.time()
            client_socket.sendall(str(data_size).encode('utf-8'))
            data = receive_and_decompress_data(client_socket)
            elapsed_time = time.time() - start_time
            print(f"Requested {data_size}MB: Received {len(data) / (1024 * 1024)}MB in {elapsed_time} seconds")

if __name__ == '__main__':
    main()
