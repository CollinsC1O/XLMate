import json
import subprocess
import time
import re

GH_PATH = r"C:\Program Files\GitHub CLI\gh.exe"

def get_issues():
    cmd = [GH_PATH, "issue", "list", "--limit", "1000", "--json", "number,title,labels"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def generate_detailed_body(title, category):
    # Templates for rich descriptions
    if category == "contracts":
        desc = "This task involves critical on-chain logic for game settlement and staking on Stellar."
        module = "contracts/game_contract/src"
    elif category == "backend":
        desc = "Focus on scaling the Actix-Rust server and managing real-time WebSocket state synchronization."
        module = "backend/modules/"
    elif category == "frontend":
        desc = "Enhance the user experience with premium Next.js UI components and fluid Web3 interactions."
        module = "frontend/app/"
    else:
        desc = "Orchestrate AI engines and deployment pipelines for the XLMate intelligent co-pilot."
        module = "agent-engines/"

    return f"""## 📖 Context
{desc}

## 🛠️ Tasks
- Analyze the existing code in `{module}`.
- Implement the feature following our established design patterns.
- Ensure efficient resource utilization (Gas/CPU).

## ✅ Acceptance Criteria
- Code is well-documented and follows style guides.
- Unit tests cover standard and edge cases.
- Feature is fully integrated and tested with `cargo` or `npm`.
"""

def final_fix():
    issues = get_issues()
    print(f"Processing {len(issues)} issues...")
    
    dup_pattern = re.compile(r'^\[?\d{1,3}/150\]?')
    cleanup_pattern = re.compile(r'\s*\(\#\d+\)$')

    for issue in issues:
        number = issue["number"]
        title = issue["title"].strip()
        labels = [l["name"] for l in issue.get("labels", [])]
        
        # 1. Close duplicates
        if dup_pattern.match(title):
            print(f"Closing duplicate #{number}")
            subprocess.run([GH_PATH, "issue", "close", str(number)], capture_output=True)
            time.sleep(1)
            continue
            
        # 2. Fix title and add body
        new_title = cleanup_pattern.sub("", title).strip()
        
        cat = "frontend"
        if "contracts" in labels: cat = "contracts"
        elif "backend" in labels: cat = "backend"
        elif "ai-infra" in labels: cat = "ai-infra"
        
        body = generate_detailed_body(new_title, cat)
        
        print(f"Updating #{number}: {new_title}")
        subprocess.run([GH_PATH, "issue", "edit", str(number), "--title", new_title, "--body", body], capture_output=True)
        time.sleep(1)

if __name__ == "__main__":
    final_fix()
