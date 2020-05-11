from install import BaseService, Logger
import subprocess


class UbuntuService(BaseService):
    def __init__(self):
        super().__init__()

    def get_python_version(self):
        super().get_python_version()

    def update_source_list(self):
        super().update_source_list()

    def upgrade_software(self):
        super().upgrade_software()

    # TODO:
    def change_apt_source(self):
        super().change_apt_source()

    # TODO:
    def install_java(self):
        try:
            subprocess.run("sudo apt-get install python-software-properties", shell=True, check=True)
            subprocess.run("sudo add-apt-repository ppa:webupd8team/java", shell=True, check=True)
            self.update_source_list()
            try:
                subprocess.run("sudo apt-get install oracle-java8-installer", shell=True, check=True)
                subprocess.run("java -version", shell=True)
            except subprocess.CalledProcessError:
                Logger.error("安装jdk失败")
        except subprocess.CalledProcessError:
            Logger.error("安装依赖失败")

    # TODO:
    def install_emqx(self):
        super().install_emqx()

    def install_mosquitto(self):
        Logger.info("准备安装Mosquitto Broker")
        try:
            subprocess.run("sudo apt install mosquitto mosquitto-clients", shell=True, check=True)
            mqtt_user_name = input("请输入MQTT用户名:")
            subprocess.run("sudo mosquitto_passwd -c /etc/mosquitto/passwd " + mqtt_user_name, shell=True, check=True)
            try:
                with open("/etc/mosquitto/conf.d/default.conf", "w+") as f:
                    f.write("allow_anonymous false\n"
                            "password_file /etc/mosquitto/pwfile\n"
                            "listener 1883\n")
                    Logger.info("写入MQTT配置成功!")
            except FileNotFoundError:
                Logger.error("未发现mqtt配置文件,请重新安装...")
        except subprocess.CalledProcessError:
            Logger.error("安装失败,请重新安装")
        finally:
            Logger.info("重启MQTT服务")
            subprocess.run("sudo systemctl restart mosquitto", shell=True, check=True)

    def install_ssh(self):
        try:
            Logger.info("开始安装ssh-server")
            subprocess.run("sudo apt install openssh-server", shell=True, check=True)

            try:
                Logger.info("启动ssh-server")
                subprocess.run("sudo /etc/init.d/ssh start", shell=True, check=True)
                Logger.info("写入自启配置")
                # 写入自启动配置
                with open("/etc/rc.local", 'a+') as f:
                    f.writelines('\n')
                    f.writelines('/etc/init.d/ssh start')
                Logger.info("自启配置写入成功")
            except subprocess.CalledProcessError:
                Logger.error("启动失败")

        except subprocess.CalledProcessError:
            Logger.error("安装失败,请重新安装")

    def install_redis(self):
        try:
            subprocess.run("sudo apt install redis-server", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("安装redis失败")

    def install_nginx(self):
        try:
            subprocess.run("sudo apt install nginx", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error("安装nginx失败")

