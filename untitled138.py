import os
import requests
import ollama
import streamlit as st
"""url=st.text_input("ENter url:")
path=st.text_input("Enter File Path:")"""
url=input(("ENter url:"))
path=input("Enter Path:")
#
models=" qwen2.5-coder:7b"
def attacker_agent(endpoint:str=""):
    print(f"Attacker Agent:\n Scanning target{url}{endpoint}")
    prompt=f"You are a Offenive security agent",f"Aalyze the target web app at{url}{endpoint} Craft a generalized injection or input payload to test security posture.Return ONLY the raw payload string."
    ans=ollama.chat(model=models,messages=[{"role":"user","content":prompt}])
    payload=ans["message"]["content"].strip()
    res=requests.get(f"{url}{endpoint}",params={"input":payload})
    return res.status_code,res.text
def defender_agent():
    print(f"\n Defender Agent:Inspecting source code at {path}")
    if not os.path.exists(path):
        print("File not Eexist!")
        return 
    with open(path,"r") as f:
        code=f.read()
    prompt=f"""You are an expert DevSecOps AI. Analyze the following source code and fix any security vulnerabilities:{code}
    Return ONLY valid executable code wrapped in ```python markdown blocks.
    """
    ans=ollama.chat(model=models,messages=[{"role":"user","content":prompt}])
    fixed_code=ans["message"]["content"]
    if "'''python" in fixed_code:
        fixed_code=fixed_code.split("'''python")[1].split("'''")[0].strip()
        
    with open(path,"w") as f:
        f.write()
        print("[DEFENDER SUCCESS]: Patched {path} successfully!")