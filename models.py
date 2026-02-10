"""
Data Models for IELTS Reading Application
Based on Class Diagram specifications
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import json


class QuestionType(Enum):
    """Enum for different question types in IELTS Reading"""
    TYPE1 = "Multiple Choice"
    TYPE2 = "True/False/Not Given"
    TYPE3 = "Yes/No/Not Given"
    TYPE4 = "Matching Information"
    TYPE5 = "Matching Headings"
    TYPE6 = "Matching Features"
    TYPE7 = "Matching Sentence Endings"
    TYPE8 = "Sentence Completion"
    TYPE9 = "Summary/Table/Flow-chart Completion"
    TYPE10 = "Diagram Label Completion"
    TYPE11 = "Short Answer Questions"


@dataclass
class Paragraph:
    """Represents a paragraph in reading content"""
    title: str = ""
    body: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'body': self.body
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Paragraph':
        return Paragraph(
            title=data.get('title', ''),
            body=data.get('body', '')
        )


@dataclass
class ReadingContent:
    """Represents the reading passage content"""
    explanation: str = ""
    title: str = ""
    paragraphs: List[Paragraph] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'explanation': self.explanation,
            'title': self.title,
            'paragraphs': [p.to_dict() for p in self.paragraphs]
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ReadingContent':
        return ReadingContent(
            explanation=data.get('explanation', ''),
            title=data.get('title', ''),
            paragraphs=[Paragraph.from_dict(p) for p in data.get('paragraphs', [])]
        )


@dataclass
class Question:
    """Represents a single question"""
    text: str = ""
    answer: str = ""
    question_id: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'answer': self.answer,
            'question_id': self.question_id
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Question':
        return Question(
            text=data.get('text', ''),
            answer=data.get('answer', ''),
            question_id=data.get('question_id', '')
        )


@dataclass
class AdditionalInput:
    """Base class for additional inputs based on question type"""
    input_type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'input_type': self.input_type,
            'data': self.data
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'AdditionalInput':
        return AdditionalInput(
            input_type=data.get('input_type', ''),
            data=data.get('data', {})
        )


@dataclass
class QuestionGroup:
    """Represents a group of questions of the same type"""
    explanation: str = ""
    type: QuestionType = QuestionType.TYPE1
    questions: List[Question] = field(default_factory=list)
    additional_inputs: Optional[AdditionalInput] = None
    
    def validate(self) -> bool:
        """Validate question count (min 2, max 10)"""
        return 2 <= len(self.questions) <= 10
    
    def to_dict(self) -> Dict:
        return {
            'explanation': self.explanation,
            'type': self.type.value,
            'questions': [q.to_dict() for q in self.questions],
            'additional_inputs': self.additional_inputs.to_dict() if self.additional_inputs else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'QuestionGroup':
        # Find matching QuestionType
        question_type = QuestionType.TYPE1
        for qt in QuestionType:
            if qt.value == data.get('type'):
                question_type = qt
                break
        
        return QuestionGroup(
            explanation=data.get('explanation', ''),
            type=question_type,
            questions=[Question.from_dict(q) for q in data.get('questions', [])],
            additional_inputs=AdditionalInput.from_dict(data['additional_inputs']) 
                if data.get('additional_inputs') else None
        )


@dataclass
class ReadingPackage:
    """Complete reading package with content and questions"""
    package_id: str = ""
    reading_content: ReadingContent = field(default_factory=ReadingContent)
    question_groups: List[QuestionGroup] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            'package_id': self.package_id,
            'reading_content': self.reading_content.to_dict(),
            'question_groups': [qg.to_dict() for qg in self.question_groups],
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'ReadingPackage':
        return ReadingPackage(
            package_id=data.get('package_id', ''),
            reading_content=ReadingContent.from_dict(data.get('reading_content', {})),
            question_groups=[QuestionGroup.from_dict(qg) for qg in data.get('question_groups', [])],
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        )
    
    def save_to_file(self, filepath: str):
        """Save package to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_from_file(filepath: str) -> 'ReadingPackage':
        """Load package from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return ReadingPackage.from_dict(data)


@dataclass
class AnswerRecord:
    """Records user's answer to a question"""
    question_id: str
    user_answer: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class HighlightRecord:
    """Records text highlighting during exam"""
    selection_range: str
    highlight_color: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FeedbackItem:
    """Feedback for a single question"""
    question_id: str
    is_correct: bool
    correct_answer: str
    user_answer: Optional[str]
    
    def to_dict(self) -> Dict:
        return {
            'question_id': self.question_id,
            'is_correct': self.is_correct,
            'correct_answer': self.correct_answer,
            'user_answer': self.user_answer
        }


@dataclass
class EvaluationResult:
    """Complete evaluation result"""
    correct_count: int = 0
    incorrect_count: int = 0
    unanswered_count: int = 0
    total_questions: int = 0
    band_score: float = 0.0
    per_question_feedback: List[FeedbackItem] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'correct_count': self.correct_count,
            'incorrect_count': self.incorrect_count,
            'unanswered_count': self.unanswered_count,
            'total_questions': self.total_questions,
            'band_score': self.band_score,
            'per_question_feedback': [f.to_dict() for f in self.per_question_feedback]
        }


@dataclass
class IELTSScoringRules:
    """IELTS band score mapping"""
    mapping: Dict[int, float] = field(default_factory=dict)
    
    @staticmethod
    def get_academic_rules() -> 'IELTSScoringRules':
        """Standard IELTS Academic Reading band scores"""
        mapping = {
            0: 0.0, 1: 1.0, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5,
            6: 4.0, 7: 4.0, 8: 4.5, 9: 4.5, 10: 5.0,
            11: 5.0, 12: 5.5, 13: 5.5, 14: 6.0, 15: 6.0,
            16: 6.5, 17: 6.5, 18: 6.5, 19: 7.0, 20: 7.0,
            21: 7.0, 22: 7.0, 23: 7.5, 24: 7.5, 25: 8.0,
            26: 8.0, 27: 8.0, 28: 8.0, 29: 8.5, 30: 8.5,
            31: 8.5, 32: 8.5, 33: 9.0, 34: 9.0, 35: 9.0,
            36: 9.0, 37: 9.0, 38: 9.0, 39: 9.0, 40: 9.0
        }
        return IELTSScoringRules(mapping=mapping)
