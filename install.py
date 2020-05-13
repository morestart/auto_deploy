import getopt
import subprocess
import sys
import time
import os
from pathlib import Path
from tools.logger import Logger
# import getpass


# 获取当前登录的用户名
# username = getpass.getuser()


# 公共服务
class BaseService:
    def __init__(self):
        # self.username = username
        ...

    # 获取当前的Python版本
    def get_python_version(self):
        try:
            Logger.info("Python3版本")
            subprocess.run("python3 -V", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("没有找到Python3")

        try:
            Logger.info("Python2版本")
            subprocess.run("python2 -V", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("没有找到Python2")

    # 更新python3版本
    def upgrade_python3(self):
        return

    # 更新软件源, apt 工具仅针对ubuntu debian系, 其他linux发行版需要重写该方法
    def update_source_list(self):
        Logger.info("准备更新软件包列表")
        try:
            subprocess.run("sudo apt update", shell=True, check=True)
            Logger.info("软件包列表更新完毕")
            Logger.info("是否更新软件(y or n, default: n)")
            confirm = input("(不输入可直接回车使用默认值)>")
            if confirm == "y" or confirm == "Y":
                self.upgrade_software()
        except subprocess.CalledProcessError:
            Logger.error("更新失败")

    # 更新软件, apt 工具仅针对ubuntu debian系, 其他linux发行版需要重写该方法
    def upgrade_software(self):
        try:
            subprocess.run("sudo apt-get upgrade", shell=True, check=True)
            Logger.info("更新软件完毕")
        except subprocess.CalledProcessError:
            Logger.error("更新失败")

    # 安装jdk环境
    def install_java(self):
        return

    # 安装emq通信服务
    def install_emqx(self):
        return

    # 安装Mosquitto通信服务器(可作为临时使用,最大并发10w+)
    def install_mosquitto(self):
        return

    # 安装ssh服务
    def install_ssh(self):
        return

    # 安装docker
    def install_docker(self):
        return

    # 安装redis
    def install_redis(self):
        return

    # 安装nginx
    def install_nginx(self):
        return

    # 更改apt源
    def change_apt_source(self):
        return

    # 设置时区
    def set_timezone(self):
        return


class Install:
    def __init__(self, system_info: str):
        self.os_name = system_info

    def help_info(self):
        ...

    def install(self):
        if self.os_name == 'Windows':
            Logger.warn('暂不支持此系统')
        elif self.os_name == "Linux":
            out = subprocess.check_output("cat /etc/os-release", shell=True)
            out = out.decode("utf-8").split('\n')
            # 判断系统为ubuntu1804
            if "VERSION_ID=\"18.04\"" in out and "NAME=\"Ubuntu\"" in out:
                ...
            else:
                Logger.warn('暂不支持当前版本的ubuntu')


if __name__ == '__main__':
    # TODO: 执行前需要先调用更新软件包列表服务
    import system.ubuntu as ubuntu
    import platform
    system = platform.system()
    from menu.menu import Menu
    try:
        Menu().show_menu()
    except PermissionError:
        Logger.error('请使用sudo/root权限运行本程序')
