import os
import streamlit as st
from untitled143 import attacker_agent, defender_agent

def main():
    st.set_page_config(page_title="AI Attacker vs Defender", page_icon="🛡️", layout="wide")
    
    st.title("🛡️ AI Security Orchestrator: Attacker vs Defender")
    st.markdown("Automated vulnerability detection and self-healing code workflow.")
    st.markdown("---")
    
    # Target File Selection
    path = st.text_input("Enter target Python file path:", value="")
    
    if not path:
        st.info("Please enter a valid file path to begin.")
        return

    if not os.path.exists(path):
        st.error(f"❌ File not found at `{path}`. Please verify the location.")
        return

    st.success(f"📁 Target file verified: `{path}`")
    st.markdown("---")
    
    # --- STEP 1: Attacker Audit ---
    st.subheader("Step 1: Attacker Agent (Vulnerability Scan)")
    if st.button("Run Attacker Audit"):
        with st.spinner("Analyzing code for security flaws..."):
            is_vuln, report = attacker_agent(path)
            
        st.markdown(report)
        if is_vuln:
            st.error("🚨 Vulnerability Detected!")
        else:
            st.success("✅ Code appears secure.")
            
    st.markdown("---")

    # --- STEP 2: Defender Fix ---
    st.subheader("Step 2: Defender Agent (Auto-Patch)")
    if st.button("Run Defender Patch"):
        with st.spinner("Generating security patch..."):
            success, msg = defender_agent(path)
            
        if success:
            st.success(f"✨ {msg}")
        else:
            st.error(f"❌ {msg}")
            
    st.markdown("---")

    # --- STEP 3: Re-verify ---
    st.subheader("Step 3: Verification Audit (Re-Test)")
    if st.button("Verify Patch"):
        with st.spinner("Re-evaluating patched file..."):
            is_vuln, report = attacker_agent(path)
            
        st.markdown(report)
        if not is_vuln:
            st.success("🎉 Fix Verified! No vulnerabilities detected.")
        else:
            st.warning("⚠️ Flaws still detected after patching.")

if __name__ == "__main__":
    main()