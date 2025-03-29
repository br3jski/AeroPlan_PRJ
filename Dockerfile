FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make the script executable
RUN chmod +x devserver.sh

# Expose the port
EXPOSE 5000

# Run the app
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0"]