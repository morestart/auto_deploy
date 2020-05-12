# 控制台带颜色的打印类
class Logger:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[31m'
    END = '\033[0m'

    @staticmethod
    def info(info):
        try:
            print(Logger.OK + "[INFO]" + info + Logger.END)
        except UnicodeEncodeError:
            Logger.error("you must install chinese font!")

    @staticmethod
    def warn(info):
        try:
            print(Logger.WARNING + "[WARN]" + info + Logger.END)
        except UnicodeEncodeError:
            Logger.error("you must install chinese font!")

    @staticmethod
    def error(info):
        try:
            print(Logger.FAIL + "[ERR]" +info + Logger.END)
        except UnicodeEncodeError:
            Logger.error("you must install chinese font!")
