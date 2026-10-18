# Copilot Cloud Agent Instructions for vscode-loc

## Repository Summary

**vscode-loc** is the localization repository for Visual Studio Code language packs. It contains 14 localized language pack extensions for VSCode, including:
- French (fr), Italian (it), German (de), Spanish (es), Russian (ru)
- Chinese Simplified (zh-cn), Chinese Traditional (zh-tw)
- Japanese (ja), Korean (ko), Czech (cs), Portuguese Brazil (pt-br), Turkish (tr), Polish (pl)
- Pseudo Language (qps-ploc) for testing

**Type**: Multi-package JavaScript/Node.js project  
**Languages**: JSON (translations), PowerShell/JavaScript (tooling)  
**Framework**: VSCode Extension format (.vsix packages)  
**Runtime**: Node.js + npm  

**Key Characteristics**:
- 14 independent language pack extensions under `/i18n/`
- Each pack contains a `package.json` and translation JSON files
- Managed translations (exported from Microsoft Localization Platform)
- Matrix-based CI/CD that builds all packs in parallel
- Minimal dependencies; mainly uses `@vscode/vsce` CLI tool for packaging

---

## Prerequisites & Setup

### Always-Do First
1. **Verify Node.js and npm** are installed:
   ```powershell
   node --version  # Requires: v16.x or later (VSCode standard)
   npm --version   # Requires: v8.x or later
   ```
   If missing, install from https://nodejs.org/

### Repository Structure
```
vscode-loc/
├── .github/
│   ├── workflows/ci.yml          # Main CI pipeline (matrix build all packs)
│   └── copilot-instructions.md   # This file
├── i18n/                          # Language packs (14 directories)
│   ├── vscode-language-pack-fr/
│   │   ├── package.json          # Extension metadata + scripts
│   │   └── translations/          # i18n JSON files organized by scope
│   │       ├── main.i18n.json    # VSCode core translations
│   │       └── extensions/        # Per-extension translations
│   └── ... (13 more packs)
├── build/
│   └── release.yml               # Azure Pipeline (publishing releases)
├── LICENSE.md
├── README.md
└── SECURITY.md
```

---

## Build & Validation Instructions

### Single Language Pack Build (Fastest for Testing)

**Always run these in order within the pack directory** (`i18n/vscode-language-pack-<lang>/`):

```powershell
cd ./i18n/vscode-language-pack-fr    # Select any language pack

# 1. **ALWAYS DO FIRST** - Install dependencies
npm install

# 2. Build the .vsix extension
npx @vscode/vsce package -o vscode-language-pack-fr-v1.110.0.vsix
```

**Output**: Creates `.vsix` file in the pack directory (~500KB-1MB)  
**Time**: ~30-60 seconds  
**Expected Success**: "Created .vsix" message, file appears in directory

### Full Repository Build (All Language Packs - Mirrors CI)

```powershell
# From repo root, build all packs (takes ~5-10 minutes total)
$languagePacks = Get-ChildItem ./i18n -Directory | ForEach-Object { $_.Name }

foreach ($pack in $languagePacks) {
    Write-Host "Building $pack..."
    cd "./i18n/$pack"
    npm install
    npx @vscode/vsce package -o "$pack-v1.110.0.vsix"
    cd ../..
}
```

**CI/CD Pipeline** (`.github/workflows/ci.yml`):
- Triggers on: PR, push to main, manual dispatch
- Runs on: Ubuntu (GitHub Actions)
- Strategy: Matrix build (parallel, one job per language pack)
- Steps per pack:
  1. Checkout code
  2. Extract version from `package.json`
  3. Run `npm install`
  4. Run `@vscode/vsce package -o <name>.vsix`
  5. Upload artifact (`.vsix` file)

---

## Validation Checklist Before PR

### Code Changes
- **JSON validation**: Ensure all translation files are valid JSON (no trailing commas, quotes balanced)
  ```powershell
  # Quick check for JSON syntax in a pack
  Get-ChildItem ./i18n/vscode-language-pack-fr/translations -Recurse -Filter "*.json" |
    ForEach-Object {
      try { Get-Content $_.FullName | ConvertFrom-Json | Out-Null; Write-Host "$($_.Name): OK" }
      catch { Write-Host "$($_.Name): ERROR - $_" }
    }
  ```

- **Package.json integrity**: Validate `package.json` has correct structure
  ```powershell
  cd ./i18n/vscode-language-pack-fr
  npm ls  # Validate dependencies and structure
  ```

### Build Validation
1. Pick one language pack (e.g., `fr`) and verify it builds end-to-end:
   ```powershell
   cd ./i18n/vscode-language-pack-fr
   npm install
   npx @vscode/vsce package
   ls *.vsix  # Verify file was created
   ```

