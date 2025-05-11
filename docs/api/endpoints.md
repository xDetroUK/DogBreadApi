# API Endpoints

---

## 🔗 `/breeds/lifespan`

**Method**: GET  
**Query Params**:
- `min_years`: minimum lifespan (int)
- `max_years`: maximum lifespan (int)

**Response**:

```json
[
  {
    "name": "Beagle",
    "lifespan": "13 - 16 years"
  }
]
```

---

## 🔗 `/breeds/alphabetical`

**Method**: GET

**Response**:

```json
[
  "Affenpinscher",
  "Beagle"
]
```

---

## 🔗 `/breeds/export/pdf`

**Method**: GET  
**Response**: PDF file

**Description**: Download a sorted PDF containing all dog breed data

---

## 🔗 `/health`

**Method**: GET  
**Response**:
```json
{ "status": "healthy" }
```