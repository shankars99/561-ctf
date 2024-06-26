FROM python:3.9

# Copy the source code
COPY . /app

# Set the working directory
WORKDIR /app

# Install required pip packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLAG=CTF_SDaT{CS561ROCKS}

# Run the application
CMD ["python", "src/main.py"]