FROM ://microsoft.com

WORKDIR /app

RUN npx playwright install chrome

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
