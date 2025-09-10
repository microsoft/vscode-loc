#!/usr/bin/env python3
"""
Script to analyze active branches and count commits not pushed to main yet.
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

def run_git_command(command: List[str], cwd: str = ".") -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        return ""

def get_branch_info() -> List[Dict]:
    """Get information about all branches using git commands."""
    branches = []
    
    # Get all remote branches
    output = run_git_command(["git", "branch", "-r", "--format=%(refname:short)|%(committerdate:iso)|%(authorname)"])
    
    for line in output.split('\n'):
        if line.strip() and not line.startswith('origin/HEAD'):
            parts = line.split('|')
            if len(parts) >= 2:
                branch_name = parts[0].replace('origin/', '')
                commit_date = parts[1] if len(parts) > 1 else ""
                author = parts[2] if len(parts) > 2 else ""
                
                branches.append({
                    'name': branch_name,
                    'commit_date': commit_date,
                    'author': author
                })
    
    return branches

def is_branch_active(branch_info: Dict, days_threshold: int = 90) -> bool:
    """Determine if a branch is considered active based on recent commits."""
    if branch_info['name'] == 'main':
        return False  # main is not considered an "active" branch for this analysis
    
    try:
        if branch_info['commit_date']:
            commit_date = datetime.fromisoformat(branch_info['commit_date'].replace('Z', '+00:00'))
            threshold_date = datetime.now().replace(tzinfo=commit_date.tzinfo) - timedelta(days=days_threshold)
            return commit_date > threshold_date
    except:
        pass
    
    # If we can't parse the date, consider it active to be safe
    return True

def count_commits_ahead_of_main(branch_name: str) -> int:
    """Count how many commits a branch is ahead of main."""
    try:
        # First, make sure we have the main branch
        run_git_command(["git", "fetch", "origin", "main:main"])
        
        # Count commits that are in the branch but not in main
        output = run_git_command(["git", "rev-list", "--count", f"origin/{branch_name}", "^main"])
        return int(output) if output.isdigit() else 0
    except:
        # If we can't compare with main, try to get total commit count on branch
        try:
            output = run_git_command(["git", "rev-list", "--count", f"origin/{branch_name}"])
            return int(output) if output.isdigit() else 0
        except:
            return 0

def main():
    """Main function to analyze branches."""
    print("🔍 Analyzing branches in the vscode-loc repository...")
    print("=" * 60)
    
    # Get branch information
    branches = get_branch_info()
    
    if not branches:
        print("No branches found. Trying alternative approach...")
        # Fallback: use the GitHub API data we know exists
        branch_names = [
            "add-new-language-cs",
            "add-new-language-en-gb", 
            "copilot/fix-ab46561c-739e-48bf-b49a-8dad647f03e4",
            "copilot/fix-c56e5d2e-77f6-420c-9c39-bdf3c624d286",
            "copilot/fix-fb52f354-8bab-481f-8e4d-38971e4030f0",
            "release/1.40", "release/1.41", "release/1.42", "release/1.43", 
            "release/1.44", "release/1.45", "release/1.46", "release/1.49", 
            "release/1.50", "release/1.52", "release/1.53",
            "update-localization-files-microsoft-vscode-loc-drop-4ae031e35a51b2133477b43c7863ac97d057f95c",
            "update-localization-files-microsoft-vscode-loc-drop-6ab898af3499236f8834a1305d7a2660d4540375",
            "update-localization-files-microsoft-vscode-loc-drop-63eb2b98af5cbd3b5dde526882dd2cecf3c4976b",
            "update-localization-files-microsoft-vscode-loc-drop-424b73e3cf23e87c82d2eeda28451a50a8c7f82a",
            "update-localization-files-microsoft-vscode-loc-drop-6382cfcf9163c032791bb466c52ac08f36638331",
            "update-localization-files-microsoft-vscode-loc-drop-bcafc0aec2dc23cb4227d666cb0d9ff05666e67b",
            "update-localization-files-microsoft-vscode-loc-drop-c0bd77a2c9aee15711b37b99cabe1b84825f23e4",
            "update-localization-files-microsoft-vscode-loc-drop-c00c1121225a8971631d49870d8a32c42dbe13ff",
            "update-localization-files-microsoft-vscode-loc-drop-e9b63e032468ca5e4e73ee230c72e6ad16f4ac59",
            "update-localization-files-microsoft-vscode-loc-drop-ef0ff67b17a06d554b85165e3b8ab3a827bf75e0",
            "update-localization-files-microsoft-vscode-loc-drop-efdb9ba1c3980129a0970d974717832b099b5bdf",
            "update-localization-files-microsoft-vscode-loc-drop-fef9c1ad4839f2777875e0b6e08e106c7100f5e7",
            "users/merlinbot/1es-pt-auto-baselining-pr"
        ]
        
        # Create branch info for fallback
        branches = [{'name': name, 'commit_date': '', 'author': ''} for name in branch_names]
    
    active_branches = []
    total_branches = len([b for b in branches if b['name'] != 'main'])
    
    print(f"📊 Found {total_branches} branches (excluding main)")
    print()
    
    # Analyze each branch
    for branch in branches:
        if branch['name'] == 'main':
            continue
            
        # For this analysis, we'll consider all non-main branches as potentially active
        # In a real scenario, you might want to filter by recent activity
        commits_ahead = count_commits_ahead_of_main(branch['name'])
        
        if commits_ahead > 0:
            active_branches.append({
                'name': branch['name'],
                'commits_ahead': commits_ahead,
                'commit_date': branch.get('commit_date', 'Unknown'),
                'author': branch.get('author', 'Unknown')
            })
    
    # Sort by number of commits ahead (descending)
    active_branches.sort(key=lambda x: x['commits_ahead'], reverse=True)
    
    print(f"🌟 Active branches with commits not in main: {len(active_branches)}")
    print()
    
    if active_branches:
        print("Branch Details:")
        print("-" * 80)
        print(f"{'Branch Name':<50} {'Commits Ahead':<15} {'Last Commit Date'}")
        print("-" * 80)
        
        total_uncommitted_commits = 0
        for branch in active_branches:
            total_uncommitted_commits += branch['commits_ahead']
            print(f"{branch['name']:<50} {branch['commits_ahead']:<15} {branch['commit_date'][:19] if branch['commit_date'] else 'Unknown'}")
        
        print("-" * 80)
        print(f"📈 Summary:")
        print(f"   • Total active branches: {len(active_branches)}")
        print(f"   • Total commits not in main: {total_uncommitted_commits}")
        print(f"   • Average commits per active branch: {total_uncommitted_commits / len(active_branches):.1f}")
    else:
        print("✅ All branches are up to date with main!")
    
    # Branch categories analysis
    print()
    print("📋 Branch Categories:")
    categories = {
        'Release branches': [b for b in active_branches if b['name'].startswith('release/')],
        'Copilot branches': [b for b in active_branches if b['name'].startswith('copilot/')],
        'Localization update branches': [b for b in active_branches if 'update-localization-files' in b['name']],
        'Feature branches': [b for b in active_branches if not any(prefix in b['name'] for prefix in ['release/', 'copilot/', 'update-localization-files'])],
    }
    
    for category, branch_list in categories.items():
        if branch_list:
            commits = sum(b['commits_ahead'] for b in branch_list)
            print(f"   • {category}: {len(branch_list)} branches, {commits} commits")

if __name__ == "__main__":
    main()