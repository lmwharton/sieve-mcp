FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir .

# Default to HTTP transport for container deployments
ENV PORT=8080
EXPOSE ${PORT}

CMD ["sieve-mcp", "http"]
