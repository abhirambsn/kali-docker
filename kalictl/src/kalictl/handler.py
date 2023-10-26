import subprocess
from kalictl import config, ERRORS, SUCCESS, FILE_ERROR
from pathlib import Path
import docker
import tabulate
import colorama
import sys
import os

VALID_CONTAINERS = ['kali', 'kracker', 'penbuntu']

def get_colored_str(text: str, color: str) -> str:
    return getattr(colorama.Fore, color)+text+colorama.Fore.RESET

def setup_ssh_keys() -> int:
    current_user = os.getenv('USER')
    ssh_dir = Path.home() / '.ssh'
    try:
        if os.path.exists(ssh_dir):
            # Check if RSA keys exist or not
            if not os.path.exists(ssh_dir / 'id_rsa'):
                subprocess.check_output(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', f'{current_user}@localhost', '-N', '', '-f', str(ssh_dir / 'id_rsa')])
                # Chown 600 these keys
                subprocess.check_output(['chmod', '600', str(ssh_dir / 'id_rsa')], user=current_user)
                print(get_colored_str("Created RSA Key Pair", "GREEN"))
            # Copy the id_rsa file to .keys folder using copy, if .keys does not exist, create it
            dest_path = Path(__file__).parent.parent.parent.parent / '.keys'
            if not os.path.exists(dest_path):
                dest_path.mkdir()
                print(get_colored_str("[*] Created .keys folder", "LIGHTGREEN_EX"))
            subprocess.check_output(['cp', str(ssh_dir / 'id_rsa'), str(dest_path)])
            subprocess.check_output(['cp', str(ssh_dir / 'id_rsa.pub'), str(dest_path)])
            print(get_colored_str("Copied RSA Key Pair to .keys folder", "GREEN"))
        else:
            os.mkdir(ssh_dir)
            subprocess.check_output(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-C', f'{current_user}@localhost', '-N', '', '-f', str(ssh_dir / 'id_rsa')])
            subprocess.check_output(['chmod', '600', str(ssh_dir / 'id_rsa')], user=current_user)
            print(get_colored_str("Created RSA Key Pair", "GREEN"))
            subprocess.check_output(['cp', str(ssh_dir / 'id_rsa'), str(dest_path)])
            subprocess.check_output(['cp', str(ssh_dir / 'id_rsa.pub'), str(dest_path)])
            print(get_colored_str("Copied RSA Key Pair to .keys folder", "GREEN"))
        return SUCCESS
    except Exception as e:
        print(get_colored_str(f"[-] Failed to setup SSH Keys with error: {e}", "RED"))
        return FILE_ERROR


class DockerHandler:
    def __init__(self):
        self.states = {
            'running': 0,
            'paused': 1,
            'exited': 2,
            'dead': 3
        }

        self.client = docker.from_env()
        self.stack_state = self.states['running']
        self.username = config.get_config_entry('username')

        self.base_script_path = Path(__file__).parent.parent.parent.parent
    
    def get_ip_address(self, container_name: str) -> str:
        container = self.client.containers.get(container_name)
        return container.attrs['NetworkSettings']['Networks']['kali-net']['IPAddress']
    
    def build_stack(self, rebuild_if_exists = False):
        setup_ssh_key = setup_ssh_keys()
        if setup_ssh_key != SUCCESS:
            print(get_colored_str(f"[-] Failed to setup SSH Keys with error: {ERRORS[setup_ssh_key]}", "RED"))
            sys.exit(1)
        print(get_colored_str("[+] SSH Keys Setup Done.", "BLUE"))

        print(get_colored_str("[*] Building Kali Linux Image...", "CYAN"))
        kali_img = self.client.images.build(
            path = str(self.base_script_path / 'docker'),
            tag = 'kalictl/kali:latest',
            rm = True,
            dockerfile = 'Dockerfile.kali',
            buildargs = {
                'user': self.username,
                'group': self.username,
                'uid': '1000',
                'gid': '1000'
            },
            forcerm = True
        )

        print(get_colored_str(f"[+] Built Image of Kali Linux with tag: {kali_img[0].tags[0]}", "GREEN"))
        print(get_colored_str("[*] Building Kracker Box Image...", "CYAN"))

        kracker_img = self.client.images.build(
            path = str(self.base_script_path / 'docker'),
            tag = 'kalictl/kracker:latest',
            rm = True,
            dockerfile = 'Dockerfile.kracker',
            forcerm = True
        )

        print(get_colored_str(f"[+] Built Image of Kracker Box with tag: {kracker_img[0].tags[0]}", "GREEN"))
        print(get_colored_str("[*] Building Penbuntu Image...", "CYAN"))

        penbuntu_img = self.client.images.build(
            path = str(self.base_script_path / 'docker'),
            tag = 'kalictl/penbuntu:latest',
            rm = True,
            dockerfile = 'Dockerfile.penbuntu',
            buildargs = {
                'user': self.username
            },
            forcerm = True
        )

        print(get_colored_str(f"[+] Built Image of Penbuntu with tag: {penbuntu_img[0].tags[0]}", "GREEN"))

    def start_stack(self, ignore_if_running = True):
        op = subprocess.check_output(['docker', 'compose', 'up', '-d'], cwd=self.base_script_path)
        print(op.decode())

    def stop_stack(self, ignore_if_stopped = True):
        op = subprocess.check_output(['docker', 'compose', 'stop'], cwd=self.base_script_path)
        print(op.decode())

    def restart_stack(self):
        op = subprocess.check_output(['docker', 'compose', 'restart'], cwd=self.base_script_path)
        print(op.decode())
        print(get_colored_str("Restarted Stack", "GREEN"))

    def copy_to_stack(self, src_path: str, dest_path: str, container_name: str = "kali") -> bool:
        if container_name not in VALID_CONTAINERS:
            raise ValueError(f'Invalid container name "{container_name}"')
        op = subprocess.check_output(['docker', 'compose', 'cp', src_path, f'{container_name}:{dest_path}'], cwd=self.base_script_path)
        print(op.decode())
        print(get_colored_str(f"Copied {src_path} to {dest_path} on {container_name}", "GREEN"))

    def copy_from_stack(self, src_path: str, dest_path: str, container_name: str = "kali") -> bool:
        if container_name not in VALID_CONTAINERS:
            raise ValueError(f'Invalid container name "{container_name}"')
        op = subprocess.check_output(['docker', 'compose', 'cp', f'{container_name}:{src_path}', dest_path], cwd=self.base_script_path)
        print(op.decode())
        print(get_colored_str(f"Copied {src_path} from {container_name} to {dest_path}", "GREEN"))

    def exec_in_stack(self, command: str, container_name="kali") -> bool:
        if container_name not in VALID_CONTAINERS:
            raise ValueError(f'Invalid container name "{container_name}"')
        blacklist = [';', '--', '&&', '|', '||', '`', '$', '(', ')', '>', '<']
        if any(i in command for i in blacklist) or not self.username.isalnum():
            print(get_colored_str("[-] Invalid command", "RED"))
            return False
        cmd = f'docker compose exec -u {self.username} -it {container_name} {command}'
        try:
            os.system(cmd)
            return True
        except Exception as e:
            print(get_colored_str(f"[-] Failed to execute command with error: {e}", "RED"))
            return False

    def get_stack_state(self) -> None:
        op = subprocess.check_output(['docker', 'compose', 'ps', '--format', '{{.Names}},{{.Service}},{{.Status}},{{.Ports}}', '-a'], cwd=self.base_script_path, text=True)
        op = op.split('\n')
        lines = [line.split(',') for line in op][:-1]
        parsed_lines = [
            {
                'name': line[0], 
                'service': line[1], 
                'status': line[2].split()[0], 
                'ports': '-' if ''.join(line[3:]) == '' else ' '.join(line[3:]), 
                'time': ' '.join(line[2].split()[1:])
            }
        for line in lines]
        data = [
            {
                'name': get_colored_str(line['service'], "GREEN"), 
                'status': get_colored_str("Running", "GREEN") if "Up" in line['status'] else get_colored_str("Stopped", "RED"), 
                'ports': get_colored_str(line['ports'] if "Up" in line['status'] else "Not Available", "CYAN"), 
                'ip': get_colored_str(self.get_ip_address(line['name']) if "Up" in line['status'] else "Not Available", "LIGHTBLUE_EX"), 
                'time': get_colored_str(line['time'] if "Up" in line['status'] else ' '.join(line['time'].split()[1:]), "LIGHTMAGENTA_EX")
            } 
        for line in parsed_lines]

        headers = [
            "Container Name", 
            "Status", 
            "Internal IP Address", 
            "Ports", 
            "Uptime" if "Up" in parsed_lines[0]['status'] else "Stopped Since"
        ]
        print(tabulate.tabulate([i.values() for i in data], tablefmt="pretty", headers=headers))   
