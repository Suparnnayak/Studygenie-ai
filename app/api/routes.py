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


api_bp = Blueprint('api', __name__)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@api_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Upload PDF syllabus and generate skill map, quiz, and interview Q&A
    
    Request:
        - Method: POST
        - Content-Type: multipart/form-data
        - Body: PDF file in 'file' field
        
    Response:
        - JSON containing:
            - skill_map: Topics and subtopics
            - quiz: Multiple choice questions
            - interview_qa: Interview questions and answers
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'message': 'Please upload a PDF file'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a PDF file to upload'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'message': 'Only PDF files are allowed'
            }), 400
        
        # Get optional parameters
        quiz_questions = request.form.get('quiz_questions', 10, type=int)
        interview_questions = request.form.get('interview_questions', 10, type=int)
        
        # Validate question counts
        if quiz_questions < 1 or quiz_questions > 50:
            quiz_questions = 10
        if interview_questions < 1 or interview_questions > 50:
            interview_questions = 10
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Extract text from PDF
            pdf_service = PDFService()
            extracted_text = pdf_service.extract_text(filepath)
            
            if not extracted_text or len(extracted_text.strip()) < 50:
                return jsonify({
                    'error': 'Invalid PDF content',
                    'message': 'PDF appears to be empty or contains no extractable text'
                }), 400
            
            # Process syllabus and generate outputs
            quiz_service = QuizService()
            result = quiz_service.process_syllabus(
                syllabus_text=extracted_text,
                quiz_questions=quiz_questions,
                interview_questions=interview_questions
            )
            
            # Validate responses with Pydantic (optional, for extra validation)
            try:
                # Validate skill map
                skill_map_validated = SkillMapResponse(**result['skill_map'])
                result['skill_map'] = skill_map_validated.model_dump()
                
                # Validate quiz
                quiz_validated = QuizResponse(**result['quiz'])
                result['quiz'] = quiz_validated.model_dump()
                
                # Validate interview Q&A
                interview_validated = InterviewResponse(**result['interview_qa'])
                result['interview_qa'] = interview_validated.model_dump()
                
            except Exception as validation_error:
                # Log validation error but don't fail the request
                # The AI response might have minor schema differences
                print(f"Validation warning: {str(validation_error)}")
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass  # Ignore cleanup errors
            
            return jsonify(result), 200
            
        except ValueError as e:
            # Clean up file on error
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({
                'error': 'PDF processing error',
                'message': str(e)
            }), 400
            
        except Exception as e:
            # Clean up file on error
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({
                'error': 'Processing error',
                'message': f'Error processing PDF: {str(e)}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'message': f'Unexpected error: {str(e)}'
        }), 500

