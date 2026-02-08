"""
API routes for StudyGenie AI Backend
"""
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.config import Config
from app.services.pdf_service import PDFService
from app.services.quiz_service import QuizService
from app.schemas.quiz_schema import SkillMapResponse, QuizResponse
from app.schemas.interview_schema import InterviewResponse

api_bp = Blueprint("api", __name__, url_prefix="/api")


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


@api_bp.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    # -----------------------
    # 1. Validate request
    # -----------------------
    if "file" not in request.files:
        return jsonify({
            "error": "No file provided",
            "message": "Please upload a PDF file using form-data with key 'file'"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "Empty filename",
            "message": "Please select a PDF file"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Invalid file type",
            "message": "Only PDF files are allowed"
        }), 400

    # -----------------------
    # 2. Read optional params
    # -----------------------
    quiz_questions = request.form.get("quiz_questions", 10, type=int)
    interview_questions = request.form.get("interview_questions", 10, type=int)

    quiz_questions = max(1, min(quiz_questions, 50))
    interview_questions = max(1, min(interview_questions, 50))

    # -----------------------
    # 3. Save file
    # -----------------------
    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    try:
        file.save(filepath)

        # -----------------------
        # 4. Extract PDF text
        # -----------------------
        pdf_service = PDFService()
        extracted_text = pdf_service.extract_text(filepath)

        if not extracted_text or len(extracted_text.strip()) < 50:
            return jsonify({
                "error": "Invalid PDF content",
                "message": "PDF is empty or contains no readable text"
            }), 400

        # -----------------------
        # 5. Generate AI outputs
        # -----------------------
        quiz_service = QuizService()
        result = quiz_service.process_syllabus(
            syllabus_text=extracted_text,
            quiz_questions=quiz_questions,
            interview_questions=interview_questions
        )

        # -----------------------
        # 6. Validate with schemas (soft validation)
        # -----------------------
        try:
            result["skill_map"] = SkillMapResponse(**result["skill_map"]).model_dump()
            result["quiz"] = QuizResponse(**result["quiz"]).model_dump()
            result["interview_qa"] = InterviewResponse(
                **result["interview_qa"]
            ).model_dump()
        except Exception as schema_error:
            print(f"[Schema validation warning] {schema_error}")

        # -----------------------
        # 7. Success response
        # -----------------------
        return jsonify(result), 200

    except Exception as e:
        print(f"[UPLOAD_PDF_ERROR] {e}")
        return jsonify({
            "error": "Processing error",
            "message": str(e)
        }), 500

    finally:
        # -----------------------
        # 8. Cleanup
        # -----------------------
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as cleanup_error:
            print(f"[Cleanup warning] {cleanup_error}")


@api_bp.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    """
    Generate quiz questions for a specific topic
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON"
            }), 400
        
        topic = data.get("topic", "")
        difficulty = data.get("difficulty", "medium").lower()
        num_questions = data.get("num_questions", 10)
        
        if not topic:
            return jsonify({
                "error": "Missing topic",
                "message": "Please provide a topic name"
            }), 400
        
        # Validate difficulty
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"
        
        # Validate and cap question count
        num_questions = max(1, min(int(num_questions), 20))
        
        # Generate quiz using AI service
        quiz_service = QuizService()
        quiz_data = quiz_service.generate_topic_quiz(
            topic=topic,
            difficulty=difficulty,
            num_questions=num_questions
        )
        
        # Validate response
        try:
            quiz_response = QuizResponse(**quiz_data).model_dump()
            return jsonify(quiz_response), 200
        except Exception as schema_error:
            print(f"[Schema validation warning] {schema_error}")
            return jsonify(quiz_data), 200
            
    except Exception as e:
        print(f"[GENERATE_QUIZ_ERROR] {e}")
        return jsonify({
            "error": "Processing error",
            "message": str(e)
        }), 500


@api_bp.route("/generate-flashcards", methods=["POST"])
def generate_flashcards():
    """
    Generate flashcards for a specific topic
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON"
            }), 400
        
        topic = data.get("topic", "")
        num_cards = data.get("num_cards", 10)
        
        if not topic:
            return jsonify({
                "error": "Missing topic",
                "message": "Please provide a topic name"
            }), 400
        
        # Validate and cap card count
        num_cards = max(1, min(int(num_cards), 20))
        
        # Generate flashcards using AI service
        quiz_service = QuizService()
        flashcards_data = quiz_service.generate_topic_flashcards(
            topic=topic,
            num_cards=num_cards
        )
        
        return jsonify(flashcards_data), 200
            
    except Exception as e:
        print(f"[GENERATE_FLASHCARDS_ERROR] {e}")
        return jsonify({
            "error": "Processing error",
            "message": str(e)
        }), 500


@api_bp.route("/generate-coding-challenge", methods=["POST"])
def generate_coding_challenge():
    """
    Generate coding challenge for a specific topic
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must be JSON"
            }), 400
        
        topic = data.get("topic", "")
        difficulty = data.get("difficulty", "medium").lower()
        language = data.get("language", "python")
        
        if not topic:
            return jsonify({
                "error": "Missing topic",
                "message": "Please provide a topic name"
            }), 400
        
        # Validate difficulty
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"
        
        # Generate coding challenge using AI service
        quiz_service = QuizService()
        challenge_data = quiz_service.generate_coding_challenge(
            topic=topic,
            difficulty=difficulty,
            language=language
        )
        
        return jsonify(challenge_data), 200
            
    except Exception as e:
        print(f"[GENERATE_CODING_CHALLENGE_ERROR] {e}")
        return jsonify({
            "error": "Processing error",
            "message": str(e)
        }), 500
