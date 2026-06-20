# Step 1: Use an official lightweight Python image as the foundation
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy only the dependencies file first (optimizes Docker build caching)
COPY requirements.txt .

# Step 4: Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY app.py .

# Step 6: Inform Docker that the container listens on port 5000 at runtime
EXPOSE 5000

# Step 7: Define the exact command to run your app when the container starts
CMD ["python", "app.py"]
