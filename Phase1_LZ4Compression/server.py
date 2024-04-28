import time
import socket
import os
import lz4.frame
import logging

# Set up logging
logging.basicConfig(filename='server.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


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
    try:
        logging.info(f"Generating {data_size}MB of data.")
        data = generate_data(data_size)
        compressed_data = compress_data(data)
        logging.info(
            f"Sending {len(compressed_data)} bytes of compressed data.")
        client_socket.sendall(compressed_data)
        # Wait for the client to confirm data reception
        # Assuming the client sends back a simple "ack"
        client_socket.recv(1024)
        # Wait for a second before considering closing the connection (for testing)
        time.sleep(1)
    except socket.error as e:
        logging.error(f"Error sending data: {e}")
    finally:
        logging.info("Completed sending data.")


def main():
    """
    Main server function that sets up a server socket, listens for connections, and serves compressed data requests.

    Process:
    - Sets up the server socket and listens on a specific port.
    - Accepts connections, receives data size requests from clients, generates the requested size of data, compresses it, and sends the compressed data back to the client.
    """
    host = '172.17.0.2'
    port = 5000
    print(f"Server is running and listening on port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        logging.info(f"Server listening on port {port}")

        while True:
            connection, client_address = server_socket.accept()
            with connection:
                logging.info(f"Connected by {client_address}")
                try:
                    message = connection.recv(16).decode('utf-8')
                    data_size = int(message)
                    send_data(connection, data_size)
                except Exception as e:
                    logging.exception(
                        f"An error occurred with {client_address}: {e}")
                finally:
                    connection.close()


if __name__ == '__main__':
    main()
