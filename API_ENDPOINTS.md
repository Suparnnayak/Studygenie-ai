# StudyGenie AI Backend - API Endpoints

## Base URL
- **Local:** `http://localhost:5000`
- **Production:** `https://studygenie-ai.onrender.com`

## Endpoints

### 1. GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "StudyGenie AI Backend"
}
```

---

### 2. POST `/api/upload-pdf`
Upload a PDF syllabus and generate study materials.

**Request:**
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file` (required): PDF file
  - `quiz_questions` (optional): Number of quiz questions (1-50, default: 10)
  - `interview_questions` (optional): Number of interview questions (1-50, default: 10)

**Response:**
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

---

### 3. POST `/api/generate-quiz`
Generate quiz questions for a specific topic.

**Request:**
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Body:**
```json
{
  "topic": "Arrays",
  "difficulty": "medium",
  "num_questions": 10
}
```

**Response:**
```json
{
  "quiz": [
    {
      "question": "What is an array?",
      "options": [
        {"text": "Option A", "is_correct": true},
        {"text": "Option B", "is_correct": false},
        {"text": "Option C", "is_correct": false},
        {"text": "Option D", "is_correct": false}
      ],
      "explanation": "Explanation text",
      "difficulty": "medium",
      "topic": "Arrays"
    }
  ],
  "total_questions": 10,
  "topics_covered": ["Arrays"]
}
```

---

### 4. POST `/api/generate-flashcards`
Generate flashcards for a specific topic.

**Request:**
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Body:**
```json
{
  "topic": "Linked Lists",
  "num_cards": 10
}
```

**Response:**
```json
{
  "flashcards": [
    {
      "front": "What is a linked list?",
      "back": "A linked list is a linear data structure...",
      "difficulty": "medium",
      "topic": "Linked Lists"
    }
  ],
  "total_cards": 10,
  "topic": "Linked Lists"
}
```

---

### 5. POST `/api/generate-coding-challenge`
Generate a coding challenge for a specific topic.

**Request:**
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Body:**
```json
{
  "topic": "Binary Search",
  "difficulty": "medium",
  "language": "python"
}
```

**Response:**
```json
{
  "challenge": {
    "title": "Implement Binary Search",
    "description": "Write a function to...",
    "difficulty": "medium",
    "topic": "Binary Search",
    "starter_code": "def binary_search(arr, target):\n    # Your code here",
    "test_cases": [
      {
        "input": "[1, 2, 3, 4, 5], 3",
        "output": "2",
        "explanation": "Finds index of 3"
      }
    ],
    "hints": [
      "Hint 1",
      "Hint 2",
      "Hint 3"
    ],
    "time_complexity": "O(log n)",
    "space_complexity": "O(1)",
    "xp_reward": 50
  }
}
```

---

## Error Responses

All endpoints return error responses in this format:

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

**Status Codes:**
- `400`: Bad Request (invalid input, missing parameters)
- `500`: Internal Server Error (processing error, API failure)
- `502`: Bad Gateway (backend connection error)

