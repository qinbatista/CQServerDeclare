from math import fabs
import os
import time
import requests
import base64
import threading
import uuid
import subprocess
from socket import *
from datetime import datetime

class DDNSClient:
    def __init__(self):
        # self._fn_stdout = "/Users/qin/Desktop/ssr_out"
        # self._fn_tderr = "/Users/qin/Desktop/ssr_error"
        # self.__file_path = "/Users/qin/Desktop/log.txt"
        self._fn_stdout = "/root/ssr_out"
        self.__file_path = "/root/logs.txt"
        self._user_name = "kFpbr4qT6tYHCXCv"
        self._password = "q6Ss3kMSfKF5BngQ"
        self._my_domain = "cq.qinyupeng.com"
        self.__target_server = "us.qinyupeng.com"
        # https://domains.google.com/checkip banned by Chinese GFW
        self._get_ip_website = "https://checkip.amazonaws.com"
        self._can_connect = 0
        self.__canSend = False
        self.__ip = ""
    def _testServer(self):
        self.__log("_testServer")
        thread_refresh = threading.Thread(
            target=self._start, name="t1", args=())
        thread_refresh.start()

    def _start(self):
        while True:
            try:
                _get_static_ip_stdout = open(self._fn_stdout, 'w+')
                process = subprocess.Popen("ssr start", stdout=_get_static_ip_stdout,
                                           stderr=_get_static_ip_stdout, universal_newlines=True, shell=True)
                process.wait()
                with open(self._fn_stdout, 'r') as f:
                    error_result = f.readlines()
                self._can_connect = 0
                self.__log(" ")
                self.__log("--------Start SSR wait for 40 seconds---------")
                # self.__log(str("amazon" not in error_result)+" "+ str("Amazon" not in error_result))
                time.sleep(40)
                for result in error_result:
                    # self.__log(str("result")+" "+str(result))
                    if "amazon" in result or "Amazon" in result:
                        self._can_connect = 1
                        self.__post_ip_address()
                        self.__log("[Done] self._can_connect="+str(self._can_connect))
                        break
                if self._can_connect == 0:
                    self.__log("[Error] str(self._can_connect)="+str(self._can_connect))
                process = subprocess.Popen("ssr stop", stdout=_get_static_ip_stdout,
                                           stderr=_get_static_ip_stdout, universal_newlines=True, shell=True)
                process.wait()
                _get_static_ip_stdout.close()
                self.__canSend = True
                time.sleep(10)
                self.__log("-------------------End SSR--------------------")
                self.__log("  ")
                os.remove(self._fn_stdout)
            except Exception as e:
                self.__log("_start"+str(e))

    def _declare_alive(self):
        self.__log("declare alive thread start: version 1.0")
        thread_refresh = threading.Thread(
            target=self.__thread_declare_alive, name="t1", args=())
        thread_refresh.start()

    def __thread_declare_alive(self):
        udpClient = socket(AF_INET, SOCK_DGRAM)
        while True:
            try:
                # udpClient.sendto("cq".encode(encoding="utf-8"),("35.167.51.108",7171))
                if self.__canSend:
                    udpClient.sendto((gethostbyname(self.__target_server)+","+str(self._can_connect)).encode(encoding="utf-8"), (self.__target_server, 7171))
                    self.__canSend = False
                    self.__log("[Send] "+str(datetime.now())+" self._can_connect="+str(self._can_connect) +" cq IP="+self.__ip)
                # data, server = udpClient.recvfrom(4096)
                # ip = gethostbyname(self.__target_server)
                # print("thread_declare_alive:"+str(data)+","+str(ip))
                time.sleep(1)
            except Exception as e:
                # print("thread_declare_alive"+str(e))
                pass

    def __get_host_ip(self):
        self.__ip = ""
        try:
            self.__ip = requests.get(self._get_ip_website).text.strip()
        except Exception as e:
            # print("error when requesting ip"+str(e))
            pass
        return self.__ip

    def __post_ip_address(self):
        try:
            ip = self.__get_host_ip()
            self.__log("[my ip] "+ip)
            if ip =="":
                return
            _fn_stdout = "/root/ip_out"
            _get_static_ip_stdout = open(_fn_stdout, 'w+')
            command = "proxychains curl -i -H 'Authorization:Basic "+self.__base64()+"' -H 'User-Agent: google-ddns-updater email@yourdomain.com' https://" + \
                self._user_name+":"+self._password+"@domains.google.com/nic/update?hostname=" + \
                self._my_domain+" -d 'myip="+ip+"' > /dev/null"
            process = subprocess.Popen(command, stdout=_get_static_ip_stdout,
                                       stderr=_get_static_ip_stdout, universal_newlines=True, shell=True)
            # process = subprocess.Popen(command,universal_newlines=True, shell=True)
            process.wait()
            self.__log("[Get my ip]"+str(ip)+", wait for 10 seconds")
            _get_static_ip_stdout.close()
            time.sleep(10)
            os.remove(_fn_stdout)
        except Exception as e:
            self.__log("error when updating ip"+str(e))

    def __log(self, result):
        # if os.path.isfile(self.__file_path)==False:
        # with open(self.__file_path,"a+") as f:pass
        # print("key:key"+str(len(content)))
        with open(self.__file_path, "a+") as f:
            f.write(result+"\n")
        if os.path.getsize(self.__file_path) > 1024*128:
            with open(self.__file_path, "r") as f:
                content = f.readlines()
                # print("content:"+str(len(content)))
                os.remove(self.__file_path)

    def __base64(self):
        theString = self._user_name+":"+self._password
        encoded_string = base64.b64encode(theString.encode('ascii'))
        return encoded_string.decode('ascii')


if __name__ == '__main__':
    # os.system("ssr start")
    ss = DDNSClient()
    ss._declare_alive()
    # ss._testServer()
