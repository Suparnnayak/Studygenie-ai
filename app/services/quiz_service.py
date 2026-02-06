"""
Quiz and content generation service using AI
"""
from typing import Dict, Any, List
from app.services.ai_service import AIService
from app.services.chunk_service import ChunkService
from app.schemas.quiz_schema import (
    SkillMapResponse,
    QuizResponse,
    MCQ,
    MCQOption,
    SkillMapItem
)
from app.schemas.interview_schema import (
    InterviewResponse,
    InterviewQuestion
)


class QuizService:
    """Service for generating quizzes, skill maps, and interview Q&A"""
    
    def __init__(self):
        """Initialize quiz service with AI and chunking"""
        self.ai_service = AIService()
        self.chunk_service = ChunkService()
    
    def generate_skill_map(self, syllabus_text: str) -> Dict[str, Any]:
        """
        Generate skill map (topics & subtopics) from syllabus
        
        Args:
            syllabus_text: Text content from PDF syllabus
            
        Returns:
            Dictionary containing skill map data
        """
        prompt = f"""Analyze the following syllabus and create a comprehensive skill map with topics and subtopics.

Syllabus Content:
{syllabus_text[:4000]}

Return a JSON object with this exact structure:
{{
  "skill_map": [
    {{
      "topic": "Topic Name",
      "subtopics": ["Subtopic 1", "Subtopic 2", ...],
      "description": "Brief description of the topic"
    }}
  ],
  "total_topics": <number>
}}

Requirements:
- Extract all major topics from the syllabus
- List relevant subtopics for each topic
- Organize hierarchically
- Include 5-15 main topics
- Return ONLY valid JSON, no markdown, no explanations
"""
        
        try:
            response = self.ai_service.generate_response(prompt, max_retries=1)
            
            # Validate structure
            if 'skill_map' not in response:
                raise ValueError("Invalid skill map response structure")
            
            return response
            
        except Exception as e:
            raise Exception(f"Error generating skill map: {str(e)}")
    
    def generate_quiz(self, syllabus_text: str, num_questions: int = 10) -> Dict[str, Any]:
        """
        Generate multiple choice quiz questions from syllabus
        
        Args:
            syllabus_text: Text content from PDF syllabus
            num_questions: Number of questions to generate
            
        Returns:
            Dictionary containing quiz data
        """
        prompt = f"""Create {num_questions} multiple choice questions (MCQs) based on the following syllabus content.

Syllabus Content:
{syllabus_text[:4000]}

Return a JSON object with this exact structure:
{{
  "quiz": [
    {{
      "question": "Question text here?",
      "options": [
        {{"text": "Option A", "is_correct": true}},
        {{"text": "Option B", "is_correct": false}},
        {{"text": "Option C", "is_correct": false}},
        {{"text": "Option D", "is_correct": false}}
      ],
      "explanation": "Explanation of why the correct answer is right",
      "difficulty": "medium",
      "topic": "Topic name"
    }}
  ],
  "total_questions": {num_questions},
  "topics_covered": ["Topic 1", "Topic 2", ...]
}}

Requirements:
- Generate exactly {num_questions} questions
- Each question must have 4 options
- Only one option should be correct (is_correct: true)
- Cover different topics from the syllabus
- Include explanations for correct answers
- Vary difficulty levels (easy, medium, hard)
- Return ONLY valid JSON, no markdown, no explanations
"""
        
        try:
            response = self.ai_service.generate_response(prompt, max_retries=1)
            
            # Validate structure
            if 'quiz' not in response:
                raise ValueError("Invalid quiz response structure")
            
            # Ensure all questions have valid structure
            for q in response.get('quiz', []):
                if 'options' not in q:
                    raise ValueError("Question missing options")
                correct_count = sum(1 for opt in q['options'] if opt.get('is_correct', False))
                if correct_count != 1:
                    raise ValueError(f"Question must have exactly one correct answer, found {correct_count}")
            
            return response
            
        except Exception as e:
            raise Exception(f"Error generating quiz: {str(e)}")
    
    def generate_interview_qa(self, syllabus_text: str, num_questions: int = 10) -> Dict[str, Any]:
        """
        Generate interview questions and answers from syllabus
        
        Args:
            syllabus_text: Text content from PDF syllabus
            num_questions: Number of questions to generate
            
        Returns:
            Dictionary containing interview Q&A data
        """
        prompt = f"""Create {num_questions} interview questions and answers based on the following syllabus content.

Syllabus Content:
{syllabus_text[:4000]}

Return a JSON object with this exact structure:
{{
  "interview_qa": [
    {{
      "question": "What is...?",
      "answer": "Comprehensive answer explaining the concept",
      "topic": "Topic name",
      "difficulty": "medium",
      "follow_up_questions": ["Follow-up question 1", "Follow-up question 2"]
    }}
  ],
  "total_questions": {num_questions},
  "topics_covered": ["Topic 1", "Topic 2", ...]
}}

Requirements:
- Generate exactly {num_questions} questions
- Provide comprehensive, detailed answers
- Cover different topics from the syllabus
- Include 1-3 follow-up questions per main question
- Vary difficulty levels (easy, medium, hard)
- Answers should be thorough and educational
- Return ONLY valid JSON, no markdown, no explanations
"""
        
        try:
            response = self.ai_service.generate_response(prompt, max_retries=1)
            
            # Validate structure
            if 'interview_qa' not in response:
                raise ValueError("Invalid interview Q&A response structure")
            
            return response
            
        except Exception as e:
            raise Exception(f"Error generating interview Q&A: {str(e)}")
    
    def process_syllabus(
        self,
        syllabus_text: str,
        quiz_questions: int = 10,
        interview_questions: int = 10
    ) -> Dict[str, Any]:
        """
        Process syllabus and generate all outputs: skill map, quiz, and interview Q&A
        
        Args:
            syllabus_text: Text content from PDF syllabus
            quiz_questions: Number of quiz questions to generate
            interview_questions: Number of interview questions to generate
            
        Returns:
            Dictionary containing skill_map, quiz, and interview_qa
        """
        try:
            # Generate all three outputs
            skill_map = self.generate_skill_map(syllabus_text)
            quiz = self.generate_quiz(syllabus_text, quiz_questions)
            interview_qa = self.generate_interview_qa(syllabus_text, interview_questions)
            
            return {
                'skill_map': skill_map,
                'quiz': quiz,
                'interview_qa': interview_qa,
                'status': 'success'
            }
            
        except Exception as e:
            raise Exception(f"Error processing syllabus: {str(e)}")

