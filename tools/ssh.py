import subprocess
import os
from tools.logger import Logger


class SSHServer:
    def __init__(self):
        ...

    def stop_ssh(self):
        try:
            subprocess.run("sudo /etc/init.d/ssh stop", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("停止失败")

    def start_ssh(self):
        try:
            subprocess.run("sudo /etc/init.d/ssh start", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("启动失败")

    def restart_ssh(self):
        try:
            subprocess.run("sudo /etc/init.d/sshresart", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("重启失败")
