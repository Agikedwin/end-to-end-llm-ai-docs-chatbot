# Use the official Python base image
FROM python:3.11-slim
# Accept build arguments
ARG OPENAI_API_KEY
ARG PINECONE_API_KEY

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV PINECONE_API_KEY=$PINECONE_API_KEY

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt 
RUN pip install -U langchain-huggingface
RUN pip install -U sentence-transformers

# Copy application code
COPY . .

# Expose the port your app runs on
EXPOSE 8085

# Set the default command
CMD ["python3", "app.py"]
