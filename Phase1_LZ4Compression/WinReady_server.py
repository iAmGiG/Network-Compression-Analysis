
import socket
import logging
import os
import lz4.frame
import time

SEND_BUFFER_SIZE = 10 * 1024 * 1024  # 10 MB send buffer

# Creates a 'logs' directory in the current working directory
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

server_log_file = os.path.join(log_dir, 'server.log')

logging.basicConfig(filename=server_log_file, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def generate_data(size_in_mb):
    return os.urandom(size_in_mb * 1024 * 1024)


def compress_data(data):
    return lz4.frame.compress(data)


def send_data(client_socket, data_size):
    try:
        logging.info(f"Generating {data_size}MB of data.")
        print(f"Generating {data_size}MB of data.")
        data = generate_data(data_size)
        compressed_data = compress_data(data)
        logging.info(
            f"Sending {len(compressed_data)} bytes of compressed data.")
        print(
            f"Sending {len(compressed_data)} bytes of compressed data.")
        client_socket.sendall(compressed_data)
        # Check if the connection is still open
        try:
            client_socket.send(b' ')  # Send a single byte
        except socket.error as e:
            logging.error(f"Connection closed unexpectedly: {e}")
            return
        client_socket.settimeout(120)  # Set a timeout of 120 seconds
        client_socket.recv(1024)  # Wait for acknowledgment
        time.sleep(1)
    except socket.error as e:
        logging.error(f"Error sending data: {e}")
        print(f"Error sending data: {e}")
    finally:
        logging.info("Completed sending data.")
        print("Completed sending data.")

def main():
    host = '0.0.0.0'
    port = 5000
    print(f"Server is running and listening on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)
        logging.info(f"Server listening on {host}:{port}")
        print(f"Server listening on {host}:{port}")

        try:
            while True:
                connection, client_address = server_socket.accept()
                with connection:
                    connection.setsockopt(
                        socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    logging.info(f"Connected by {client_address}")
                    print(f"Connected by {client_address}")
                    try:
                        message = connection.recv(4).decode('utf-8').strip()
                        data_size = int(message) 
                        send_data(connection, data_size)
                    except Exception as e:
                        logging.exception(
                            f"An error occurred with {client_address}: {e}")
                        print(
                            f"An error occurred with {client_address}: {e}")
                    finally:
                        connection.close()
        except KeyboardInterrupt:
            logging.info("Server shutdown requested by user.")
            print("Server shutdown requested by user.")


if __name__ == '__main__':
    main()
