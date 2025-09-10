#!/usr/bin/env python3
"""
Script to analyze active branches and count commits not pushed to main yet.
Uses GitHub API data since we have limited local branch access.
"""

import subprocess
import sys
from typing import List, Dict

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

def get_commit_sha(ref: str) -> str:
    """Get the commit SHA for a given reference."""
    try:
        return run_git_command(["git", "rev-parse", ref])
    except:
        return ""

def count_commits_between_shas(sha1: str, sha2: str) -> int:
    """Count commits between two SHAs."""
    try:
        # Count commits in sha1 that are not in sha2
        output = run_git_command(["git", "rev-list", "--count", f"{sha1}", f"^{sha2}"])
        return int(output) if output.isdigit() else 0
    except:
        return 0

def analyze_branches_with_api_data():
    """Analyze branches using the GitHub API data we know exists."""
    
    # GitHub API data we retrieved earlier
    github_branches = [
        {"name": "add-new-language-cs", "sha": "b70d1832e6c17dbbfa75e34a1aa6d919c1d5f195", "protected": False},
        {"name": "add-new-language-en-gb", "sha": "8e92eb899b5f17d549dd966b3b3ef53a7f85add1", "protected": False},
        {"name": "copilot/fix-ab46561c-739e-48bf-b49a-8dad647f03e4", "sha": "37ae9abe8489e03c7dc712a7eb8fc3ffddf31f12", "protected": False},
        {"name": "copilot/fix-c56e5d2e-77f6-420c-9c39-bdf3c624d286", "sha": "02e76a8646574fa45cda5a8abceea0ab5473b988", "protected": False},
        {"name": "copilot/fix-fb52f354-8bab-481f-8e4d-38971e4030f0", "sha": "5a4669cd4435669d43a01846a33729bc0ec276e7", "protected": False},
        {"name": "main", "sha": "b5da11a23a56463f0e569f3d669d378217214cb2", "protected": True},
        {"name": "release/1.40", "sha": "87223f3efbf84e24a1ad44b33b12bdbd35b852ea", "protected": True},
        {"name": "release/1.41", "sha": "7cd14c86b9b826695bdfa7aa6eccbe5f829db7cc", "protected": True},
        {"name": "release/1.42", "sha": "85e1dfc89903ac9af53971cd914269613171cf48", "protected": True},
        {"name": "release/1.43", "sha": "ad1e5ce0f5d45aa300920b691e63bf9a5b144c15", "protected": True},
        {"name": "release/1.44", "sha": "ecc14692d5d7a790a40b185b9ef7096cefb16854", "protected": True},
        {"name": "release/1.45", "sha": "fc70260756ae0077cb57fbc7fc29aaf61286934e", "protected": True},
        {"name": "release/1.46", "sha": "9af8dd309d7dca75ae0f46cf08bc083fca324de3", "protected": True},
        {"name": "release/1.49", "sha": "e81f98af158141ec32e25c22ec37b51945121eae", "protected": True},
        {"name": "release/1.50", "sha": "557016a33f53ab6eb0673405ce44340661b36f82", "protected": True},
        {"name": "release/1.52", "sha": "2aea5a4b5c2f0811c9e3b6c3c55c9de9acdae918", "protected": True},
        {"name": "release/1.53", "sha": "8414365cca49966a7e50894ecc6106db6a6def64", "protected": True},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-4ae031e35a51b2133477b43c7863ac97d057f95c", "sha": "4a8750f70e2d22915c264f9683f468c279df8f7e", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-6ab898af3499236f8834a1305d7a2660d4540375", "sha": "1609895c0a3398d8905ed85a56e38eafa06ef038", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-63eb2b98af5cbd3b5dde526882dd2cecf3c4976b", "sha": "daaa33b07e077a88ada5e852bdc98f484c18e905", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-424b73e3cf23e87c82d2eeda28451a50a8c7f82a", "sha": "038823ea2fb2e00c4ffbebbff35b1ec329c56dc6", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-6382cfcf9163c032791bb466c52ac08f36638331", "sha": "f865d133a741d2b2807b023393542ed51218a574", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-bcafc0aec2dc23cb4227d666cb0d9ff05666e67b", "sha": "4048bf238e337304c34ca09d7427cbbd633486b4", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-c0bd77a2c9aee15711b37b99cabe1b84825f23e4", "sha": "858fc576004d343a6c883b6fc5277ae73ed246c5", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-c00c1121225a8971631d49870d8a32c42dbe13ff", "sha": "013ca529c8cab0ae6da0287acd7e81e7615fb946", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-e9b63e032468ca5e4e73ee230c72e6ad16f4ac59", "sha": "2459c85e2ba796da11264f8d73e4afa7fcf8a746", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-ef0ff67b17a06d554b85165e3b8ab3a827bf75e0", "sha": "42dbddedcb11944bb9acf12b489faf5be06a3200", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-efdb9ba1c3980129a0970d974717832b099b5bdf", "sha": "969f540c5f0e2c0af84b6412ab420e0079cf86ef", "protected": False},
        {"name": "update-localization-files-microsoft-vscode-loc-drop-fef9c1ad4839f2777875e0b6e08e106c7100f5e7", "sha": "a6d40d38bbebfc1327bfb2f7f4eb08326b5f18e3", "protected": False},
        {"name": "users/merlinbot/1es-pt-auto-baselining-pr", "sha": "d2cf3b41b80216e3185871f3b759d861ec471632", "protected": False}
    ]
    
    # Find main branch SHA
    main_sha = None
    for branch in github_branches:
        if branch["name"] == "main":
            main_sha = branch["sha"]
            break
    
    if not main_sha:
        print("❌ Could not find main branch SHA")
        return
    
    print("🔍 Analyzing branches in the vscode-loc repository...")
    print("=" * 70)
    
    # Analyze each non-main branch
    active_branches = []
    protected_branches = []
    total_branches = len([b for b in github_branches if b["name"] != "main"])
    
    print(f"📊 Found {total_branches} branches (excluding main)")
    print()
    
    for branch in github_branches:
        if branch["name"] == "main":
            continue
        
        branch_sha = branch["sha"]
        branch_name = branch["name"]
        is_protected = branch["protected"]
        
        # For this analysis, we'll assume all non-main branches are "active"
        # since we don't have local access to check commit dates
        
        # Determine if this branch has different commits than main
        commits_different = 0 if branch_sha == main_sha else 1  # Simplified: if SHA differs, assume it has different commits
        
        branch_info = {
            'name': branch_name,
            'sha': branch_sha,
            'commits_ahead': commits_different,
            'protected': is_protected
        }
        
        if is_protected:
            protected_branches.append(branch_info)
        else:
            active_branches.append(branch_info)
    
    # Display results
    all_branches = active_branches + protected_branches
    branches_with_changes = [b for b in all_branches if b['commits_ahead'] > 0]
    
    print(f"🌟 Branches with potential changes from main: {len(branches_with_changes)}")
    print()
    
    if branches_with_changes:
        print("Branch Analysis:")
        print("-" * 70)
        print(f"{'Branch Name':<50} {'Type':<12} {'Status'}")
        print("-" * 70)
        
        # Sort by type (protected first) and then by name
        sorted_branches = sorted(branches_with_changes, key=lambda x: (not x['protected'], x['name']))
        
        for branch in sorted_branches:
            branch_type = "Protected" if branch['protected'] else "Active"
            status = "Different SHA" if branch['commits_ahead'] > 0 else "Same as main"
            print(f"{branch['name']:<50} {branch_type:<12} {status}")
        
        print("-" * 70)
        
        # Summary statistics
        active_count = len([b for b in branches_with_changes if not b['protected']])
        protected_count = len([b for b in branches_with_changes if b['protected']])
        
        print(f"📈 Summary:")
        print(f"   • Total branches analyzed: {total_branches}")
        print(f"   • Active branches (unprotected): {active_count}")
        print(f"   • Protected branches: {protected_count}")
        print(f"   • Branches with changes from main: {len(branches_with_changes)}")
    else:
        print("✅ All branches have the same SHA as main!")
    
    # Branch categories analysis
    print()
    print("📋 Branch Categories:")
    categories = {
        'Release branches': [b for b in all_branches if b['name'].startswith('release/')],
        'Copilot branches': [b for b in all_branches if b['name'].startswith('copilot/')],
        'Localization update branches': [b for b in all_branches if 'update-localization-files' in b['name']],
        'Language branches': [b for b in all_branches if b['name'].startswith('add-new-language')],
        'User branches': [b for b in all_branches if b['name'].startswith('users/')],
        'Other branches': [b for b in all_branches if not any(prefix in b['name'] for prefix in ['release/', 'copilot/', 'update-localization-files', 'add-new-language', 'users/'])],
    }
    
    for category, branch_list in categories.items():
        if branch_list:
            changes = len([b for b in branch_list if b['commits_ahead'] > 0])
            protected = len([b for b in branch_list if b['protected']])
            print(f"   • {category}: {len(branch_list)} total, {changes} with changes, {protected} protected")

def main():
    """Main function."""
    try:
        analyze_branches_with_api_data()
        print()
        print("💡 Note: This analysis is based on SHA comparison since we have limited")
        print("   local branch access. Branches with different SHAs than main are")
        print("   considered to have changes that haven't been merged to main.")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()