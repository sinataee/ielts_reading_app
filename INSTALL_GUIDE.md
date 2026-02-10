# IELTS Reading Test Application
# Complete Installation and Usage Guide

## INSTALLATION INSTRUCTIONS

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Step 1: Verify Python Installation
```bash
python --version
# or
python3 --version
```

You should see Python 3.7 or higher.

### Step 2: Install tkinter (if needed)

**On Ubuntu/Debian Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**On Fedora/RedHat Linux:**
```bash
sudo dnf install python3-tkinter
```

**On macOS:**
tkinter should be included with Python. If not:
```bash
brew install python-tk
```

**On Windows:**
tkinter is included with Python installer. If missing:
- Download Python from python.org
- Run installer
- Check "tcl/tk and IDLE" option
- Complete installation

### Step 3: Verify Installation
```bash
cd ielts_reading_app
python test_installation.py
```

This will check all components and report any issues.

### Step 4: Run the Application
```bash
python main.py
```

## APPLICATION STRUCTURE

```
ielts_reading_app/
│
├── main.py                    # Main application launcher
├── models.py                  # Data models and structures
├── content_editor.py          # Content creation module
├── exam_engine.py             # Test-taking module
├── result_engine.py           # Results and scoring module
├── test_installation.py       # Installation verification
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── QUICK_START.txt           # Quick start guide
└── INSTALL_GUIDE.md          # This file
```

## USAGE WORKFLOWS

### Workflow 1: Create and Take Your First Test

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Create Sample Package** (Recommended for first time)
   - Click "Create Sample Package"
   - Save as "my_first_test.json"
   - Close the save dialog

3. **Take the Test**
   - Click "Take Exam"
   - Select "my_first_test.json"
   - Click "Start Exam"
   - Answer the questions
   - Click "End Exam" when done

4. **Review Results**
   - View your band score
   - Check detailed feedback
   - Review incorrect answers

### Workflow 2: Create Custom Reading Package

1. **Open Content Editor**
   - Launch main.py
   - Click "Content Editor"

2. **Add Reading Content**
   - Enter explanation text
   - Enter passage title
   - Click "Add Paragraph" multiple times
   - Fill in paragraph titles and bodies
   - Use formatting toolbar (Bold, Italic, Headers)
   - Click "Save Reading Content"

3. **Add Question Groups**
   - Click "Add Question Group"
   - Enter group explanation
   - Select question type from dropdown
   - Add at least 2 questions (max 10)
   - Enter answers
   - For matching questions, add additional inputs
   - Click "Save Question Group"
   - Repeat for multiple question groups

4. **Save Package**
   - Go to File > Save Package
   - Choose location and filename
   - Click Save

### Workflow 3: Taking a Timed Exam

1. **Load Package**
   - Launch exam_engine.py or use main menu
   - Select package file

2. **Exam Interface**
   - Left side: Reading passage
   - Right side: Questions
   - Top: Timer and controls

3. **During Exam**
   - Read passage carefully
   - Highlight important text (select text, choose color)
   - Answer questions in any order
   - Use Pause button if needed
   - Watch the timer

4. **Submit**
   - Click "End Exam" to submit early
   - Or wait for timer to expire
   - Automatic submission when time is up

### Workflow 4: Analyzing Results

1. **Summary View**
   - Band score (0-9)
   - Correct/Incorrect/Unanswered counts
   - Quick performance overview

2. **Detailed Results Tab**
   - Question-by-question breakdown
   - Your answer vs correct answer
   - Marked as correct/incorrect

3. **Incorrect Answers Tab**
   - Focus on mistakes only
   - Review what you got wrong
   - Learn from errors

4. **Statistics Tab**
   - Performance by question type
   - Accuracy percentages
   - Overall statistics

5. **Export Results**
   - Click "Export Results"
   - Save as JSON file
   - Track progress over time

## QUESTION TYPES REFERENCE

### Type 1: Multiple Choice
- Select A, B, C, or D
- Radio button interface

### Type 2: True/False/Not Given
- Verify factual statements
- Three-option selector

### Type 3: Yes/No/Not Given
- Author's opinion/view
- Three-option selector

### Type 4: Matching Information
- Match info to paragraphs
- Dropdown selector

### Type 5: Matching Headings
- Match headings to paragraphs
- Dropdown selector

### Type 6: Matching Features
- Match features to options
- Dropdown selector

### Type 7: Matching Sentence Endings
- Complete sentences
- Dropdown selector

### Type 8: Sentence Completion
- Fill in missing words
- Text input field

### Type 9: Summary/Table/Flow-chart Completion
- Complete diagrams/tables
- Multiple text fields

### Type 10: Diagram Label Completion
- Label diagram parts
- Text fields

### Type 11: Short Answer Questions
- Brief text answers
- Text input field
- Word limit specified

## KEYBOARD SHORTCUTS

### Content Editor
- **Ctrl+N**: New Package
- **Ctrl+O**: Open Package
- **Ctrl+S**: Save Package
- **Ctrl+B**: Bold (when text selected)
- **Ctrl+I**: Italic (when text selected)

### Exam Engine
- **Space**: Pause/Resume (when Start clicked)
- **Enter**: Submit answer (in text fields)
- **Tab**: Move to next field
- **Ctrl+A**: Select all (in text fields)

