# Cryptocurrency Rates Service

A service that fetches real-time cryptocurrency exchange rates from Binance API and provides a REST API for querying cached rates.

Supports: BTC, ETH, USDT

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Run the Service

1. **Clone and start**
   ```bash
   git clone <repository-url>
   cd cryptocurrency_rates
   chmod +x start.sh
   ./start.sh
   ```

2. **Test the API**
   ```bash
   curl "http://localhost:8080/api/v1/crypto-currency/rate?from_currency=BTC&to_currency=USDT"
   ```

### Manual Setup (if script doesn't work)

```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec cryptocurrency_rates_service alembic upgrade head

# Check health
curl http://localhost:4000/ping/cryptocurrency_rates
```

## API Usage

**Get exchange rate:**
```bash
curl "http://localhost:8080/api/v1/crypto-currency/rate?from_currency=BTC&to_currency=USDT"
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
- **Database errors**: Run `docker-compose down && docker-compose up -d` to reset
