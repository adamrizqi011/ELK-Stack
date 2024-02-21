import socket
import logging

# Inisialisasi logger
logging.basicConfig(filename="active_ports.log", format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_active_ports():
    active_ports = []

    for port in range(1, 65535):
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_connection.settimeout(1)
        result = socket_connection.connect_ex(("localhost", port))
        if result == 0:
            active_ports.append(port)
        socket_connection.close()
    return active_ports

#if __name__ == "__main__":
   # active_ports = get_active_ports()
    #logger.info("Active ports: {}".format(active_ports))



active_ports = get_active_ports()
logger.info("Active ports: {}".format(active_ports))
print("Active ports: {}".format(active_ports))

#print(type(active_ports))

