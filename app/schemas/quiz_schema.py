"""
Pydantic schemas for Quiz generation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class MCQOption(BaseModel):
    """Multiple choice question option"""
    text: str = Field(..., description="Option text")
    is_correct: bool = Field(..., description="Whether this option is correct")


class MCQ(BaseModel):
    """Multiple Choice Question"""
    question: str = Field(..., description="Question text")
    options: List[MCQOption] = Field(..., min_items=2, max_items=5, description="Answer options")
    explanation: Optional[str] = Field(None, description="Explanation for the correct answer")
    difficulty: Optional[str] = Field(None, description="Difficulty level: easy, medium, hard")
    topic: Optional[str] = Field(None, description="Topic or subtopic this question covers")


class QuizResponse(BaseModel):
    """Quiz response schema"""
    quiz: List[MCQ] = Field(..., description="List of multiple choice questions")
    total_questions: int = Field(..., description="Total number of questions")
    topics_covered: List[str] = Field(default_factory=list, description="Topics covered in the quiz")


class SkillMapItem(BaseModel):
    """Individual skill/topic item"""
    topic: str = Field(..., description="Main topic name")
    subtopics: List[str] = Field(default_factory=list, description="List of subtopics")
    description: Optional[str] = Field(None, description="Brief description of the topic")


class SkillMapResponse(BaseModel):
    """Skill map response schema"""
    skill_map: List[SkillMapItem] = Field(..., description="List of topics and subtopics")
    total_topics: int = Field(..., description="Total number of topics")

