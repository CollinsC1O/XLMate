import json
import subprocess
import time
import re

GH_PATH = r"C:\Program Files\GitHub CLI\gh.exe"

def get_issues():
    cmd = [GH_PATH, "issue", "list", "--limit", "1000", "--json", "number,title"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def clean():
    issues = get_issues()
    closed_count = 0
    updated_count = 0
    
    # Pattern for the duplicates to CLOSE: [1/150], 1/150, [10/150] etc.
    duplicate_pattern = re.compile(r'^\[?\d{1,3}/150\]?')
    
    # Pattern for removing the (#1) from the GOOD issues
    cleanup_pattern = re.compile(r'\s*\(\#\d+\)$')

    for issue in issues:
        number = issue["number"]
        title = issue["title"].strip()
        
        if duplicate_pattern.match(title):
            print(f"Closing duplicate: #{number} - {title}")
            subprocess.run([GH_PATH, "issue", "close", str(number)], capture_output=True)
            closed_count += 1
            time.sleep(1) # throttler
        elif cleanup_pattern.search(title):
            new_title = cleanup_pattern.sub("", title).strip()
            print(f"Cleaning title: #{number} - {title} -> {new_title}")
            subprocess.run([GH_PATH, "issue", "edit", str(number), "--title", new_title], capture_output=True)
            updated_count += 1
            time.sleep(1) # throttler

    print(f"Done. Closed {closed_count} duplicates and cleaned {updated_count} titles.")

if __name__ == "__main__":
    clean()
