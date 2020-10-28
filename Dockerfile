FROM python:3

WORKDIR /the/workdir/path

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./run.py"]

