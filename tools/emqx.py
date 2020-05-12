import subprocess
from tools.logger import Logger


class EMQX:
    def __init__(self):
        ...

    def start_emqx(self):
        try:
            subprocess.run("sudo emqx start", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error('启动失败')

    def stop_emqx(self):
        try:
            subprocess.run("sudo emqx stop", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error('停止失败')

    def restart_emqx(self):
        try:
            subprocess.run("sudo emqx restart", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error('重启失败')

    def get_emq_status(self):
        try:
            subprocess.run("sudo emqx_ctl status", shell=True, check=True)
        except subprocess.CalledProcessError:
            Logger.error('查询状态失败')

    def emqx_config_explain(self):
        Logger.info("配置路径:")
        Logger.info("/etc/emqx")
        Logger.info("取消匿名访问模式:")
        Logger.info("使用sudo nano /etc/emqx/emqx.conf 编辑配置文件,将allow_anonymous设置为false, ctrl o保存")
        Logger.info("鉴权设置:")
        Logger.info("使用此命令编辑sudo nano /etc/emqx/etc/plugins/emqx_auth_username.conf, "
                    "注释掉现有内容, 打开auth.user.1的用户名和密码")
        Logger.warn("在启动鉴权时,请先在dashboard中启动鉴权插件")
