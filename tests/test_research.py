from fastapi.testclient import TestClient
from app.main import app


def test_research_report_contains_citations_and_critique():
    client = TestClient(app)
    response = client.post('/api/research', json={'topic': 'RAG evaluation for enterprise AI', 'depth': 3})
    assert response.status_code == 201
    report = response.json()
    assert report['tasks']
    assert report['claims']
    assert '## Sources' in report['markdown']
    assert report['critiques']


def test_report_can_be_retrieved_after_creation():
    client = TestClient(app)
    created = client.post('/api/research', json={'topic': 'AI security controls', 'depth': 2}).json()
    fetched = client.get(f"/api/reports/{created['id']}").json()
    assert fetched['id'] == created['id']


def test_unrelated_topic_does_not_receive_fake_confident_claims():
    client = TestClient(app)
    report = client.post('/api/research', json={'topic': 'medieval bread recipes for monastery kitchens', 'depth': 3}).json()
    assert report['claims'] == []
    assert report['critiques'][0]['severity'] == 'high'
    assert 'No source-grounded claims' in report['markdown']


def test_acronym_casing_is_preserved_in_claims():
    client = TestClient(app)
    report = client.post('/api/research', json={'topic': 'RAG evaluation for enterprise AI systems', 'depth': 2}).json()
    assert any('RAG systems' in claim['text'] for claim in report['claims'])
    assert all('rAG' not in claim['text'] and 'lLM' not in claim['text'] for claim in report['claims'])
