from aimo_opt.optimize_aimo import AMCProcessor


def test_extract_final_answer_basic_code():
    """
    Test basic code block execution and answer extraction.
    """
    processor = AMCProcessor()
    
    response = '''
    Here's the solution:
    ```python
    x = 5 + 3
    print(x)
    ```
    '''
    assert processor.extract_final_answer(response) == "8"

def test_extract_final_answer_multiple_prints():
    """
    Test handling of multiple print statements in code block.
    """
    processor = AMCProcessor()
    
    response = '''
    ```python
    print("intermediate")
    print(42)
    print("final:", 79)
    ```
    '''
    assert processor.extract_final_answer(response) == "79"

def test_extract_final_answer_computation():
    """
    Test code block with mathematical computation.
    """
    processor = AMCProcessor()
    
    response = '''
    ```python
    import math
    result = math.factorial(4)
    print(result)
    ```
    '''
    assert processor.extract_final_answer(response) == "24"

def test_extract_final_answer_invalid_code():
    """
    Test handling of invalid Python code.
    """
    processor = AMCProcessor()
    
    response = '''
    ```python
    x = 1/0  # Division by zero error
    ```
    '''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

def test_extract_final_answer_non_numeric():
    """
    Test handling of non-numeric output.
    """
    processor = AMCProcessor()
    
    response = '''
    ```python
    print("hello")
    ```
    '''
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

def test_extract_final_answer_boxed():
    """
    Test extraction of boxed LaTeX answers.
    """
    processor = AMCProcessor()
    
    response = r'\boxed{42}'
    assert processor.extract_final_answer(response) == "42"

def test_extract_final_answer_code_and_boxed():
    """
    Test precedence of code output over boxed answer.
    """
    processor = AMCProcessor()
    
    response = '''
    ```python
    print(79)
    ```
    Final answer: \boxed{42}
    '''
    assert processor.extract_final_answer(response) == "79"

def test_extract_final_answer_invalid_format():
    """
    Test handling of invalid answer formats.
    """
    processor = AMCProcessor()
    
    response = "The answer is 42"
    assert processor.extract_final_answer(response) == processor.INVALID_ANS

def test_extract_final_answer_empty():
    """
    Test handling of empty or None input.
    """
    processor = AMCProcessor()
    
    assert processor.extract_final_answer("") == processor.INVALID_ANS
    assert processor.extract_final_answer(None) == processor.INVALID_ANS
