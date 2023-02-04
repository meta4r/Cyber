import socket
import logging
import requests

def get_geolocation(ip_address):
    response = requests.get(f"http://api.ipstack.com/{ip_address}?access_key=your_api_key")
    location_data = response.json()
    country_name = location_data.get("country_name", "Unknown")
    region_name = location_data.get("region_name", "Unknown")
    city = location_data.get("city", "Unknown")
    return f"{city}, {region_name}, {country_name}"

def handle_connection(conn, addr):
    location = get_geolocation(addr[0])
    logging.info(f"[+] Connected by: {addr[0]}:{addr[1]} from {location}")
    conn.send(b"HTTP/1.0 200 OK\n\nWelcome to the honeypot!")
    data = conn.recv(1024)
    logging.info(f"[+] Data received: {data.decode()}")
    conn.close()

def honeypot():
    logging.basicConfig(filename='honeypot.log', level=logging.INFO, format='%(asctime)s %(message)s')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 80))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        handle_connection(conn, addr)

if __name__ == "__main__":
    honeypot()
