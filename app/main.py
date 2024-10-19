from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

##get the path of this file
import os
current_path = os.path.dirname(os.path.realpath(__file__))


class Map:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def setname(self, name):
        self.name = name

    def setpath(self, path):
        self.path = path

    def getname(self):
        return self.name
    
    def getpath(self):
        return self.path


map = Map("","")


# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/setmap', methods=['POST'])
def handle_setmap():
    # Get the posted json data in example form {"name":"map1"}
    currmap = request.get_json()
    print(currmap)
    
    if currmap:
        # Broadcast the message to all connected WebSocket clients
        ##save the map
        map.setname(currmap)
        socketio.emit('new_map', currmap)
        return 'Map broadcasted!\n', 200
    else:
        return 'No map received!\n', 400


@app.route('/getmap', methods=['GET'])
def handle_getmap():
    if map.getname():
        return map.getname() + '\n', 200
    else:
        return 'No map received!\n', 400

@app.route('/setplayers', methods=['POST'])
def handle_setplayers():
    # Get the posted json data in example form {"players":{"idiot1":[-1780.55, -660.03],"idiot2":[-1265.88, 720.96]}}
    
    players = request.get_json()

    print(players)



    if players:
        # Broadcast the message to all connected WebSocket clients
        socketio.emit('new_players', players['players'])
        return 'Players broadcasted!\n', 200
    else:
        return 'No players received!\n', 400


# WebSocket connection handler
@socketio.on('connect')
def handle_connect():
    print('Client connected!')

# WebSocket disconnection handler
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000)
