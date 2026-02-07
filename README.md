# StudyGenie AI Backend

A production-ready Flask backend service that analyzes PDF syllabi and generates comprehensive study materials using Groq's Llama 3.1 70B Versatile AI.

## 🚀 Features

- **PDF Text Extraction**: Extract and clean text from PDF syllabi
- **Skill Map Generation**: Automatically identify topics and subtopics
- **Quiz Generation**: Create multiple-choice questions (MCQs) with explanations
- **Interview Q&A**: Generate interview questions with detailed answers
- **JSON Validation**: Strict JSON output validation using Pydantic schemas
- **Production Ready**: Optimized for deployment on Render, Heroku, or any cloud platform

## 📡 API Endpoints

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "StudyGenie AI Backend"
}
```

### POST `/api/upload-pdf`
Upload a PDF syllabus and generate study materials.

**Request:**
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file` (required): PDF file
  - `quiz_questions` (optional): Number of quiz questions (1-50, default: 10)
  - `interview_questions` (optional): Number of interview questions (1-50, default: 10)

**Example (cURL):**
```bash
curl -X POST https://your-app.onrender.com/api/upload-pdf \
  -F "file=@syllabus.pdf" \
  -F "quiz_questions=15" \
  -F "interview_questions=12"
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('quiz_questions', '15');
formData.append('interview_questions', '12');

const response = await fetch('https://your-app.onrender.com/api/upload-pdf', {
  method: 'POST',
  body: formData
});

const data = await response.json();
```

**Success Response (200):**
```json
{
  "skill_map": {
    "skill_map": [
      {
        "topic": "Introduction to Python",
        "subtopics": ["Variables", "Data Types", "Operators"],
        "description": "Fundamentals of Python programming"
      }
    ],
    "total_topics": 8
  },
  "quiz": {
    "quiz": [
      {
        "question": "What is the correct syntax for declaring a variable?",
        "options": [
          {"text": "var x = 5", "is_correct": false},
          {"text": "x = 5", "is_correct": true},
          {"text": "int x = 5", "is_correct": false},
          {"text": "x := 5", "is_correct": false}
        ],
        "explanation": "Python uses dynamic typing...",
        "difficulty": "easy",
        "topic": "Variables"
      }
    ],
    "total_questions": 10,
    "topics_covered": ["Variables", "Data Types"]
  },
  "interview_qa": {
    "interview_qa": [
      {
        "question": "Explain the difference between lists and tuples.",
        "answer": "Lists are mutable while tuples are immutable...",
        "topic": "Data Structures",
        "difficulty": "medium",
        "follow_up_questions": ["When would you use a tuple?"]
      }
    ],
    "total_questions": 10,
    "topics_covered": ["Data Structures"]
  },
  "status": "success"
}
```

**Error Responses:**

- **400 Bad Request:** Invalid file, missing file, or invalid PDF content
- **500 Server Error:** Processing error or API failure

## 🛠️ Tech Stack

- **Python 3.10+**
- **Flask** - Web framework
- **pdfplumber** - PDF text extraction
- **groq** - Groq Llama 3.1 70B Versatile integration
- **Pydantic** - JSON schema validation
- **python-dotenv** - Environment variable management
- **gunicorn** - Production WSGI server

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd studygenie-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your_secret_key
   CORS_ORIGINS=*
   ```

5. **Run the application**
   ```bash
   python -m app.main
   ```
   Server runs on `http://localhost:5000`

## 🚀 Deployment to Render

### Option 1: Using Render Dashboard

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3
4. **Add Environment Variables:**
   - `GROQ_API_KEY` - Your Groq API key (get from https://console.groq.com)
   - `SECRET_KEY` - A secure random string
   - `CORS_ORIGINS` - Your frontend URL (or `*` for all)
   - `FLASK_DEBUG` - Set to `False` for production

### Option 2: Using render.yaml

The project includes a `render.yaml` file. Simply:
1. Push your code to GitHub
2. Connect the repository in Render
3. Render will automatically detect and use `render.yaml`

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key | ✅ Yes | - |
| `SECRET_KEY` | Flask secret key | ⚠️ Recommended | Auto-generated |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | ❌ No | `*` |
| `PORT` | Server port (auto-set by Render) | ❌ No | `5000` |
| `FLASK_DEBUG` | Debug mode | ❌ No | `False` |

## 📁 Project Structure

```
studygenie-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask app factory
│   ├── config.py            # Configuration
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── services/
│   │   ├── pdf_service.py   # PDF extraction
│   │   ├── ai_service.py    # Groq AI integration
│   │   └── quiz_service.py  # Content generation
│   ├── schemas/
│   │   ├── quiz_schema.py   # Quiz models
│   │   └── interview_schema.py # Interview models
│   └── utils/
│       ├── cleaner.py       # Text cleaning
│       └── json_validator.py # JSON validation
├── uploads/                 # Temporary file storage
├── requirements.txt         # Dependencies
├── render.yaml             # Render configuration
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🔧 Development

### Running Locally

```bash
python -m app.main
```

### Running with Gunicorn (Production-like)

```bash
pip install gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000
```

### Testing the API

```bash
# Health check
curl http://localhost:5000/health

# Upload PDF
curl -X POST http://localhost:5000/api/upload-pdf \
  -F "file=@syllabus.pdf"
```

## 📝 Notes

- **PDF Requirements:** PDFs must contain extractable text (scanned PDFs not supported)
- **File Size Limit:** Maximum 16MB per file
- **Processing Time:** 10-30 seconds depending on PDF size
- **API Rate Limits:** Be aware of Groq API rate limits

## 🐳 Docker Deployment

```bash
# Build
docker build -t studygenie-ai .

# Run
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key \
  -e SECRET_KEY=your_secret \
  studygenie-ai
```

## 📄 License

This project is provided as-is for educational and development purposes.

## 🆘 Troubleshooting

### Render Deployment Issues

**Issue: Build fails with Rust/cargo errors**
- **Solution:** The project uses Python 3.11 (specified in `runtime.txt` and `render.yaml`) to avoid compilation issues with newer Python versions
- Ensure `runtime.txt` contains `python-3.11.9`
- Render should automatically use Python 3.11 if `runtime.txt` is present

**Issue: Module not found errors**
- **Solution:** Ensure all dependencies are in `requirements.txt` with pinned versions

**Issue: Port binding errors**
- **Solution:** The app automatically uses the `$PORT` environment variable set by Render

## 🆘 Support

For issues or questions:
- Check [Flask documentation](https://flask.palletsprojects.com/)
- Check [Groq API documentation](https://console.groq.com/docs)
- Check [Render documentation](https://render.com/docs)
