import socket
from urllib.parse import urlparse

def http_client(url, port=80, save_file=True):
    """
    Client HTTP simple qui prend un lien complet ou un nom de domaine.
    """
    #  Extraire le host et la page depuis l'URL
    parsed_url = urlparse(url if "://" in url else "http://" + url)
    host = parsed_url.netloc
    page = parsed_url.path or "/"  # chemin par défaut "/"

    # Créer le socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except socket.gaierror:
        print(f"\n X Impossible de résoudre le nom de domaine '{host}'. Vérifiez l'orthographe ou l'existence du site.")
        return

    print("=============================================================================================")
    print(f"=> Connexion établie avec {host}:{port}")

    #  Préparer et envoyer la requête HTTP GET
    request = f"GET {page} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())
    print(f"=> Requête envoyée pour {page}")

    #  Recevoir la réponse
    response = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data
    client_socket.close()
    print("==> Connexion Reçue")

    #  Séparer headers et body
    headers, _, body = response.partition(b"\r\n\r\n")
    headers_text = headers.decode(errors="ignore")
    body_text = body.decode(errors="ignore")

    #  Affichage
    print("====================================== En-têtes HTTP ===========================================")
    print(headers_text)
    print("\n================================= Début du corps HTML ========================================")
    print(body_text[:500])

    #  Vérification code HTTP
    if "404" in headers_text:
        print("\n X 404 : Fichier non trouvé")
    elif "401" in headers_text:
        print("\n X 401 : Accès non autorisé")
    else:
        print("\n => Requête réussie")

    # Sauvegarder la page si c'est OK
    if save_file and "200 OK" in headers_text:
        filename = page.strip("/").replace("/", "_") or "index"
        filename += ".html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(body_text)
        print(f" => Page HTML sauvegardée dans '{filename}'")


if __name__ == "__main__":
    print("\n ==================================== Client HTTP simple =====================================")
    url = input("Entrez le lien complet ou le nom de domaine du site à consulter : ").strip()
    http_client(url)
