import socket
import os
import lz4.frame

def generate_data(size_in_mb):
    # Generates a binary string that roughly corresponds to the desired size in MB
    return os.urandom(size_in_mb * 1024 * 1024)

def compress_data(data):
    return lz4.frame.compress(data)

def send_data(client_socket, data_size):
    data = generate_data(data_size)
    compressed_data = compress_data(data)
    client_socket.sendall(compressed_data)

def main():
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
