FROM debian:10-slim
#add file
ADD * ./
ADD shadowsocksr /root/.local/shadowsocksr
WORKDIR /root/.local/shadowsocksr
RUN bash initcfg.sh
WORKDIR /

#install packages
RUN apt-get update
RUN apt-get -y install vim git tar iputils-ping libsodium23 wget sudo curl proxychains python python-pip

#update pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#install ssr
RUN chmod +x ./ssr
RUN mv ./ssr /usr/local/sbin/
RUN ssr install

#set config
COPY configus.json /etc/shadowsocks.json
COPY proxychains.conf /etc/proxychains.conf

WORKDIR /root
CMD ["python","/cq_qinyupeng_com_client.py"]
