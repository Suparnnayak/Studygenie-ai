"""
Pydantic schemas for Interview Q&A generation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class InterviewQuestion(BaseModel):
    """Interview question and answer"""
    question: str = Field(..., description="Interview question")
    answer: str = Field(..., description="Expected answer")
    topic: Optional[str] = Field(None, description="Topic this question covers")
    difficulty: Optional[str] = Field(None, description="Difficulty level: easy, medium, hard")
    follow_up_questions: Optional[List[str]] = Field(default_factory=list, description="Potential follow-up questions")


class InterviewResponse(BaseModel):
    """Interview Q&A response schema"""
    interview_qa: List[InterviewQuestion] = Field(..., description="List of interview questions and answers")
    total_questions: int = Field(..., description="Total number of questions")
    topics_covered: List[str] = Field(default_factory=list, description="Topics covered in the interview")

