try:
    from pick import pick
    import platform
    from tools.logger import Logger
    from system.ubuntu import UbuntuService
    import subprocess
except ImportError:
    import subprocess
    subprocess.run('sudo apt install pip3', shell=True)
    subprocess.run('sudo pip3 install pick', shell=True)
    from pick import pick
    import platform
    from tools.logger import Logger
    from system.ubuntu import UbuntuService


class Menu:
    def __init__(self):
        self.os_name = platform.system()
        self.main_title = "励图{}环境安装工具 v0.1".format(self.os_name)
        # self.main_options = ["💼 环境安装", "👀 工具使用", "🏃 退出"]
        self.main_options = ["环境安装", "工具使用", "退出"]
        self.subtitle = "========系统环境配置========"
        self.sub_options = ["更新Python3", "更新软件包列表", "更新系统软件包",
                            "更换系统apt源", "设置时区",
                            "安装JDK8", "安装emqx", "安装mosquitto",
                            "安装ssh", "安装docker", "安装redis", "安装nginx", "返回主菜单"]

    def show_menu(self):
        exit_code = True
        # while exit_code:
        option, index = pick(self.main_options, self.main_title)
        if option == "环境安装":
            # 进入二级菜单
            option, index = pick(self.sub_options, self.subtitle)
            # 返回主菜单
            if option == "返回主菜单":
                pick(self.main_options, self.main_title)
            else:
                # 其他命令使用install函数安装
                self.install(option)
        elif option == "退出":
            exit(0)
        elif option == "工具使用":
            print('工具使用')

    def install(self, command: str):
        if self.os_name == 'Windows':
            Logger.warn('暂不支持此系统')
        elif self.os_name == "Linux":
            out = subprocess.check_output("cat /etc/os-release", shell=True)
            out = out.decode("utf-8").split('\n')
            # 判断系统为ubuntu1804
            if "VERSION_ID=\"18.04\"" in out and "NAME=\"Ubuntu\"" in out:
                if command == "更新Python3":
                    UbuntuService().upgrade_python3()
                elif command == "更新软件包列表":
                    UbuntuService().update_source_list()
                elif command == "更新系统软件包":
                    UbuntuService().upgrade_software()
                elif command == "更换系统apt源":
                    UbuntuService().change_apt_source()
                elif command == "设置时区":
                    UbuntuService().set_timezone()
                elif command == "安装JDK8":
                    UbuntuService().install_java()
                elif command == "安装emqx":
                    UbuntuService().install_emqx()
                elif command == "安装mosquitto":
                    UbuntuService().install_mosquitto()
                elif command == "安装ssh":
                    UbuntuService().install_ssh()
                elif command == "安装docker":
                    UbuntuService().install_docker()
                elif command == "安装redis":
                    UbuntuService().install_redis()
                elif command == "安装nginx":
                    UbuntuService().install_nginx()
            # TODO: 其他系统
            else:
                Logger.warn('暂不支持当前系统')
        else:
            Logger.warn('暂不支持当前系统')

    # TODO:
    def tools_use(self, command: str):
        ...
