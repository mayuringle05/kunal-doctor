FROM python:3.13-alpine
WORKDIR /app
COPY build.py ./build.py
COPY content/doctor.json ./content/doctor.json
COPY assets/ ./assets/
RUN python3 build.py
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["sh", "-c", "exec python3 -m http.server ${PORT:-8080} --bind 0.0.0.0 --directory dist"]
