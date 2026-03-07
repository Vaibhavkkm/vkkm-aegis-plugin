# Use the official lightweight Python image.
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose the port that Hugging Face expects (7860 by default for HF Spaces)
EXPOSE 7860

# Run the FastAPI server. 
# We set host to 0.0.0.0 so it's accessible externally.
# We set port to 7860 to match Hugging Face's default.
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "7860"]
