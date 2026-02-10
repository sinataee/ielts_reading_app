# IELTS Reading Test Application

A comprehensive Python application for creating, taking, and scoring IELTS Academic Reading tests.

## Overview

This application consists of three main modules that follow the architecture specified in the UML diagrams:

1. **Content Editor Module** - Create and edit IELTS reading packages
2. **Exam Engine Module** - Take reading tests with timing and scoring
3. **Result Engine Module** - View detailed results and band scores

## Features

### Content Editor
- Rich text editing with formatting (bold, italic, headers, alignment)
- Create reading passages with multiple paragraphs
- Add question groups (11 different IELTS question types supported)
- Save and load reading packages as JSON files
- Validate question counts (2-10 questions per group)

### Exam Engine
- Split-screen interface (reading passage on left, questions on right)
- 60-minute countdown timer with pause/resume
- Text highlighting system (4 colors)
- Support for all IELTS question types:
  - Type 1: Multiple Choice
  - Type 2: True/False/Not Given
  - Type 3: Yes/No/Not Given
  - Type 4-7: Matching types (Information, Headings, Features, Sentence Endings)
  - Type 8: Sentence Completion
  - Type 9: Summary/Table/Flow-chart Completion
  - Type 10: Diagram Label Completion
  - Type 11: Short Answer Questions
- Real-time answer recording
- Automatic submission when time expires

### Result Engine
- Comprehensive result display with band score (0-9)
- Summary cards showing:
  - Band score with interpretation
  - Correct answers
  - Incorrect answers
  - Unanswered questions
  - Total questions
- Three result tabs:
  - Detailed Results: Question-by-question breakdown
  - Incorrect Answers: Focus on mistakes
  - Statistics: Performance by question type
- Export results to JSON

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup
```bash
# Clone or download the application
cd ielts_reading_app

# Run the application
python main.py
```

## Usage

### 1. Creating a Reading Package

1. Launch the application: `python main.py`
2. Click "Content Editor"
3. Add reading content:
   - Enter explanation (e.g., "You should spend about 20 minutes...")
   - Enter title
   - Add paragraphs with titles and bodies
   - Click "Save Reading Content"
4. Add question groups:
   - Click "Add Question Group"
   - Enter explanation
   - Select question type
   - Add questions (minimum 2, maximum 10)
   - Add answers
   - Optionally add additional inputs (for matching questions)
   - Click "Save Question Group"
5. Save the package: File > Save Package

### 2. Taking a Test

1. Launch the application: `python main.py`
2. Click "Take Exam"
3. Select a reading package file (.json)
4. Click "Start Exam" to begin the timer
5. Read the passage (left side) and answer questions (right side)
6. Use highlighting tools to mark important text:
   - Select text to show highlight toolbar
   - Choose a color or remove highlight
7. Click "End Exam" when finished or let the timer expire

### 3. Viewing Results

Results are displayed automatically after exam submission showing:
- Band score (0-9 scale)
- Number of correct/incorrect/unanswered questions
- Detailed question-by-question feedback
- Performance statistics by question type
- Option to export results

### 4. Creating a Sample Package

1. Launch the application: `python main.py`
2. Click "Create Sample Package"
3. Choose where to save the sample file
4. Use this package to test the Exam Engine

## Architecture

### Data Models (models.py)
- `ReadingPackage`: Complete test package
- `ReadingContent`: Passage content with paragraphs
- `QuestionGroup`: Group of related questions
- `Question`: Individual question with answer
- `AnswerRecord`: User's answer to a question
- `EvaluationResult`: Complete test results
- `IELTSScoringRules`: Band score mapping

### Module Structure

```
ielts_reading_app/
├── main.py                 # Application launcher
├── models.py               # Data models
├── content_editor.py       # Content Editor module
├── exam_engine.py          # Exam Engine module
├── result_engine.py        # Result Engine module
└── README.md              # This file
```

## IELTS Band Score System

The application uses the official IELTS Academic Reading band score conversion:

| Correct Answers | Band Score |
|----------------|------------|
| 39-40          | 9.0        |
| 37-38          | 8.5        |
| 35-36          | 8.0        |
| 33-34          | 7.5        |
| 30-32          | 7.0        |
| 27-29          | 6.5        |
| 23-26          | 6.0        |
| 19-22          | 5.5        |
| 15-18          | 5.0        |
| 13-14          | 4.5        |
| 10-12          | 4.0        |
| 8-9            | 3.5        |
| 6-7            | 3.0        |
| 4-5            | 2.5        |
| 3              | 2.0        |
| 2              | 1.0        |
| 0-1            | 0.0        |

## Question Types Supported

The application supports all 11 IELTS Reading question types. For detailed input requirements for each type, see **QUESTION_TYPES_GUIDE.md**.

1. **Multiple Choice** - Select from options A, B, C, D
2. **True/False/Not Given** - Verify statements against the passage
3. **Yes/No/Not Given** - Author's opinion verification
4. **Matching Information** - Match information to paragraphs
5. **Matching Headings** - Match headings to paragraphs
6. **Matching Features** - Match features to options
7. **Matching Sentence Endings** - Complete sentences
8. **Sentence Completion** - Fill in missing words
9. **Summary/Table/Flow-chart Completion** - Complete diagrams
10. **Diagram Label Completion** - Label diagrams
11. **Short Answer Questions** - Brief text answers

## File Format

Reading packages are stored as JSON files with the following structure:

```json
{
  "package_id": "unique-id",
  "reading_content": {
    "explanation": "Instructions...",
    "title": "Passage Title",
    "paragraphs": [
      {
        "title": "Paragraph Title",
        "body": "Paragraph text..."
      }
    ]
  },
  "question_groups": [
    {
      "explanation": "Question instructions...",
      "type": "Multiple Choice",
      "questions": [
        {
          "question_id": "unique-question-id",
          "text": "Question text?",
          "answer": "correct answer"
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Issue: Application won't start
- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python -m tkinter`

### Issue: Can't load package
- Verify the JSON file is valid
- Check that the file follows the correct structure
- Try creating a new sample package

### Issue: Timer not working
- The timer runs in a separate thread
- Ensure your Python installation supports threading

## Future Enhancements

Potential improvements for future versions:
- User authentication system
- Database storage for packages and results
- Progress tracking across multiple tests
- More detailed analytics and reporting
- Export to PDF
- Audio for listening section
- Writing task modules
- Speaking task recording

## License

This is an educational application for IELTS test preparation.

## Credits

Developed based on Cambridge IELTS test format specifications.
