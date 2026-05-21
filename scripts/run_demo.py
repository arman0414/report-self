from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.post('/api/research', json={'topic': 'production-grade AI incident response platforms', 'audience': 'CTO and platform engineering leads', 'depth': 4})
response.raise_for_status()
report = response.json()
print(report['markdown'])
