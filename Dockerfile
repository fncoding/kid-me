# Stage 1: Node build for static assets
FROM node:20-alpine as nodebuilder
WORKDIR /app
COPY src/package.json ./
RUN npm install
COPY src/static_src/ ./static_src/
RUN npm run build-static:linux

# Stage 2: Python build
FROM python:3.11-slim as builder
WORKDIR /app
COPY src/requirements.txt .
RUN python -m venv /opt/venv
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Stage 3: Final image
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./src /app/
COPY --from=nodebuilder /app/assets/css /app/staticfiles/css
COPY --from=nodebuilder /app/assets/js /app/staticfiles/js
COPY --from=nodebuilder /app/assets/bootstrap-icons /app/staticfiles/bootstrap-icons
EXPOSE 8000