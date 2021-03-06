from install import BaseService
from tools.logger import Logger
import subprocess
import os


class UbuntuService(BaseService):
    def __init__(self):
        super().__init__()

    def get_python_version(self):
        super().get_python_version()

    def update_source_list(self):
        super().update_source_list()

    def upgrade_software(self):
        super().upgrade_software()

    # TODO: upgrade_python3
    def upgrade_python3(self):
        self.get_python_version()
        Logger.warn('暂不支持, 请等待后续支持')

    # TODO: install_docker
    def install_docker(self):
        Logger.warn('暂不支持, 请等待后续支持')

    def change_apt_source(self):
        Logger.info('备份系统源')
        subprocess.run('cp /etc/apt/sources.list /etc/apt/sources.list.bak', shell=True)
        with open('/etc/apt/sources.list', 'w+') as f:
            f.writelines(
                """
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
            """)

    def install_java(self):
        try:
            # 文件存在不需要重复下载
            if os.path.exists('jdk-8u231-linux-x64.tar.gz'):
                subprocess.run('sudo mkdir /usr/lib/jvm', shell=True, check=True)
                subprocess.run('sudo tar -zxvf jdk-8u231-linux-x64.tar.gz -C /usr/lib/jvm')
            else:
                Logger.info('开始下载jdk8')
                subprocess.run('sudo wget https://github.com/morestart/auto_deploy/releases/download/1.0/jdk-8u231'
                               '-linux-x64.tar.gz', shell=True, check=True)
                subprocess.run('sudo mkdir /usr/lib/jvm', shell=True, check=True)
                subprocess.run('sudo tar -zxvf jdk-8u231-linux-x64.tar.gz -C /usr/lib/jvm')

                with open('sudo nano ~/.bashrc', 'a+') as f:
                    f.writelines('\n')
                    f.writelines('export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_231')
                    f.writelines('\n')
                    f.writelines('export JRE_HOME=${JAVA_HOME}/jre')
                    f.writelines('\n')
                    f.writelines('export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib')
                    f.writelines('\n')
                    f.writelines('export PATH=${JAVA_HOME}/bin:$PATH')
                subprocess.run('source ~/.bashrc', shell=True)
                subprocess.run('sudo update-alternatives --install /usr/bin/java java '
                               '/usr/lib/jvm/jdk1.8.0_231/bin/java 300', shell=True)
                subprocess.run('java -version', shell=True)

        except subprocess.CalledProcessError:
            Logger.error('下载jdk8失败')

    def set_timezone(self):
        try:
            Logger.info("开始设置中国时区")
            subprocess.run("timedatectl set-timezone Asia/Shanghai", shell=True, check=True)
            subprocess.run("date -R", shell=True)
        except subprocess.CalledProcessError:
            Logger.error("时区设置错误")

    def install_emqx(self):
        try:
            Logger.info("开始安装EMQ依赖")
            subprocess.run("sudo apt update && sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common", shell=True, check=True)
            try:
                Logger.info('添加GPG秘钥')
                subprocess.run("curl -fsSL https://repos.emqx.io/gpg.pub | sudo apt-key add -", shell=True, check=True)
                try:
                    command = "sudo add-apt-repository \
    \"deb [arch=amd64] https://repos.emqx.io/emqx-ce/deb/ubuntu/ \
    ./$(lsb_release -cs) \
    stable\""
                    subprocess.run(command, shell=True, check=True)
                    self.update_source_list()
                    Logger.info("查询EMQ的可用版本")
                    subprocess.run("sudo apt-cache madison emqx", shell=True)
                    version = input("请输入需要的版本号,默认为最新版本(可直接回车)>")
                    if version == '':
                        try:
                            subprocess.run("sudo apt install emqx", shell=True, check=True)
                        except subprocess.CalledProcessError:
                            Logger.error('安装EMQ失败,请重试')
                    else:
                        try:
                            subprocess.run("sudo apt install emqx={}".format(version), shell=True, check=True)
                            Logger.info('安装完成')
                            get_better = input("是否调优?(y or n, default is y)>")
                            if get_better == '':
                                subprocess.run("sudo sysctl -w fs.file-max=2097152", shell=True)
                                subprocess.run("sudo sysctl -w fs.nr_open=2097152", shell=True)
                                subprocess.run("sudo echo 2097152 > /proc/sys/fs/nr_open", shell=True)
                                subprocess.run("ulimit -n 1048576", shell=True)
                                with open('/etc/sysctl.conf', 'a+') as f:
                                    f.writelines('\n')
                                    f.writelines("fs.file-max = 1048576")

                                with open("/etc/systemd/system.conf", 'a+') as f:
                                    f.writelines('\n')
                                    f.writelines("DefaultLimitNOFILE=1048576")

                                with open("/etc/security/limits.conf", "a+") as f:
                                    f.writelines('\n')
                                    f.writelines('*      soft   nofile      1048576')
                                    f.writelines('\n')
                                    f.writelines('*      hard   nofile      1048576')
                                subprocess.run('sysctl -w net.core.somaxconn=32768', shell=True)
                                subprocess.run('sysctl -w net.ipv4.tcp_max_syn_backlog=16384', shell=True)
                                subprocess.run('sysctl -w net.core.netdev_max_backlog=16384', shell=True)
                                subprocess.run('sysctl -w net.ipv4.ip_local_port_range=\'1000 65535\'', shell=True)
                                subprocess.run('sysctl -w net.core.rmem_default=262144', shell=True)
                                subprocess.run('sysctl -w net.core.wmem_default=262144', shell=True)
                                subprocess.run('sysctl -w net.core.rmem_max=16777216', shell=True)
                                subprocess.run('sysctl -w net.core.wmem_max=16777216', shell=True)
                                subprocess.run('sysctl -w net.core.optmem_max=16777216', shell=True)
                                subprocess.run('sysctl -w net.ipv4.tcp_rmem=\'1024 4096 16777216\'', shell=True)
                                subprocess.run('sysctl -w net.ipv4.tcp_wmem=\'1024 4096 16777216\'', shell=True)
                                subprocess.run('sysctl -w net.nf_conntrack_max=1000000', shell=True)
                                subprocess.run('sysctl -w net.netfilter.nf_conntrack_max=1000000', shell=True)
                                subprocess.run('sysctl -w net.netfilter.nf_conntrack_tcp_timeout_time_wait=30',
                                               shell=True)
                                subprocess.run('sysctl -w net.ipv4.tcp_max_tw_buckets=1048576', shell=True)
                                subprocess.run('sysctl -w net.ipv4.tcp_fin_timeout=15', shell=True)

                                with open('/etc/emqx/etc/emqx.conf', 'a+') as f:
                                    f.writelines('\n')
                                    f.writelines('node.process_limit = 2097152')
                                    f.writelines('\n')
                                    f.writelines('node.max_ports = 1048576')

                                Logger.info('请手动配置TCP监听器的 Acceptor 池大小')
                                Logger.info('sudo nano /etc/emqx/etc/emqx.conf')
                                Logger.info('修改 listener.tcp.external.acceptors = 64')

                        except subprocess.CalledProcessError:
                            Logger.error('安装{}版本EMQ失败,请尝试其他版本'.format(version))
                except subprocess.CalledProcessError:
                    Logger.error('添加stable仓库失败')
            except subprocess.CalledProcessError:
                Logger.error('添加秘钥失败')
        except subprocess.CalledProcessError:
            Logger.error('安装依赖失败,请重试')

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
