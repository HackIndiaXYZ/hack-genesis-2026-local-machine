import os
import ollama

model = "qwen2.5-coder:7b"

def type_classifier(file_path: str):
    """
    Classifies the programming language of the given file using the LLM.
    Returns a tuple: (success: bool, language_info: str)
    """
    if not os.path.exists(file_path):
        return False, "Error: File path does not exist."
        
    with open(file_path, mode="r", encoding="utf-8") as f:
        code = f.read()
        
    prompt = f"You are an expert programming language classifier. Analyze the following code snippet and determine the programming language it is written in. Return only the name of the language.\n\nCode:\n{code}"
    
    try:
        ans = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        response = ans["message"]["content"].strip()
        return True, response
    except Exception as e:
        return False, f"Ollama execution failed: {str(e)}"

def attacker_agent(file_path: str):
    """
    Scans the given file for security vulnerabilities using the LLM.
    Returns a tuple: (is_vulnerable: bool, analysis_report: str)
    """
    if not os.path.exists(file_path):
        return False, "Error: File path does not exist."
        
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    prompt = f"""You are an offensive security auditor. Analyze the following source code and check for critical security vulnerabilities (such as SQL injection, XSS, command injection, insecure parameters, etc.).

If vulnerabilities exist, explain them briefly and include the keyword VULNERABLE_FOUND. 
If the code is completely secure, output SECURE.

Code:
{code}"""
    
    try:
        ans = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        response = ans["message"]["content"]
        is_vulnerable = "VULNERABLE_FOUND" in response or "vulnerability" in response.lower()
        return is_vulnerable, response
    except Exception as e:
        return False, f"Ollama execution failed: {str(e)}"

def defender_agent(file_path: str):
    """
    Analyzes vulnerable code, generates a secure fix in its original language, 
    and overwrites the target file using a universal markdown code-block parser.
    """
    if not os.path.exists(file_path):
        return False, "Error: Target file not found."
        
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    prompt = f"""You are an expert DevSecOps AI. Analyze the following source code, fix all security vulnerabilities, and keep the code in its exact original programming language:
{code} 

Return only valid executable code wrapped in markdown code blocks (e.g., ```python, ```javascript, ```cpp, etc.). Do not include extra conversational text."""
    
    try:
        ans = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        fixed_code = ans["message"]["content"]
        
        # UNIVERSAL MARKDOWN PARSER: Works for Python, JS, C++, Java, PHP, etc.
        if "```" in fixed_code:
            parts = fixed_code.split("```")
            if len(parts) >= 2:
                block_content = parts[1]
                if "\n" in block_content:
                    fixed_code = block_content.split("\n", 1)[1].strip()
                else:
                    fixed_code = block_content.strip()
                    
        # Write patched code back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code)
            
        return True, "Code successfully patched and overwritten in its native language."
    except Exception as e:
        return False, f"Failed to patch code: {str(e)}"