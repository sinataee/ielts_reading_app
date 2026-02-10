# Contributing to IELTS Reading Test Application

First off, thank you for considering contributing to the IELTS Reading Test Application! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10, Ubuntu 22.04]
 - Python Version: [e.g. 3.9.7]
 - Application Version: [e.g. 1.2]

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List some examples** of how it would be used

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request**

## Development Process

### Setting Up Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/ielts-reading-app.git
cd ielts-reading-app
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

4. Verify installation:
```bash
python test_installation.py
```

### Coding Standards

#### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small (ideally < 50 lines)
- Use type hints where appropriate

#### Example:

```python
def calculate_band_score(correct_count: int, scoring_rules: IELTSScoringRules) -> float:
    """
    Calculate IELTS band score based on correct answer count.
    
    Args:
        correct_count: Number of correct answers
        scoring_rules: IELTS scoring rules object
        
    Returns:
        Band score as a float (0.0 - 9.0)
    """
    if correct_count in scoring_rules.mapping:
        return scoring_rules.mapping[correct_count]
    return 0.0
```

#### GUI Development

- Use consistent spacing and padding
- Follow the existing color scheme
- Ensure UI is responsive
- Test on different screen resolutions
- Add tooltips for complex features

#### File Organization

```
ielts-reading-app/
├── main.py              # Keep main launcher simple
├── models.py            # All data models here
├── content_editor.py    # Content Editor module
├── exam_engine.py       # Exam Engine module
├── result_engine.py     # Result Engine module
├── utils/               # Utility functions (if needed)
└── tests/               # Test files
```

### Testing

Before submitting a pull request:

1. **Run the installation test:**
```bash
python test_installation.py
```

2. **Manual testing checklist:**
- [ ] Create a new package
- [ ] Test all 11 question types
- [ ] Take a complete exam
- [ ] View results
- [ ] Export results
- [ ] Open and edit existing package
- [ ] Test on fullscreen mode
- [ ] Test highlighting feature
- [ ] Test table builder
- [ ] Test flowchart builder

3. **Edge cases to test:**
- [ ] Empty fields
- [ ] Maximum question counts (10 per group)
- [ ] Special characters in text
- [ ] Very long paragraphs
- [ ] Very long questions
- [ ] Timer expiration
- [ ] Pause/resume functionality

### Documentation

When adding new features:

1. **Update README_GITHUB.md** with new features
2. **Add to QUESTION_TYPES_GUIDE.md** if adding question types
3. **Update UPDATE_NOTES** with version changes
4. **Add inline comments** for complex logic
5. **Write docstrings** for all new functions

### Commit Messages

Use clear and descriptive commit messages:

```
feat: Add support for image insertion in diagrams
fix: Correct band score calculation for 40 questions
docs: Update installation guide for macOS
style: Format code according to PEP 8
refactor: Simplify question rendering logic
test: Add tests for Type 9 table builder
```

Prefix conventions:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Project Structure

### Core Modules

**models.py**
- Data structures and models
- Serialization/deserialization
- Validation logic

**content_editor.py**
- Rich text editing
- Question creation UI
- Table/flowchart builders
- Package management

**exam_engine.py**
- Exam interface
- Timer management
- Highlighting system
- Answer collection
- Visual rendering (tables, flowcharts)

**result_engine.py**
- Answer evaluation
- Score calculation
- Results display
- Statistics generation

### Adding New Features

#### Adding a New Question Type

1. Add to `QuestionType` enum in `models.py`
2. Update `create_answer_input()` in `exam_engine.py`
3. Add input form in `add_question_group()` in `content_editor.py`
4. Update `QUESTION_TYPES_GUIDE.md`
5. Add example in sample package generator

#### Adding New Highlighting Colors

1. Add color to `HighlightToolbar` in `exam_engine.py`
2. Add tag configuration in text widgets
3. Update `_color_to_name()` mapping

#### Adding Export Formats

1. Create new export function in `result_engine.py`
2. Add button in results UI
3. Handle file format conversion
4. Update documentation

## Feature Requests

We track feature requests through GitHub Issues. Before creating a new feature request:

1. **Search existing issues** to avoid duplicates
2. **Be specific** about the feature
3. **Explain the use case**
4. **Consider implementation** complexity

## Questions?

Feel free to create an issue with the label `question` if you need help.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
