FROM manjarolinux/build:latest

ADD . /home/endpoint
WORKDIR /home/endpoint

RUN yes | pacman -Syu python-pip git mariadb
RUN python -m venv endp_env
RUN source ./endp_env/bin/activate && yes | pip install -r requirements.txt



