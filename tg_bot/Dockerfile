# Use an official Python image as a base
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /tg_bot

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the command to start the bot
CMD ["python", "bot.py"]