FROM python:2-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./solutions.py" ]
#CMD ["--protocol", "http", "--hostname", "localhost", "--port", "3000"]
CMD ["--help"]

