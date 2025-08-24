# Auto-Translation Workflow Test Cases

This document describes the available test case branches for testing the automatic documentation translation workflow.

## Overview

Each test case branch contains pre-configured changes that represent different scenarios the workflow should handle. These branches can be used to create PRs and test the workflow behavior repeatedly.

## Test Case Branches

### Test Case 1A: Add New English Content with Navigation Update
**Branch:** `test-case-1a-add-english-with-nav`

**Changes:**
- Adds new English file: `en/documentation/pages/getting-started/integration-guide.mdx`
- Updates `docs.json` to include the new file in navigation

**Expected Workflow Behavior:**
- Should classify as "English-only changes with navigation update"
- Should create zh-hans and ja-jp translations of `integration-guide.mdx`
- Should mirror the navigation entries in zh-hans and ja-jp sections of `docs.json`
- Should create a translation PR with translated files and navigation updates

---

### Test Case 1B: Update Existing English Content Only  
**Branch:** `test-case-1b-update-english-only`

**Changes:**
- Updates existing English file: `en/documentation/pages/getting-started/introduction.mdx`
- Enhanced introduction description and Quick Start card text
- No navigation changes

**Expected Workflow Behavior:**
- Should classify as "English-only content updates"
- Should update zh-hans and ja-jp translations of `introduction.mdx`
- Should NOT change `docs.json` navigation structure
- Should create a translation PR with only the updated translated files

---

### Test Case 1C: Remove English Content with Navigation Update
**Branch:** `test-case-1c-remove-english-with-nav`

**Changes:**
- Removes English file: `en/documentation/pages/getting-started/deprecated-guide.mdx`
- Removes corresponding navigation entry from `docs.json`

**Expected Workflow Behavior:**
- Should classify as "English content removal with navigation changes"
- Should remove zh-hans and ja-jp translations of `deprecated-guide.mdx`
- Should remove navigation entries from zh-hans and ja-jp sections in `docs.json`
- Should create a translation PR with file removals and navigation cleanup

---

### Test Case 1D: Add Translation Content Only
**Branch:** `test-case-1d-add-translation-only`

**Changes:**
- Adds new Chinese translation file: `zh-hans/documentation/pages/getting-started/manual-translation-example.mdx`
- No corresponding English source file
- No English content changes

**Expected Workflow Behavior:**
- Should classify as "Translation-only changes"
- Should NOT trigger auto-translation workflow
- Should NOT create any translation PRs
- Original PR should be processed normally without workflow intervention

---

### Test Case 1E: Update Translation Content Only
**Branch:** `test-case-1e-update-translation-only`

**Changes:**
- Updates existing Chinese translation: `zh-hans/documentation/pages/getting-started/introduction.mdx`
- Adds additional descriptive content to Chinese version
- No English content changes

**Expected Workflow Behavior:**
- Should classify as "Translation-only changes"
- Should NOT trigger auto-translation workflow
- Should NOT create any translation PRs
- Should NOT affect English or Japanese content

---

### Test Case 1F: Mixed Content Changes
**Branch:** `test-case-1f-mixed-content-changes`

**Changes:**
1. Add new English file with navigation: `en/documentation/pages/getting-started/mixed-test-guide.mdx`
2. Update existing English content: `en/documentation/pages/getting-started/quick-start.mdx`
3. Add translation-only content: `ja-jp/documentation/pages/getting-started/manual-japanese-addition.mdx`
4. Update translation content: `zh-hans/documentation/pages/getting-started/introduction.mdx`

**Expected Workflow Behavior:**
- Should classify as "Mixed content changes"
- Should trigger auto-translation for English changes only (#1 and #2)
- Should preserve manual translation additions/updates (#3 and #4)
- Should create a translation PR with:
  - New zh-hans/ja-jp translations of `mixed-test-guide.mdx`
  - Updated zh-hans/ja-jp translations of `quick-start.mdx`
  - Navigation updates for new English content
  - Should NOT modify the manual translation files

## Usage Instructions

To test any scenario:

1. **Create a PR from test branch:**
   ```bash
   gh pr create --head test-case-1a-add-english-with-nav --title "Test 1A: Integration Guide"
   ```

2. **Monitor workflow execution:**
   ```bash
   gh run list --limit 3
   gh run view [run-id] --log
   ```

3. **Check results:**
   ```bash
   gh pr list  # Look for auto-generated translation PRs
   gh pr diff [translation-pr-number]  # Examine translation PR contents
   ```

4. **Clean up (optional):**
   ```bash
   gh pr close [pr-number]  # Close test PRs
   git branch -D test-branch-name  # Delete local branch if needed
   ```

## Validation Checklist

For each test case, verify:

- [ ] Analyze workflow completes successfully
- [ ] Execute workflow completes successfully (if triggered)
- [ ] Translation PR is created (when expected)
- [ ] Translation PR contains correct files
- [ ] Navigation structure is properly synced (when expected)
- [ ] Translation notice headers are included
- [ ] No original PR content is included in translation PR

## Notes

- All test branches are based on `main` and can be updated as needed
- Test cases are designed to be independent and can be run in any order  
- Each test creates different file names to avoid conflicts
- Branches include detailed commit messages explaining the test scenario