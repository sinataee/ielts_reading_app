#!/usr/bin/env python3
"""
Test script to verify IELTS Reading Application installation
Run this script to check if all components are working correctly
"""

import sys
import os

def check_python_version():
    """Check if Python version is adequate"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need 3.7+")
        return False

def check_tkinter():
    """Check if tkinter is available"""
    print("\nChecking tkinter...")
    try:
        import tkinter as tk
        print("✓ tkinter is available")
        return True
    except ImportError:
        print("✗ tkinter is not available")
        print("  Install: sudo apt-get install python3-tk (Linux)")
        print("           or reinstall Python with tcl/tk support")
        return False

def check_modules():
    """Check if all required modules can be imported"""
    print("\nChecking application modules...")
    modules = ['models', 'content_editor', 'exam_engine', 'result_engine', 'main']
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}.py - OK")
        except ImportError as e:
            print(f"✗ {module}.py - ERROR: {e}")
            all_ok = False
        except Exception as e:
            print(f"⚠ {module}.py - WARNING: {e}")
    
    return all_ok

def check_files():
    """Check if all required files exist"""
    print("\nChecking required files...")
    files = [
        'main.py',
        'models.py', 
        'content_editor.py',
        'exam_engine.py',
        'result_engine.py',
        'README.md',
        'requirements.txt',
        'QUICK_START.txt'
    ]
    
    all_ok = True
    for filename in files:
        if os.path.exists(filename):
            print(f"✓ {filename} - Found")
        else:
            print(f"✗ {filename} - Missing")
            all_ok = False
    
    return all_ok

def test_data_models():
    """Test basic data model functionality"""
    print("\nTesting data models...")
    try:
        from models import (
            ReadingPackage, ReadingContent, Paragraph,
            QuestionGroup, Question, QuestionType,
            IELTSScoringRules
        )
        
        # Test creating a simple package
        package = ReadingPackage()
        package.package_id = "test_123"
        
        rc = ReadingContent()
        rc.title = "Test Title"
        
        para = Paragraph()
        para.title = "Test Paragraph"
        para.body = "Test content"
        rc.paragraphs.append(para)
        
        package.reading_content = rc
        
        # Test scoring rules
        rules = IELTSScoringRules.get_academic_rules()
        if len(rules.mapping) > 0:
            print("✓ Data models working correctly")
            return True
        else:
            print("✗ Scoring rules not loaded")
            return False
            
    except Exception as e:
        print(f"✗ Data model test failed: {e}")
        return False

def test_package_serialization():
    """Test package save/load functionality"""
    print("\nTesting package serialization...")
    try:
        from models import ReadingPackage, ReadingContent
        import tempfile
        import os
        
        # Create a test package
        package = ReadingPackage()
        package.package_id = "serialize_test"
        package.reading_content = ReadingContent()
        package.reading_content.title = "Serialization Test"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        package.save_to_file(temp_path)
        
        # Load it back
        loaded_package = ReadingPackage.load_from_file(temp_path)
        
        # Clean up
        os.unlink(temp_path)
        
        if loaded_package.package_id == "serialize_test":
            print("✓ Package serialization working")
            return True
        else:
            print("✗ Package data mismatch after load")
            return False
            
    except Exception as e:
        print(f"✗ Serialization test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("IELTS Reading Application - Installation Verification")
    print("="*60)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Tkinter", check_tkinter()))
    results.append(("Files", check_files()))
    results.append(("Modules", check_modules()))
    results.append(("Data Models", test_data_models()))
    results.append(("Serialization", test_package_serialization()))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All tests passed! Your installation is ready.")
        print("\nTo start the application, run:")
        print("    python main.py")
    else:
        print("\n✗ Some tests failed. Please review errors above.")
        print("\nCommon solutions:")
        print("1. Install tkinter: sudo apt-get install python3-tk")
        print("2. Upgrade Python: python3 --version should be 3.7+")
        print("3. Check all files are in the same directory")
    
    print("\n")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
