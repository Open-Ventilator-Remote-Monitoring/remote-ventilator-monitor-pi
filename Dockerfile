FROM naomori/raspbian-buster-lite:2020-02-13

RUN apt-get update && apt-get install -y python3-pip
RUN mkdir -p /opt/rvm
COPY server.py /opt/rvm/
COPY requirements.txt /opt/rvm/
COPY config.py /opt/rvm/
COPY wsgi.py /opt/rvm/
COPY start.sh /opt/rvm
RUN pip3 install -r /opt/rvm/requirements.txt

CMD cd /opt/rvm/ && ./start.sh
