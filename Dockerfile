# Backend stage
FROM python:3.11.6-slim AS backendBuilder

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the backend files
COPY . .

EXPOSE 8000

# just for build
# cmd ["cd", "frontend", "npm run i && npm run build"]

CMD ["python", "main.py"]