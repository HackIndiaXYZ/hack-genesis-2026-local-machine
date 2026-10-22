import os
import ollama

# Configuration: Takes only the file path input
path = input("Enter Python file path to test/secure (e.g., C:\\Users\\ashmi\\Downloads\\untitled137.py): ").strip()
models = "qwen2.5-coder:7b"

def attacker_agent(file_path: str):
    print(f"\n[ATTACKER AGENT]: Inspecting code at {file_path} for security flaws...")
    if not os.path.exists(file_path):
        print("❌ Error: File not found!")
        return False
        
    with open(file_path, "r") as f:
        code = f.read()
        
    prompt = f"""You are an offensive security auditor. Analyze the following source code and check for critical security vulnerabilities (such as SQL injection, insecure parameters, etc.).
    If vulnerabilities exist, explain them briefly and include the keyword VULNERABLE_FOUND. If the code is completely secure, output SECURE.
    
    Source Code:
    {code}
    """
    
    ans = ollama.chat(model=models, messages=[{"role": "user", "content": prompt}])
    response_text = ans["message"]["content"]
    print(f"\n--- Attacker Audit Report ---\n{response_text}\n-----------------------------")
    
    # Check if the model flagged vulnerabilities
    is_vulnerable = "VULNERABLE_FOUND" in response_text or "vulnerability" in response_text.lower()
    return is_vulnerable

def defender_agent(file_path: str):
    print(f"\n[DEFENDER AGENT]: Securing source code at {file_path}...")
    if not os.path.exists(file_path):
        print("❌ Error: File not found!")
        return 
        
    with open(file_path, "r") as f:
        code = f.read()
        
    prompt = f"""You are an expert DevSecOps AI. Analyze the following source code and completely fix all security vulnerabilities (such as SQL injection, unescaped queries, etc.):
    
    {code}
    
    Return ONLY valid executable Python code wrapped in ```python markdown blocks. Do not add extra chat text.
    """
    
    ans = ollama.chat(model=models, messages=[{"role": "user", "content": prompt}])
    fixed_code = ans["message"]["content"]
    
    # Clean up markdown code blocks
    if "```python" in fixed_code:
        fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
    elif "```" in fixed_code:
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
        
    with open(file_path, "w") as f:
        f.write(fixed_code)
        
    print(f"✨ [DEFENDER SUCCESS]: Patched {file_path} successfully!")

def main():
    print("-" * 60)
    print("🚀 Path-Only Self-Healing Security Agent Demo")
    print("-" * 60)
    
    if not path or not os.path.exists(path):
        print(f"❌ Error: The path '{path}' is invalid or does not exist.")
        return

    input("\n[Press Enter] Step 1: Run Attacker Agent (Code Audit)...")
    vulnerable = attacker_agent(path)
    
    if not vulnerable:
        print("⚠️ Warning: Attacker agent did not detect vulnerabilities. Make sure your target file contains insecure code to demonstrate the fix.")

    input("\n[Press Enter] Step 2: Run Defender Agent (Auto-Patch)...")
    defender_agent(path)
    
    input("\n[Press Enter] Step 3: Re-run Attacker Agent (Verification Audit)...")
    attacker_agent(path)
    
    print("-" * 60)
    print("🏆 Demo Complete!")

if __name__ == "__main__":
    main()