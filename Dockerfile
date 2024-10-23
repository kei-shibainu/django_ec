FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip install -r requirements.txt
COPY . /workspace/
