from install import BaseService
from tools.logger import Logger
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

    # TODO: 还未做
    def change_apt_source(self):
        super().change_apt_source()

    # TODO: 下载测试
    def install_java(self):
        try:
            subprocess.run('https://github-production-release-asset-2e65be.s3.amazonaws.com/262994799/'
                           '8f9e0500-946f-11ea-9dfd-d6a2ba2d2804?X-Amz-Algorithm='
                           'AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20200512%2'
                           'Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20200512T084439Z&X-Amz-Expires'
                           '=300&X-Amz-Signature=f507010e6ebcbbca6253e6d20c20ea855dcc669c246fbe356'
                           'bee550e8d58d0bc&X-Amz-SignedHeaders=host&actor_id=35556811&repo_id=262994799'
                           '&response-content-disposition=attachment%3B%20filename%'
                           '3Djdk-8u231-linux-x64.tar.gz&response-content-type='
                           'application%2Foctet-stream', shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error('下载jdk8失败')
        # try:
        #     subprocess.run("sudo apt install python-software-common", shell=True, check=True)
        #     subprocess.run("sudo add-apt-repository ppa:webupd8team/java", shell=True, check=True)
        #     self.update_source_list()
        #     try:
        #         subprocess.run("sudo apt install oracle-java8-installer", shell=True, check=True)
        #         subprocess.run("java -version", shell=True)
        #     except subprocess.CalledProcessError:
        #         Logger.error("安装jdk失败")
        # except subprocess.CalledProcessError:
        #     Logger.error("安装依赖失败")

    def set_timezone(self):
        try:
            subprocess.run("timedatectl set-timezone Asia/Shanghai", shell=True, check=True)
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
