import os
import ollama

MODEL = "qwen2.5-coder:7b"

def attacker_agent(file_path: str):
    """
    Scans the given file for security vulnerabilities using the LLM.
    Returns a tuple: (is_vulnerable: bool, analysis_report: str)
    """
    if not os.path.exists(file_path):
        return False, "Error: File path does not exist."
        
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    prompt = f"""You are an offensive security auditor. Analyze the following source code and check for critical security vulnerabilities (such as SQL injection, command injection, insecure parameters, etc.).

If vulnerabilities exist, explain them briefly and include the keyword VULNERABLE_FOUND. 
If the code is completely secure, output SECURE.

Code:
{code}"""
    
    try:
        ans = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        response = ans["message"]["content"]
        is_vulnerable = "VULNERABLE_FOUND" in response or "vulnerability" in response.lower()
        return is_vulnerable, response
    except Exception as e:
        return False, f"Ollama execution failed: {str(e)}"


def defender_agent(file_path: str):
    """
    Analyzes the vulnerable code, generates a secure fix, and overwrites the target file.
    Returns a tuple: (success: bool, status_message: str)
    """
    if not os.path.exists(file_path):
        return False, "Error: Target file not found."
        
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    prompt = f"""You are an expert DevSecOps AI. Analyze the following source code and fix all security vulnerabilities:
{code} 

Return only valid executable Python code wrapped in ```python markdown blocks. Do not include extra conversational text."""
    
    try:
        ans = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        fixed_code = ans["message"]["content"]
        
        # Parse output to extract pure python code inside codeblocks
        if "```python" in fixed_code:
            fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
        elif "```" in fixed_code:
            fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
            
        # Write patched code back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)
            
        return True, "Code successfully patched and overwritten."
    except Exception as e:
        return False, f"Failed to patch code: {str(e)}"