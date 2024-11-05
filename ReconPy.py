from doctest import OutputChecker
import os
import re
import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
from threading import local

def Banner():
    print("""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝                                          
""")
   
def NetSlayerBanner():
    print("""
███╗   ██╗███████╗████████╗███████╗██╗      █████╗ ██╗   ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████╗██║     ███████║ ╚████╔╝ █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ███████║███████╗██║  ██║   ██║   ███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
""")
    
def Menu():
    print("1 - WiFi Recon")
    print("2 - Exit")
   
def GetLocalIPAddress():
    hostname = socket.gethostname()  # Cihazın adını alır
    local_ip = socket.gethostbyname(hostname)  # Hostname üzerinden IP adresini alır
    return local_ip

def PingAndDisplay(ip_address):
    response = os.system(f"ping -c 1 {ip_address} > /dev/null")
    if response == 0:
        print(f">>Cihaz Bulundu : IP - {ip_address}")
        
def DisplayConnectedDevices():
    print("\n>>Cihazların MAC Adreslerini bulunuyor...")

    if platform.system() == "Windows":
        command = ["C:\\Windows\\System32\\arp.exe", "-a"]
    elif platform.system() == "Linux":
        command = ["ip", "neighbor"]
    elif platform.system() == "Darwin":
        command = ["arp", "-a"]
    else:
        print("Unsupported OS")
        return

    try:
        # Komutu çalıştırma
        output = subprocess.run(command, capture_output=True, text=True, check=True).stdout

        # Çıktıyı işleme
        matches = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([\da-fA-F:-]+)", output)
        for match in matches:
            print(f">> IP Address: {match[0]}, MAC Address: {match[1]}")
    except FileNotFoundError:
        print(f">> Error: The command '{' '.join(command)}' was not found.")
    except subprocess.CalledProcessError as e:
        print(f">> Command failed with return code {e.returncode}. Output:\n{e.output}")
    except Exception as e:
        print(f">> An unexpected error occurred: {e}")

        
def main():
    while True:
        Banner()
        Menu()
        option = input(">>Enter Your Option : ")
        if option == "1":
            NetSlayerBanner()
            local_ip = GetLocalIPAddress()
            subnet = ".".join(local_ip.split(".")[:3]) + "."
            with ThreadPoolExecutor(max_workers=10) as executor:
                for i in range(1, 255):
                    ip = f"{subnet}{i}"
                    executor.submit(PingAndDisplay, ip)
            DisplayConnectedDevices()
        elif option == "2":
            break
        
if __name__ == "__main__":
    main()