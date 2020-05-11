import subprocess
from install import Logger


class Redis:
    def __init__(self):
        pass

    def start_redis(self):
        try:
            subprocess.run("sudo service redis start", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("启动redis失败")

    def stop_redis(self):
        try:
            subprocess.run("sudo service redis stop", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("停止redis失败")

    def restart_redis(self):
        try:
            subprocess.run("sudo service redis restart", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("重启redis失败")
