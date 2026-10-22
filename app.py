import os
from flask import Flask, render_template_string, request
from Agants import type_classifier, attacker_agent, defender_agent
app = Flask(__name__)
CYBER_DASHBOARD_TEMPLATE = """
<html>
<html>
<head>
    <title>Attacker vs Defender</title>
    <style>
        :root {
            --bg: #011e49;
            --surface:rgb(0, 0, 0);
            --border: #1a2a3f;
            --text: #d0dce8;
            --muted: #6b7c93;
            --accent: #bbff00;
            --attacker: #ff2d55;
            --defender: #00b4ff;
            --glow-attacker: 0 0 18px rgba(255, 45, 83, 0.673);
            --glow-defender: 0 0 18px rgba(0, 180, 255, 0.25);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'SF Mono', 'Fira Code', 'Courier New',monospace;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
            background-image:
                radial-gradient(ellipse at top, #0d1a2b 0%, transparent 60%),
                linear-gradient(180deg, #02060c 0%, #050b14 100%);
        }

        /* Header */
        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #00e5a0, #00b4ff);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: 800;
            color: #02060c;
        }

        .logo h1 {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #e8f0f8;
        }

        .logo span {
            font-size: 0.7rem;
            color: var(--muted);
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .status-pill {
            font-size: 0.7rem;
            padding: 5px 12px;
            border-radius: 20px;
            background: rgba(0, 229, 160, 0.1);
            border: 1px solid rgba(0, 229, 160, 0.3);
            color: var(--accent);
            letter-spacing: 0.5px;
        }

        /* Config */
        .config {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 24px;
        }

        .config-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: var(--muted);
            margin-bottom: 10px;
        }

        .path-row {
            display: flex;
            gap: 12px;
            margin-bottom: 18px;
        }

        input[type="text"] {
            flex: 1;
            background: #050b14;
            border: 1px solid #1e3248;
            color: var(--accent);
            padding: 12px 16px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input[type="text"]:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(0, 229, 160, 0.12);
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .btn {
            background: transparent;
            border: 1px solid #2a3f55;
            color: var(--text);
            padding: 10px 18px;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.18s ease;
            letter-spacing: 0.3px;
        }

        .btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(0, 229, 160, 0.06);
        }

        .btn-primary {
            border-color: var(--attacker);
            color: var(--attacker);
        }

        .btn-primary:hover {
            background: rgba(255, 45, 85, 0.12);
            box-shadow: var(--glow-attacker);
        }

        .btn-secondary {
            border-color: var(--defender);
            color: var(--defender);
        }

        .btn-secondary:hover {
            background: rgba(0, 180, 255, 0.12);
            box-shadow: var(--glow-defender);
        }

        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media (max-width: 860px) {
            .grid { grid-template-columns: 1fr; }
            .path-row { flex-direction: column; }
        }

        .panel {
            background: var(--surface);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            min-height: 420px;
            border: 1px solid var(--border);
        }

        .panel.attacker {
            border-color: rgba(255, 45, 85, 0.25);
            box-shadow: inset 0 1px 0 rgba(255, 45, 85, 0.08);
        }

        .panel.defender {
            border-color: rgba(0, 180, 255, 0.25);
            box-shadow: inset 0 1px 0 rgba(0, 180, 255, 0.08);
        }

        .panel-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 18px;
            background: rgba(0, 0, 0, 0.25);
            border-bottom: 1px solid var(--border);
        }

        .panel-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.4px;
        }

        .panel.attacker .panel-title { color: var(--attacker); }
        .panel.defender .panel-title { color: var(--defender); }

        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .panel.attacker .dot {
            background: var(--attacker);
            box-shadow: 0 0 8px var(--attacker);
        }

        .panel.defender .dot {
            background: var(--defender);
            box-shadow: 0 0 8px var(--defender);
        }

        .badge {
            font-size: 0.65rem;
            padding: 3px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 700;
        }

        .badge-danger {
            background: rgba(255, 45, 85, 0.15);
            color: var(--attacker);
            border: 1px solid rgba(255, 45, 85, 0.4);
        }

        .badge-safe {
            background: rgba(0, 229, 160, 0.12);
            color: var(--accent);
            border: 1px solid rgba(0, 229, 160, 0.35);
        }

        .badge-idle {
            background: rgba(107, 124, 147, 0.12);
            color: var(--muted);
            border: 1px solid rgba(107, 124, 147, 0.3);
        }

        .terminal {
            flex: 1;
            padding: 16px 18px;
            font-size: 0.8rem;
            line-height: 1.55;
            overflow-y: auto;
            white-space: pre-wrap;
            color: #b8c9d9;
            background: #03080f;
        }

        .footer {
            margin-top: 22px;
            text-align: center;
            font-size: 0.7rem;
            color: var(--muted);
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <div class="logo">
           
            <div>
                <span>Attacker Defender Agents</span>
            </div>
        </div>
        <div class="status-pill">● SYSTEM ONLINE</div>
    </div>

    <form method="POST">
        <div class="config">
            <div class="config-label">Target Source File</div>
            <div class="path-row">
                <input type="text"
                       id="path"
                       name="path"
                       value="{{ path }}"
                       placeholder="/path/to/target_app.py"
                       required
                       autocomplete="off">
            </div>

            <div class="actions">
                <button type="submit" name="action" value="detect" class="btn"> Detect Language</button>
                <button type="submit" name="action" value="attack" class="btn btn-primary">Run Attacker Audit</button>
                <button type="submit" name="action" value="defend" class="btn btn-secondary"> Run Defender Patch</button>
                <button type="submit" name="action" value="verify" class="btn">Verify Fix</button>
            </div>
        </div>
    </form>

    <div class="grid">
        <!-- Attacker -->
        <div class="panel attacker">
            <div class="panel-head">
                <div class="panel-title">
                    <span class="dot"></span>
                    Attacker Agent
                </div>
                {% if action_type in ['attack', 'verify'] %}
                    {% if is_vuln %}
                        <span class="badge badge-danger">Vulnerable</span>
                    {% else %}
                        <span class="badge badge-safe">Secure</span>
                    {% endif %}
                {% else %}
                    <span class="badge badge-idle">Standby</span>
                {% endif %}
            </div>
            <div class="terminal">{{ attacker_output or 'Awaiting target...\n→ Execute “Run Attacker Audit” to begin recon.' }}</div>
        </div>

        <!-- Defender -->
        <div class="panel defender">
            <div class="panel-head">
                <div class="panel-title">
                    <span class="dot"></span>
                    Defender Agent
                </div>
                {% if action_type == 'defend' %}
                    <span class="badge badge-safe">Patched</span>
                {% else %}
                    <span class="badge badge-idle">Standby</span>
                {% endif %}
            </div>
            <div class="terminal">{{ defender_output or 'Standing by...\n→ Execute “Run Defender Patch” to remediate.' }}</div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    path = ""
    attacker_output = ""
    defender_output = ""
    action_type = ""
    is_vuln = False
    
    if request.method == "POST":
        path = request.form.get("path", "").strip()
        action = request.form.get("action")
        action_type = action
        
        if not path or not os.path.exists(path):
            attacker_output = f"Error: Target file path '{path}' does not exist."
        else:
            if action == "detect":
                success, info = type_classifier(path)
                attacker_output = f"Language Classification Protocol Initialized...\n\nResult: Identified language as [{info}]" if success else f"❌ {info}"
                
            elif action == "attack":
                is_vuln, report = attacker_agent(path)
                attacker_output = report
                
            elif action == "defend":
                success, msg = defender_agent(path)
                defender_output = f"Security Alert Received! Analyzing traceback and AST...\n\nStatus: {msg}\nAction: Source code safely rewritten & synchronized." if success else f"❌ Patch Failed: {msg}"
                
            elif action == "verify":
                is_vuln, report = attacker_agent(path)
                attacker_output = f"--- POST-REMEDIATION VERIFICATION AUDIT ---\n\n" + report
                defender_output = f"Verification check completed.\nTarget Status Vulnerable: {is_vuln}\nResult: {'⚠️ Flaws persist.' if is_vuln else '🎉 Patch confirmed successful. Zero residual flags.'}"

    return render_template_string(
        CYBER_DASHBOARD_TEMPLATE, 
        path=path, 
        attacker_output=attacker_output, 
        defender_output=defender_output, 
        action_type=action_type, 
        is_vuln=is_vuln
    )

if __name__ == "__main__":
    app.run()