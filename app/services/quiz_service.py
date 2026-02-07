"""
Quiz, Skill Map, and Interview generation using a SINGLE AI call
"""
from typing import Dict, Any
from app.services.ai_service import AIService
from app.config import Config


class QuizService:
    """
    Service for generating skill map, quiz, and interview Q&A
    using ONE LLM call (Groq)
    """

    def __init__(self):
        self.ai_service = AIService()

    def process_syllabus(
        self,
        syllabus_text: str,
        quiz_questions: int = 10,
        interview_questions: int = 10
    ) -> Dict[str, Any]:
        """
        Process syllabus and generate:
        - skill_map
        - quiz
        - interview_qa

        Returns a single structured JSON
        """

        # 🔒 Safety: cap syllabus size
        syllabus_text = syllabus_text[:Config.MAX_SYLLABUS_CHARS]
        
        # 🥇 FIX 1: Reduce JSON size to improve parsing reliability
        # Cap questions to reduce JSON size by ~40% and improve correctness
        quiz_questions = min(quiz_questions, 6)
        interview_questions = min(interview_questions, 5)

        prompt = f"""
You are an educational AI system.

Analyze the following syllabus and generate ALL of the following
in ONE JSON response:

1. Skill Map
2. Quiz (MCQs)
3. Interview Q&A

====================
SYLLABUS
====================
{syllabus_text}

====================
OUTPUT JSON FORMAT (STRICT)
====================
{{
  "skill_map": {{
    "skill_map": [
      {{
        "topic": "Topic Name",
        "subtopics": ["Subtopic 1", "Subtopic 2"],
        "description": "Brief description"
      }}
    ],
    "total_topics": <number>
  }},
  "quiz": {{
    "quiz": [
      {{
        "question": "Question text?",
        "options": [
          {{"text": "Option A", "is_correct": true}},
          {{"text": "Option B", "is_correct": false}},
          {{"text": "Option C", "is_correct": false}},
          {{"text": "Option D", "is_correct": false}}
        ],
        "explanation": "Why the correct answer is correct",
        "difficulty": "easy | medium | hard",
        "topic": "Topic name"
      }}
    ],
    "total_questions": {quiz_questions}
  }},
  "interview_qa": {{
    "interview_qa": [
      {{
        "question": "Interview question?",
        "answer": "Detailed answer",
        "topic": "Topic name",
        "difficulty": "easy | medium | hard",
        "follow_up_questions": [
          "Follow-up question 1",
          "Follow-up question 2"
        ]
      }}
    ],
    "total_questions": {interview_questions}
  }}
}}

====================
RULES (MANDATORY)
====================
- Return ONLY valid JSON
- No markdown
- No explanations outside JSON
- Every MCQ must have EXACTLY one correct option
- Use realistic interview-level answers
- Cover as many syllabus topics as possible
"""

        try:
            response = self.ai_service.generate_json_response(
                prompt=prompt,
                max_retries=1
            )

            # 🔎 Minimal structural validation
            if "skill_map" not in response:
                raise ValueError("Missing skill_map in AI response")
            if "quiz" not in response:
                raise ValueError("Missing quiz in AI response")
            if "interview_qa" not in response:
                raise ValueError("Missing interview_qa in AI response")

            return {
                "skill_map": response["skill_map"],
                "quiz": response["quiz"],
                "interview_qa": response["interview_qa"],
                "status": "success"
            }

        except Exception as e:
            raise RuntimeError(f"Error processing syllabus: {str(e)}")
