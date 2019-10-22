FROM python:3-slim

WORKDIR /app/

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY __init__.py lodestone.py ./

ENTRYPOINT ["python", "lodestone.py"]