### General
- **Alt+F4** (Windows/Linux): Close window
- **Cmd+Q** (macOS): Quit application
- **Esc**: Close dialogs

## TIPS AND BEST PRACTICES

### Content Creation Tips
1. Write clear, unambiguous questions
2. Make answers specific and exact
3. Use 2-4 paragraphs for passages
4. Mix different question types
5. Test your package before distributing

### Test-Taking Tips
1. Read instructions carefully
2. Skim passage first, then read in detail
3. Highlight keywords and key information
4. Manage your time (20 minutes per passage)
5. Answer all questions (no penalty for guessing)
6. Check answers before submitting

### Study Tips
1. Practice regularly (3-4 times per week)
2. Review incorrect answers
3. Focus on weak question types
4. Time yourself strictly
5. Track your band score progress

## TROUBLESHOOTING

### Problem: "tkinter not found"
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk

# Windows - Reinstall Python with tcl/tk
```

### Problem: Application freezes during exam
**Solution:**
1. Close application completely
2. Restart application
3. Load package again
4. If persists, check system resources

### Problem: Can't load package file
**Solution:**
1. Verify file is .json format
2. Check file isn't corrupted
3. Try creating new sample package
4. Validate JSON syntax online

### Problem: Answers not being recorded
**Solution:**
1. Make sure exam is started (click "Start Exam")
2. Click inside answer fields
3. For dropdown, select an option
4. For text fields, type and press Enter

### Problem: Timer not starting
**Solution:**
1. Click "Start Exam" button
2. Check if Python has threading support
3. Restart application

### Problem: Wrong band score
**Solution:**
1. Verify you're using Academic scoring
2. Check answer accuracy
3. Review evaluation algorithm
4. Count correct answers manually

## FILE FORMATS

### Package File (.json)
```json
{
  "package_id": "unique-identifier",
  "reading_content": {
    "explanation": "Instructions for candidates",
    "title": "Passage Title",
    "paragraphs": [
      {
        "title": "Section Title",
        "body": "Paragraph text content..."
      }
    ]
  },
  "question_groups": [
    {
      "explanation": "Question instructions",
      "type": "Multiple Choice",
      "questions": [
        {
          "question_id": "q1",
          "text": "Question text?",
          "answer": "Correct answer"
        }
      ],
      "additional_inputs": {
        "input_type": "Type4",
        "data": {"infoList": ["Item 1", "Item 2"]}
      }
    }
  ],
  "created_at": "2025-02-10T10:30:00"
}
```

### Results File (.json)
```json
{
  "correct_count": 25,
  "incorrect_count": 8,
  "unanswered_count": 7,
  "total_questions": 40,
  "band_score": 6.5,
  "per_question_feedback": [
    {
      "question_id": "q1",
      "is_correct": true,
      "correct_answer": "answer",
      "user_answer": "answer"
    }
  ]
}
```

## ADVANCED FEATURES

### Rich Text Formatting
- Bold: Select text, click B button
- Italic: Select text, click I button
- Font size: Select size from dropdown
- Headers: H1 (large), H2 (medium)
- Alignment: Left, Center

### Text Highlighting
- Yellow: General highlighting
- Green: Key facts
- Blue: Definitions
- Pink: Important names/dates
- Remove: Clear highlighting

### Answer Normalization
- Case-insensitive comparison
- Leading/trailing spaces removed
- Common punctuation ignored
- "Answer" matches "answer" matches "ANSWER"

## PERFORMANCE OPTIMIZATION

### For Large Packages (50+ questions)
1. Use pagination if needed
2. Close other applications
3. Ensure adequate RAM (2GB+)
4. Use SSD for faster file loading

### For Smooth Experience
1. Close unnecessary programs
2. Use modern Python version (3.9+)
3. Keep packages under 20 question groups
4. Limit paragraph length to 500 words

## SCORING SYSTEM

### IELTS Academic Reading Band Scores
- 39-40 correct → Band 9.0 (Expert)
- 37-38 correct → Band 8.5 (Very Good)
- 35-36 correct → Band 8.0 (Very Good)
- 33-34 correct → Band 7.5 (Good)
- 30-32 correct → Band 7.0 (Good)
- 27-29 correct → Band 6.5 (Competent)
- 23-26 correct → Band 6.0 (Competent)
- 19-22 correct → Band 5.5 (Modest)
- 15-18 correct → Band 5.0 (Modest)
- 13-14 correct → Band 4.5 (Limited)
- 10-12 correct → Band 4.0 (Limited)

## GETTING HELP

### Resources
1. README.md - Comprehensive documentation
2. QUICK_START.txt - Quick reference
3. models.py - Data structure documentation
4. Test packages - Example content

### Community Support
- Review module docstrings
- Check error messages
- Run test_installation.py
- Examine sample packages

## LICENSE AND CREDITS

This is an educational application for IELTS test preparation.
Based on Cambridge IELTS test format specifications.

Developed following software engineering best practices:
- Modular architecture
- Clear separation of concerns
- Comprehensive documentation
- Thorough testing

## NEXT STEPS

1. Complete test_installation.py successfully
2. Create sample package
3. Take practice test
4. Review results
5. Create custom packages
6. Practice regularly
7. Track progress

Good luck with your IELTS preparation! 🎓
