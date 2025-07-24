# Cryptocurrency Rates Service

A service that fetches real-time cryptocurrency exchange rates from Binance API and provides a REST API for querying cached rates.

## Supported Currencies

**From currencies:** BTC, ETH
**To currencies:** USDT

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Run the Service

1. **Clone and start**
   ```bash
   git clone <repository-url>
   cd cryptocurrency_rates
   docker-compose up -d --build
   ```

2. **Test the API**
   ```bash
   curl "http://localhost:8080/api/v1/convert?from=BTC&to=USDT&amount=1000"
   curl "http://localhost:8080/api/v1/convert?from=BTC&to=USDT&amount=1000&timestamp=2025-07-24+19:10:00"
   ```

## API Usage

**Convert cryptocurrency:**
```bash
curl "localhost:8080/api/v1/convert?from=BTC&to=USDT&amount=1000"
curl "localhost:8080/api/v1/convert?from=BTC&to=USDT&amount=1000&timestamp=2025-07-24+19:10:00"
```

**Response:**
```json
{
    "result_code": "success",
    "rate": "50000.00"
}
```

## Management

```bash
# View logs
docker-compose logs -f

# Stop service
docker-compose down

# Restart
docker-compose restart
```

## Troubleshooting

- **Service won't start**: Check ports 8080 and 4000 are free
- **API returns "quotes_outdated"**: Wait a few minutes for background tasks to fetch rates
- **Database errors**: Run `docker-compose down && docker-compose up -d --build` to reset
