from datetime import datetime
from time import sleep
import requests
import os
import docker

log_file = "/var/log/check_api.log"

def write_log(log):
    try:
        if not os.path.exists(log_file):
            with open(log_file, "w") as file:
                file.write("Datetime" + ": " + "log" + "\n")    
        now = datetime.now()
        with open(log_file, "+a") as file:
            file.write(str(now) + ": " + str(log) + '\n')
            file.close()
    except Exception as e:
        print(f"Falha ao gravar log {str(e)}")

def restart_container_docker(container_name: str):
    try:
        write_log(f"Reiniciando o container: {container_name}")
        print(f"Reiniciando o container: {container_name}")
        docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        result = docker_client.containers.get(container_name).restart()
        write_log(f"Resultado do restart: {result}")
        print(f"Resultado do restart: {result}")
    except Exception as e:
        write_log(f"Erro ao reiniciar o container: {container_name}")
        print(f"Erro ao reiniciar o container: {container_name}")
        exit(3)

def main():
    try:
        sites = []
        sites.append("http://httpstat.us/200?sleep=5000")
        sites.append("http://httpstat.us/403")
        sites.append("http://httpstat.us/500")
        for url in sites:
            sleep(30)
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                write_log(f"StatusCode: {response.status_code}! OK !")
                print(f"StatusCode: {response.status_code}! OK !")
            elif response.status_code == 400 or response.status_code == 403:
                write_log(f"StatusCode: {response.status_code}")
                print(f"StatusCode: {response.status_code}")
            else:
                write_log(f"Error: {response.status_code}")
                print(f"Error: {response.status_code}")
                restart_container_docker("jovial_kare")
    except Exception as e:
        exit(3)

if __name__ == '__main__':
    main()