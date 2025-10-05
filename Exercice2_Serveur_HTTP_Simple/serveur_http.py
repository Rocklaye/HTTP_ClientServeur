import socket
import os

def http_server(host="127.0.0.1", port=8080):
    # Création du socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"=> Serveur HTTP lancé sur http://{host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f" ! Connexion depuis {addr}")

        # Réception de la requête HTTP
        request = client_socket.recv(1024).decode()
        print("=== Requête reçue ===")
        print(request)

        # Déterminer quel fichier a été demandé
        try:
            fichier = request.split(" ")[1][1:]  # récupère après le "/"
            if fichier == "":
                fichier = "index.html"
        except Exception:
            fichier = "index.html"

        # Vérifier si le fichier existe
        if os.path.exists(fichier):
            with open(fichier, "r", encoding="utf-8") as f:
                contenu = f.read()
            reponse = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + contenu
        else:
            reponse = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html\r\n\r\n" \
                      "<h1>401 - Not found</h1>"

        # Envoi de la réponse
        client_socket.sendall(reponse.encode())
        client_socket.close()

if __name__ == "__main__":
    http_server()