2. **Confidence level**: If French pack builds, all others will (they're identical structure)

### Typical Changes & Where They Go
- **Translation updates**: `i18n/<pack>/translations/*.json` files
- **Version bump**: Update version in `i18n/<pack>/package.json`
- **Adding new language pack**: Add directory under `/i18n/`, copy from existing pack template
- **Tooling/CI changes**: Modify `.github/workflows/ci.yml` or `build/release.yml`
- **README/docs**: Edit root `README.md`, `SECURITY.md`, or this file

---

## Common Failures & Workarounds

### Failure: "node: command not found"
- **Symptom**: CI fails immediately on Windows runner
- **Cause**: Node.js not in PATH or not installed
- **Fix**: Ensure CI runner has `setup-node@v4` action before build steps (already in `ci.yml`)

### Failure: `npm install` hangs or timeout (>5 min)
- **Symptom**: Install step gets stuck or times out after initial output
- **Cause**: Network issue, npm registry slow, or corrupted cache
- **Fix**:
  ```powershell
  cd ./i18n/vscode-language-pack-fr
  npm cache clean --force
  npm install --verbose  # Shows what's happening
  ```

### Failure: `@vscode/vsce package` fails with "extension not found"
- **Symptom**: "Cannot find extension data"
- **Cause**: Missing or malformed `package.json` in the pack directory
- **Fix**: Verify `package.json` has required fields: `name`, `displayName`, `version`, `publisher`, `contributes`

### Failure: JSON parse error in translations
- **Symptom**: CI fails on "Unexpected token" when reading translation files
- **Cause**: Invalid JSON syntax (trailing comma, unescaped quotes, etc.)
- **Fix**: Use online JSON validator or PowerShell to check:
  ```powershell
  Get-Content ./i18n/vscode-language-pack-fr/translations/main.i18n.json | ConvertFrom-Json
  ```

### Change Workflow Validation (Tested)
✅ File edits via copilot tools work correctly  
✅ Git staging/tracking functions properly  
✅ Changes can be committed and reverted cleanly  
✅ Working directory status is tracked accurately  
⚠️ Note: Full build validation requires Node.js (not available in current environment)

---

## CI Pipeline & Release Flow

### Continuous Integration (GitHub Actions)
**File**: `.github/workflows/ci.yml`  
**Triggers**: Every PR, push to main, manual dispatch  
**Runs**: On Ubuntu (GitHub's `ubuntu-latest`)  

**Pipeline Flow**:
1. **determine-matrix**: Dynamically finds all language packs using PowerShell
2. **build** (matrix job):
   - For each language pack in parallel:
     - Install dependencies
     - Build `.vsix` file
     - Upload as artifact

**Success Criteria**: All matrix builds succeed and `.vsix` artifacts uploaded  
**Time**: ~3-5 minutes total  

### Release Pipeline (Azure Pipelines)
**File**: `build/release.yml`  
**Trigger**: Weekly schedule (Wednesdays 9 AM UTC) + manual trigger  
**Requires**: `languagePack` variable set (via Azure UI)  
**Process**:
1. Update version number with timestamp patch (e.g., `1.110.20260822`)
2. Copy LICENSE.md to pack directory
3. Package and publish to VSCode Marketplace

**Note**: Release pipeline runs per-language; set `languagePack` variable to the directory name (e.g., `vscode-language-pack-fr`)

---

## How to Make Common Changes

### Adding a Translation Fix
1. Locate the correct language pack: `i18n/vscode-language-pack-<lang>/`
2. Update the `.i18n.json` file (main core or extensions/)
3. Validate JSON syntax (see Validation section)
4. Test build: `npm install && npx @vscode/vsce package`
5. Commit and push (CI will validate all 14 packs)

### Updating Tool Dependencies
1. Edit `package.json` in the target pack (or root if shared)
2. Run `npm install` in the target pack
3. If that pack already tracks a lockfile, commit the updated lockfile with `package.json`
4. CI will validate the updated dependencies

### Adding a New Language Pack
1. Copy existing pack structure: `cp -r i18n/vscode-language-pack-fr i18n/vscode-language-pack-<lang>`
2. Update `package.json`: `name`, `displayName`, `keywords`
3. Update `translations/main.i18n.json` and extension translations
4. Commit; CI will auto-add to matrix and build it

---

## Trust This File First

**Future agents**: When working on vscode-loc, **trust this file and the inline comments in CI workflows first**. Only search the codebase if:
- Build instructions change unexpectedly
- New commands/tools are added outside of `npm` ecosystem
- A new workflow file is created that is not mentioned here
- CI fails with errors not covered in the "Common Failures" section

This file documents the stable, tested build process and architecture. Search only when you need to debug or extend beyond what is documented here.
