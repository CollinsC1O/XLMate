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
    # Base templates based on category
    if category == "contracts":
        core_component = "on-chain state management and game determinism on the Stellar network"
        consequence = "malicious actors could potentially exploit the protocol logic causing unintended game outcomes or loss of staked XLM"
        risk = "financial loss and protocol insolvency"
        module_path = "contracts/game_contract/src"
        reference = "- [Soroban Smart Contract Documentation](https://soroban.stellar.org/docs)\n- [Stellar Developer Ecosystem](https://developers.stellar.org/docs/)"
    elif category == "backend":
        core_component = "the Actix-Rust server that handles real-time Websocket events, state sync, and matchmaking"
        consequence = "players may experience dropped games, unacceptable latency, or corrupt session states"
        risk = "poor user experience and data inconsistencies across the PostgreSQL database"
        module_path = "backend/modules/ or backend/src/"
        reference = "- [Actix-Web Framework](https://actix.rs/)\n- [Tokio Asynchronous Runtime](https://tokio.rs/)"
    elif category == "frontend":
        core_component = "the Next.js client interface ensuring smooth, premium Web3 user interactions"
        consequence = "users might face a substandard gaming experience with poor feedback on blockchain states"
        risk = "loss of user retention and confusion regarding their wallet transactions"
        module_path = "frontend/app/ and frontend/components/"
        reference = "- [Next.js Documentation](https://nextjs.org/docs)\n- [TailwindCSS Documentation](https://tailwindcss.com/docs)\n- [Stellar Freighter Wallet Integration](https://docs.freighter.app/)"
    else:
        # AI/Infra
        core_component = "the AI agent orchestration and automated deployment pipelines"
        consequence = "the AI co-pilot feature cannot reliably serve accurate chess moves or the deployment remains disjointed"
        risk = "unfair algorithmic advantages, broken AI integrations, or deployment bottlenecks"
        module_path = "agent-engines/ or root config files"
        reference = "- [Stockfish / Leela Chess Zero](https://stockfishchess.org/)\n- [PyTorch / Python WASM environments](https://pytorch.org/)"

    # Create dynamic values based on the title
    task_focus = title.split(":")[-1].strip() if ":" in title else title.replace("Contract: ", "").replace("Backend: ", "").replace("Frontend: ", "").replace("AI/Infra: ", "")
    missing_feature = f"a robust implementation of **{task_focus}**"
    target_behavior = f"fully integrate **{task_focus}** while maintaining high performance and security boundaries"

    body = f"""## 📖 Context and Rationale
The XLMate platform relies heavily on {core_component} to maintain robust operations. Currently, the implementation lacks {missing_feature}. This is a critical gap because {consequence}. In a high-stakes decentralized environment leveraging Stellar, we need to ensure that our architecture is strictly upheld at all times to prevent {risk}. Addressing this issue will massively improve the reliability and scalability of the platform for our growing community.

## 🛠️ Technical Implementation Details
To properly resolve this task, the contributor will need to interact with several key architectural layers. Please read the codebase thoroughly before making changes.

1. **Module Focus**: `{category}` layer (`{module_path}`)
2. **Current Workflow**: At present, the system defaults to basic or unoptimized pathways for this feature.
3. **Target Workflow**: We expect the new logic to {target_behavior}.
4. **Key Implementation Steps**:
   - Locate the primary functionality governing `{task_focus}`.
   - Refactor or introduce the necessary structs, interfaces, and logic blocks.
   - Ensure that the new changes are decoupled where possible, preventing monolithic dependencies.
   - For backend/contracts: Pay strict attention to memory utilization and deterministic execution.
   - For frontend: Ensure state management (e.g., React Context / Zustand) is cleanly updated without unnecessary rerenders.

## ✅ Acceptance Criteria
To ensure high quality, the PR must satisfy the following checks before it will be reviewed and merged:
- [x] **Core Logic**: Successfully implement `{task_focus}` as outlined in the Target Workflow.
- [x] **Test Coverage**: Provide comprehensive unit tests covering standard behavior, edge cases, and failure modes. We expect >85% branch coverage for new modules.
- [x] **Performance Validation**: Optimize the code for minimal overhead (e.g., Soroban gas/instructions limit, minimal latency in Actix, optimized asset loading in Next.js).
- [x] **Regression Check**: No regressions introduced into the existing `{category}` test suites. Ensure `cargo test` or `npm run test` strictly passes.
- [x] **Code Standards**: The code must precisely follow the established style guide (e.g., `rustfmt`, `clippy`, ESLint/Prettier) and include inline documentation for complex logic blocks.

## 📚 References & Resources
- Please refer to our [CONTRIBUTING.md](./CONTRIBUTING.md) for overarching repository guidelines.
{reference}

> **Note to Contributors**: We actively reward high-quality PRs. If you are blocked or need architectural clarification, please ping the maintainers in this thread or our community channels!
"""
    return body

def fix_issues():
    issues = get_issues()
    print(f"Loaded {len(issues)} issues total.")
    
    count_closed = 0
    count_updated = 0
    
    for issue in issues:
        title = issue["title"]
        number = issue["number"]
        labels = [l["name"] for l in issue.get("labels", [])]
        
        # 1. Close duplicates starting with "X/150", "[X/150]" or variations
        if re.match(r'^\[?\d{1,3}/150\]?', title.strip()):
            print(f"Closing duplicate issue #{number}: {title}")
            try:
                subprocess.run([GH_PATH, "issue", "close", str(number)], capture_output=True, check=True)
                count_closed += 1
                time.sleep(1) # Prevent secondary rate limit
            except subprocess.CalledProcessError as e:
                print(f"Error closing #{number}: {e}")
            continue
            
        # 2. Fix the titles that have (#XX) appended and update descriptions
        match = re.search(r'\s*\(\#\d+\)$', title)
        if match or ("contribution-ready" in labels):
            new_title = title
            if match:
                new_title = title[:match.start()].strip()
            
            category = "frontend"
            if "contracts" in labels: category = "contracts"
            elif "backend" in labels: category = "backend"
            elif "ai-infra" in labels: category = "ai-infra"
            
            new_body = generate_detailed_body(new_title, category)
            
            print(f"Updating issue #{number} -> New Title: '{new_title}'")
            try:
                cmd = [GH_PATH, "issue", "edit", str(number), "--title", new_title, "--body", new_body]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                count_updated += 1
                time.sleep(2) # Prevent secondary rate limit
            except subprocess.CalledProcessError as e:
                print(f"Error updating #{number}: {e.stderr}")

    print(f"\nDone! Closed {count_closed} duplicates. Updated {count_updated} issues with detailed descriptions and fixed titles.")

if __name__ == "__main__":
    fix_issues()
