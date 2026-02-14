from socket import *
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    host = "127.0.0.1"
    try:
        serverSocket.bind((host, port))
        print(f"Server successfully bound to {host}:{port}")
    except Exception as e:
        print(f"Error binding to port: {e}")
        return

    serverSocket.listen(1)
    print("The server is ready to receive connections...")

    while True:
        print('\nWaiting for a client...')
        connectionSocket, addr = serverSocket.accept()
        print(f"Accepted connection from: {addr}")

        try:
            message = connectionSocket.recv(1024).decode()

            if not message:
                connectionSocket.close()
                continue

            print(f"Request received: {message.splitlines()[0]}")

            filename = message.split()[1]

            f = open(filename[1:], "rb")

            file_content = f.read()
            f.close()

            header_line = "HTTP/1.1 200 OK\r\n"
            server_header = "Server: MyPythonServer\r\n"
            content_type = "Content-Type: text/html; charset=UTF-8\r\n"
            connection_header = "Connection: close\r\n"
            blank_line = "\r\n"

            response_headers = header_line + server_header + content_type + connection_header + blank_line

            connectionSocket.sendall(response_headers.encode() + file_content)

            print("File sent successfully.")

        except IOError:
            print("404 Error: File not found.")

            not_found_header = "HTTP/1.1 404 Not Found\r\n"
            content_type = "Content-Type: text/html\r\n"
            connection_header = "Connection: close\r\n"
            blank_line = "\r\n"

            error_body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The file you requested does not exist.</p></body></html>"

            response = not_found_header + content_type + connection_header + blank_line + error_body
            connectionSocket.sendall(response.encode())

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            connectionSocket.close()


if __name__ == "__main__":
    webServer(13331)