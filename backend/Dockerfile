# Use an official Python image with CUDA support
FROM nvidia/cuda:12.6.2-base-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    cuda-toolkit-12-6 \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install PyTorch with CUDA support
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies (excluding torchvision and torchaudio)
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5000

# Run the application
CMD ["python3", "app.py"]
