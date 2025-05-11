from fastapi.testclient import TestClient
from src.main import app
from src.services import breed_service

client = TestClient(app)


def mock_breed_data():
    return [
        {
            "name": "Akita",
            "life_span": "10 - 14 years",
            "bred_for": "Guarding",
            "breed_group": "Working",
            "temperament": "Docile, Alert",
        },
        {
            "name": "Beagle",
            "life_span": "12 - 15 years",
            "bred_for": "Hunting",
            "breed_group": "Hound",
            "temperament": "Excitable, Gentle",
        },
        {
            "name": "Bulldog",
            "life_span": "8 - 10 years",
            "bred_for": "Bull baiting",
            "breed_group": "Non-Sporting",
            "temperament": "Docile, Friendly",
        },
    ]


def test_breeds_by_lifespan(monkeypatch):
    async def mock_fetch():
        return mock_breed_data()

    monkeypatch.setattr(breed_service, "fetch_breeds", mock_fetch)

    response = client.get("/breeds/lifespan?min_years=10&max_years=14")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("name" in b and "lifespan" in b for b in data)
    assert any(b["name"] == "Akita" for b in data)
    assert all("Bulldog" not in b["name"] for b in data)


def test_breeds_by_lifespan_invalid_range():
    response = client.get("/breeds/lifespan?min_years=15&max_years=5")
    assert response.status_code == 400
    assert "min_years must be less than or equal to max_years" in response.text


def test_breeds_alphabetical(monkeypatch):
    async def mock_fetch():
        return mock_breed_data()

    monkeypatch.setattr(breed_service, "fetch_breeds", mock_fetch)

    response = client.get("/breeds/alphabetical")
    assert response.status_code == 200
    data = response.json()
    expected = sorted([b["name"] for b in mock_breed_data()])
    assert data == expected


def test_breeds_export_pdf(monkeypatch):
    async def mock_fetch():
        return mock_breed_data()

    monkeypatch.setattr(breed_service, "fetch_breeds", mock_fetch)

    response = client.get("/breeds/export/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 100

