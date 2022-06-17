from flask import Flask, Response, render_template

import os, json, socket, threading

app = Flask(__name__)

filename = os.path.join(app.static_folder, "data.json")

@app.route("/")
def index():
    return render_template("index.html")
    
    """
    with open(filename) as file:
        data = json.load(file)
        
        print(data)
    return Response(json.dumps(data), mimetype="application/json")
    """
    
@app.route("/clients")
def connections():
    pass

def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8086))
    server.listen(1)

    print(f"listening on: (127.0.0.1:8086)\n\n\n")

    while True:
        connection, address = server.accept()

        print(f" address: {address} connected!")
        
        data = connection.recv(1024).decode()
    
        if data:
            print(data)
            with open(filename, "w") as file:
                json.dump(data, file)
        else:
            connection.close()

if __name__ == "__main__":
    thread = threading.Thread(target=socket_server, daemon=True).start()

    app.run(debug=True, host="127.0.0.1", port=8085, use_reloader=False)
