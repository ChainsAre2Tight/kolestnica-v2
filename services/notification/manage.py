

import sys
sys.path.append('./application/')


from notification_server import socket, app


if __name__ == "__main__":
    socket.run(app, port=5030, debug=True)
