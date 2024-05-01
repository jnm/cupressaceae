FROM cypress/included:13.8.1
RUN apt-get update && apt-get install --yes python3 python3-venv && apt-get clean
COPY index.py requirements.txt /opt/http-handler/
RUN ["/bin/bash", "-c", "python3 -m venv /opt/http-handler/e && source /opt/http-handler/e/bin/activate && pip install -r /opt/http-handler/requirements.txt"]
COPY ./volume/ /yay/
WORKDIR /yay/
ENTRYPOINT ["/bin/bash", "-c", "source /opt/http-handler/e/bin/activate && python3 /opt/http-handler/index.py"]
