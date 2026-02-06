# API Reference

## Base URL
- **Local:** `http://localhost:5000`
- **Production:** `https://your-app.onrender.com`

## Endpoints

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "StudyGenie AI Backend"
}
```

---

### POST `/api/upload-pdf`
Upload a PDF syllabus and generate study materials.

**Request:**
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `file` (required): PDF file
  - `quiz_questions` (optional): Number of quiz questions (1-50, default: 10)
  - `interview_questions` (optional): Number of interview questions (1-50, default: 10)

**Success Response (200):**
```json
{
  "skill_map": {
    "skill_map": [...],
    "total_topics": 8
  },
  "quiz": {
    "quiz": [...],
    "total_questions": 10,
    "topics_covered": [...]
  },
  "interview_qa": {
    "interview_qa": [...],
    "total_questions": 10,
    "topics_covered": [...]
  },
  "status": "success"
}
```

**Error Responses:**
- **400:** Invalid file, missing file, or invalid PDF content
- **500:** Processing error or API failure

