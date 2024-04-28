
import socket
import logging
import lz4.frame
import time
import os

RECV_BUFFER_SIZE = 10 * 1024 * 1024  # 10 MB receive buffer

# Creates a 'logs' directory in the current working directory
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

client_log_file = os.path.join(log_dir, 'client.log')

logging.basicConfig(filename=client_log_file, level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        client_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUFFER_SIZE)
        # Set a timeout of 30 seconds for all socket operations
        client_socket.settimeout(30)
        client_socket.connect((host, port))
        # Optionally, receive an initial server acknowledgment if expected
        client_socket.recv(1024)
        return client_socket
    except socket.error as e:
        logging.error(f"Socket error during connection: {e}")
        # client_socket.close()  Ensure the socket is closed on error
        return None


def receive_and_decompress_data(client_socket):
    compressed_data = bytearray()
    chunk_size = 65536  # 64 KB
    try:
        while True:
            chunk = client_socket.recv(chunk_size)
            if not chunk:
                break
            compressed_data.extend(chunk)
        data = lz4.frame.decompress(compressed_data)
        client_socket.sendall(b'ack')
        return data
    except Exception as e:
        print(f"Reception error: {e}")
        logging.error(f"Reception error: {e}")
        return None


def main():
    server_host = '127.0.0.1'
    server_port = 5000

    try:
        client_socket = connect_to_server(server_host, server_port)
        if client_socket:
            with client_socket:
                for data_size in [1, 10, 100]:
                    logging.info(
                        f"Requesting {data_size}MB of data from the server.")
                    print(
                        f"Requesting {data_size}MB of data from the server.")
                    data_size_str = str(data_size).encode('utf-8')
                    client_socket.sendall(data_size_str)
                    start_time = time.time()
                    data = receive_and_decompress_data(client_socket)
                    elapsed_time = time.time() - start_time
                    if data is not None:
                        throughput = data_size / elapsed_time
                        logging.info(
                            f"Received {data_size}MB of data in {elapsed_time:.2f} seconds with throughput of {throughput:.2f}MB/s")
                        print(
                            f"Data Size: {data_size}MB, Time: {elapsed_time:.2f}s, Throughput: {throughput:.2f}MB/s")
                    else:
                        logging.info(
                            f"Failed to receive {data_size}MB of data.")
                        print(f"Failed to receive {data_size}MB of data.")
        else:
            logging.error("Failed to connect to the server.")
            print("Failed to connect to the server.")
    except KeyboardInterrupt:
        logging.info("Client shutdown requested by user.")
        print("Client shutdown requested by user.")
        if client_socket:
            client_socket.close()


if __name__ == '__main__':
    main()
