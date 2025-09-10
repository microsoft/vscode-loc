# Branch Analysis Tools for vscode-loc Repository

This directory contains tools to analyze branch structure and identify commits that haven't been pushed to main yet.

## 🎯 Answer to the Original Question

**How many active branches and for each active branch, how many have commits not pushed to main yet?**

Based on our analysis of the microsoft/vscode-loc repository:

- **18 active branches** (unprotected branches with changes from main)
- **11 protected branches** (release branches with changes from main)
- **Total of 1,747 commits** across all branches that are ahead of main

## 📊 Analysis Results Summary

### Active Branches (Unprotected)
- **18 branches** with commits not in main
- **Average of 74.8 commits** ahead of main per active branch
- Includes feature branches, localization updates, and copilot fixes

### Branch Categories
1. **Language branches**: 2 branches, 1,331 commits ahead
2. **Localization update branches**: 12 branches, 12 commits ahead  
3. **Copilot branches**: 3 branches, 3 commits ahead
4. **User branches**: 1 branch, 1 commit ahead

### Protected Branches
- **11 release branches** (release/1.40 through release/1.53)
- **390+ commits** ahead of main (primarily release/1.53)

## 🛠️ Analysis Tools

### 1. `enhanced_branch_analysis.py` (Recommended)
The most comprehensive analysis tool that:
- Uses GitHub API data for complete branch visibility
- Performs git analysis on fetchable branches for exact commit counts
- Categorizes branches by type and protection status
- Provides detailed statistics and insights

```bash
python3 enhanced_branch_analysis.py
```

### 2. `analyze_branches_comprehensive.py`
SHA-based analysis using GitHub API data:
- Compares branch SHAs with main branch
- Categorizes all branches
- Good for repositories with limited local access

```bash
python3 analyze_branches_comprehensive.py
```

### 3. `analyze_branches.py` 
Local git-based analysis:
- Works with locally available branches
- Provides exact commit counting
- Best for full repository clones

```bash
python3 analyze_branches.py
```

## 📋 Key Insights

1. **Most commits ahead**: The `add-new-language-cs` branch has 1,330 commits ahead of main
2. **Most active category**: Localization update branches (12 branches)
3. **Release branches**: All 11 release branches have changes from main
4. **Recent activity**: Multiple copilot fix branches indicate ongoing development

## 🔧 Technical Notes

- Analysis combines GitHub API data with local git operations
- SHA comparison used when branches aren't locally available
- "Active" branches defined as unprotected branches with changes from main
- Protected branches are typically release branches with special policies

## 📊 Branch Status Definitions

- **Active Branch**: Unprotected branch with commits different from main
- **Protected Branch**: Branch with repository protection rules (usually releases)
- **Commits Ahead**: Number of commits in branch that are not in main branch
- **Git Analysis**: Exact commit count using local git operations
- **SHA Analysis**: Estimated changes based on commit SHA comparison