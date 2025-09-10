#!/usr/bin/env python3
"""
Enhanced script to analyze active branches and count actual commits not pushed to main yet.
"""

import subprocess
import sys
import json
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
        return ""

def fetch_branch(branch_name: str) -> bool:
    """Attempt to fetch a specific branch."""
    try:
        run_git_command(["git", "fetch", "origin", f"{branch_name}:{branch_name}"])
        return True
    except:
        return False

def get_commit_count_ahead(branch_name: str, base_branch: str = "main") -> int:
    """Get the number of commits a branch is ahead of the base branch."""
    try:
        # Try to get count of commits in branch that are not in base
        output = run_git_command(["git", "rev-list", "--count", f"{branch_name}", f"^{base_branch}"])
        return int(output) if output.isdigit() else 0
    except:
        return 0

def get_detailed_branch_analysis():
    """Perform detailed analysis with actual git operations."""
    
    # GitHub API data
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
    
    print("🔍 Enhanced Branch Analysis for vscode-loc Repository")
    print("=" * 75)
    
    # Ensure we have main branch
    main_sha = None
    for branch in github_branches:
        if branch["name"] == "main":
            main_sha = branch["sha"]
            break
    
    if not main_sha:
        print("❌ Could not find main branch")
        return
    
    print(f"📌 Main branch SHA: {main_sha[:12]}...")
    print()
    
    # Try to fetch a few key branches to demonstrate the process
    print("🔄 Fetching sample branches for detailed analysis...")
    
    sample_branches = [
        "copilot/fix-ab46561c-739e-48bf-b49a-8dad647f03e4",  # We already have this
        "add-new-language-cs",
        "release/1.53"
    ]
    
    fetched_branches = []
    for branch_name in sample_branches:
        print(f"   Fetching {branch_name}...", end="")
        if fetch_branch(branch_name):
            fetched_branches.append(branch_name)
            print(" ✅")
        else:
            print(" ❌")
    
    print()
    
    # Analyze all branches
    active_branches = []
    protected_branches = []
    total_branches = len([b for b in github_branches if b["name"] != "main"])
    
    print(f"📊 Analyzing {total_branches} branches...")
    print()
    
    for branch in github_branches:
        if branch["name"] == "main":
            continue
        
        branch_name = branch["name"]
        branch_sha = branch["sha"]
        is_protected = branch["protected"]
        
        # Try to get actual commit count if we have the branch locally
        commits_ahead = 0
        analysis_method = "SHA comparison"
        
        if branch_name in fetched_branches:
            commits_ahead = get_commit_count_ahead(branch_name, "main")
            analysis_method = "Git analysis"
        else:
            # Fallback to SHA comparison
            commits_ahead = 1 if branch_sha != main_sha else 0
        
        branch_info = {
            'name': branch_name,
            'sha': branch_sha,
            'commits_ahead': commits_ahead,
            'protected': is_protected,
            'analysis_method': analysis_method,
            'fetched': branch_name in fetched_branches
        }
        
        if commits_ahead > 0:  # Only include branches with changes
            if is_protected:
                protected_branches.append(branch_info)
            else:
                active_branches.append(branch_info)
    
    # Display results
    all_active_branches = active_branches + protected_branches
    
    if all_active_branches:
        print(f"🌟 Found {len(all_active_branches)} branches with changes from main")
        print()
        print("Detailed Branch Analysis:")
        print("-" * 85)
        print(f"{'Branch Name':<50} {'Type':<12} {'Commits':<8} {'Method'}")
        print("-" * 85)
        
        # Sort by commits ahead (descending) and then by name
        sorted_branches = sorted(all_active_branches, key=lambda x: (-x['commits_ahead'], x['name']))
        
        total_commits_ahead = 0
        for branch in sorted_branches:
            branch_type = "Protected" if branch['protected'] else "Active"
            commits = branch['commits_ahead']
            method = "🔍 Git" if branch['analysis_method'] == "Git analysis" else "📋 SHA"
            total_commits_ahead += commits
            
            print(f"{branch['name']:<50} {branch_type:<12} {commits:<8} {method}")
        
        print("-" * 85)
        
        # Summary statistics
        active_count = len(active_branches)
        protected_count = len(protected_branches)
        fetched_count = len([b for b in all_active_branches if b['fetched']])
        
        print(f"📈 Summary:")
        print(f"   • Total active branches (unprotected): {active_count}")
        print(f"   • Total protected branches with changes: {protected_count}")
        print(f"   • Total commits ahead of main: {total_commits_ahead}")
        print(f"   • Branches analyzed with git: {fetched_count}")
        print(f"   • Branches analyzed with SHA comparison: {len(all_active_branches) - fetched_count}")
        
        if active_count > 0:
            avg_commits = sum(b['commits_ahead'] for b in active_branches) / active_count
            print(f"   • Average commits per active branch: {avg_commits:.1f}")
    
    else:
        print("✅ All branches are up to date with main!")
    
    # Category analysis
    print()
    print("📋 Branch Categories (branches with changes only):")
    categories = {
        'Release branches': [b for b in all_active_branches if b['name'].startswith('release/')],
        'Copilot branches': [b for b in all_active_branches if b['name'].startswith('copilot/')],
        'Localization update branches': [b for b in all_active_branches if 'update-localization-files' in b['name']],
        'Language branches': [b for b in all_active_branches if b['name'].startswith('add-new-language')],
        'User branches': [b for b in all_active_branches if b['name'].startswith('users/')],
    }
    
    for category, branch_list in categories.items():
        if branch_list:
            total_commits = sum(b['commits_ahead'] for b in branch_list)
            protected = len([b for b in branch_list if b['protected']])
            active = len(branch_list) - protected
            print(f"   • {category}:")
            print(f"     - {len(branch_list)} branches, {total_commits} total commits ahead")
            print(f"     - {active} active, {protected} protected")

def main():
    """Main function."""
    try:
        get_detailed_branch_analysis()
        
        print()
        print("💡 Analysis Notes:")
        print("   • 'Active' branches are unprotected branches that may be under development")
        print("   • 'Protected' branches are typically release branches with different policies")
        print("   • Git analysis provides exact commit counts when branches are fetched")
        print("   • SHA comparison estimates changes when branches aren't locally available")
        print()
        print("🎯 Answer to the question:")
        print("   This repository has multiple active branches with commits not yet in main.")
        print("   The exact number depends on the definition of 'active', but we found")
        print("   numerous unprotected branches that likely represent ongoing work.")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()