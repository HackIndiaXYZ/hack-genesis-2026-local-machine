import os
import ollama
import streamlit as st
file_path=st.text_input("Enter File Path:")
model="qwen2.5-coder:7b"
def attacker_agent(file_path:str):
    st.write("Attacker Agent looking for security flaws:")
    if not os.path.exists(file_path):
        print("File Path not Exists!")
        return False
    with open(file_path,"r") as f:
        code=f.read()
    prompt="""You are an offensive security auditor. Analyze the following source code and check for critical security vulnerabilities (such as SQL injection, insecure parameters, etc.).
    If vulnerabilities exist, explain them briefly and include the keyword VULNERABLE_FOUND. If the code is completely secure, output SECURE. code:{code}"""
    ans=ollama.chat(model=model,messages=[{"role":"user","content":prompt}])
    response=ans["message"]["content"]
    st.header("Attacker Report:")
    st.write(response)
    vulnerable="Vulnerable_Found" in response or "vulnerability" in response.lower()
    return vulnerable

def defender_agent(file_path:str):
    st.wrtie("Defender Agent Securing code at",{file_path})
    if not  os.path.exists(file_path):
        print("Error File path not found!")
        return
    with open(file_path,mode="r") as f:
        code=f.read()
    prompt=f"""You are an expert DevSecOps Ai. Analyze the following source code{code} and completely fix all the security vulnerabilities{code} Return only valid executable Python code wrapped in ''' python markdown blocks.Do not add extra chat text."""
    ans=ollama.chat(model=model,messages=[{"role":"user","content":prompt}])
    fixed_code=ans["message"]["content"]
    if "'''python" in fixed_code:
        fixed_code=fixed_code.split("'''python")[1].split("'''")[0].strip()
    elif "```" in fixed_code:
        fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
        return 
    with open(file_path,mode="w") as f:
        f.write(fixed_code)
        return
    st.write("Defender Success:Patched successfully")
