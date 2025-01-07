FROM python:3.13.1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run", "app.py", "--host", "0.0.0.0", "--port", "5000" ]
