# WebSocket Chat Application

A real-time chat application built with Flask, WebSocket, PostgreSQL, and monitoring using Prometheus and Grafana.

## Features

- Real-time messaging using WebSocket
- Message persistence in PostgreSQL
- Monitoring with Prometheus and Grafana
- Docker containerization
- CI/CD pipeline with GitHub Actions

## Prerequisites

- Docker and Docker Compose
- Git

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd websocket-chat-app
```

2. Create necessary directories:
```bash
mkdir -p app/templates prometheus
```

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at:
- Web Application: http://localhost:5001
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default credentials: admin/admin)

## Development

### Project Structure
```
.
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus/
│   └── prometheus.yml
├── docker-compose.yml
└── README.md
```

### Running Tests
```bash
cd app
pip install -r requirements.txt
pip install pytest pytest-cov
pytest
```

## Monitoring

### Prometheus
- Access Prometheus at http://localhost:9090
- View metrics at http://localhost:9090/metrics

### Grafana
- Access Grafana at http://localhost:3000
- Default credentials: admin/admin
- Add Prometheus as a data source (URL: http://prometheus:9090)

## CI/CD

The project uses GitHub Actions for continuous integration and deployment:
- Tests run on every push and pull request
- Docker image is built and pushed to DockerHub on main branch updates

## Security

- The application runs with a non-root user in Docker
- Database credentials are configurable through environment variables
- WebSocket connections are secured with a secret key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request