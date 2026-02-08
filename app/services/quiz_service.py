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

    def generate_topic_quiz(
        self,
        topic: str,
        difficulty: str = "medium",
        num_questions: int = 10
    ) -> Dict[str, Any]:
        """
        Generate quiz questions for a specific topic
        """
        num_questions = min(num_questions, 15)  # Cap at 15 for reliability
        
        prompt = f"""
You are an educational AI system.

Generate {num_questions} multiple-choice quiz questions about the topic: "{topic}"

Difficulty level: {difficulty}

====================
OUTPUT JSON FORMAT (STRICT)
====================
{{
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
      "difficulty": "{difficulty}",
      "topic": "{topic}"
    }}
  ],
  "total_questions": {num_questions},
  "topics_covered": ["{topic}"]
}}

====================
RULES (MANDATORY)
====================
- Return ONLY valid JSON
- No markdown, no explanations outside JSON
- Every MCQ must have EXACTLY one correct option
- Questions should be appropriate for {difficulty} difficulty
- Cover different aspects of {topic}
"""

        try:
            response = self.ai_service.generate_json_response(
                prompt=prompt,
                max_retries=1
            )
            
            if "quiz" not in response:
                raise ValueError("Missing quiz in AI response")
            
            return response
            
        except Exception as e:
            raise RuntimeError(f"Error generating quiz: {str(e)}")

    def generate_topic_flashcards(
        self,
        topic: str,
        num_cards: int = 10
    ) -> Dict[str, Any]:
        """
        Generate flashcards for a specific topic
        """
        num_cards = min(num_cards, 15)  # Cap at 15 for reliability
        
        prompt = f"""
You are an educational AI system.

Generate {num_cards} flashcards about the topic: "{topic}"

Each flashcard should have:
- Front: A question or concept
- Back: The answer or explanation

====================
OUTPUT JSON FORMAT (STRICT)
====================
{{
  "flashcards": [
    {{
      "front": "Question or concept",
      "back": "Answer or explanation",
      "difficulty": "easy | medium | hard",
      "topic": "{topic}"
    }}
  ],
  "total_cards": {num_cards},
  "topic": "{topic}"
}}

====================
RULES (MANDATORY)
====================
- Return ONLY valid JSON
- No markdown, no explanations outside JSON
- Front should be a clear question or concept
- Back should be a comprehensive answer
- Cover different aspects of {topic}
"""

        try:
            response = self.ai_service.generate_json_response(
                prompt=prompt,
                max_retries=1
            )
            
            if "flashcards" not in response:
                raise ValueError("Missing flashcards in AI response")
            
            return response
            
        except Exception as e:
            raise RuntimeError(f"Error generating flashcards: {str(e)}")

    def generate_coding_challenge(
        self,
        topic: str,
        difficulty: str = "medium",
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Generate a coding challenge for a specific topic
        """
        prompt = f"""
You are an educational AI system.

Generate a coding challenge about the topic: "{topic}"

Difficulty: {difficulty}
Language: {language}

====================
OUTPUT JSON FORMAT (STRICT)
====================
{{
  "challenge": {{
    "title": "Challenge Title",
    "description": "Detailed problem description",
    "difficulty": "{difficulty}",
    "topic": "{topic}",
    "starter_code": "// Starter code in {language}",
    "test_cases": [
      {{
        "input": "input example",
        "output": "expected output",
        "explanation": "What this test case checks"
      }}
    ],
    "hints": [
      "Hint 1",
      "Hint 2",
      "Hint 3"
    ],
    "time_complexity": "O(n) or similar",
    "space_complexity": "O(1) or similar",
    "xp_reward": 50
  }}
}}

====================
RULES (MANDATORY)
====================
- Return ONLY valid JSON
- No markdown, no explanations outside JSON
- Challenge should be appropriate for {difficulty} difficulty
- Include at least 3 test cases
- Provide starter code in {language}
- Include 3-5 progressive hints
"""

        try:
            response = self.ai_service.generate_json_response(
                prompt=prompt,
                max_retries=1
            )
            
            if "challenge" not in response:
                raise ValueError("Missing challenge in AI response")
            
            return response
            
        except Exception as e:
            raise RuntimeError(f"Error generating coding challenge: {str(e)}")

