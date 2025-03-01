FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the SQLite database file exists and set permissions
# RUN mkdir -p /app/database && chmod 777 /app/database

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for Flask

# Run the Flask application
RUN mkdir -p /app/database && chmod 777 /app/database
RUN python init_db.py
# RUN sudo apt-get install tar
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz
RUN tar -xzvf geckodriver-v0.33.0-linux-aarch64.tar.gz -C /usr/local/bin
RUN chmod +x /usr/local/bin/geckodriver

CMD ["python", "app.py"]
