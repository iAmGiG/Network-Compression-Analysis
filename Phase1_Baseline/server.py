import socket
import time
import os

# Function to generate a data packet of a specific size

"""
1. Server Socket Setup: The script sets up a server that listens on TCP port 5000 for incoming connections.

2. Data Generation: The generate_data function creates a data packet of the desired size using os.urandom, 
which generates a string of random bytes.

3. Sending Data: The send_data function sends the entire data packet to the client in one go using sendall.

4. Main Loop: The server listens for connections, accepts them, and based on the client's request, 
sends the appropriate size data packet and then closes the connection.
"""


def generate_data(size_in_mb):
    """Generates a binary string that roughly corresponds to the desired size in MB"""
    return os.urandom(size_in_mb * 1024 * 1024)

# Function to send data packets


def send_data(client_socket, data_size):
    """
    sends the data to the client
    """
    data = generate_data(data_size)
    client_socket.sendall(data)


def main():
    """
    The baseline main.
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
