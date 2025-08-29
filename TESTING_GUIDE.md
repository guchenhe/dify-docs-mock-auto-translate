# Translation Workflow Testing Guide

## Overview

This guide covers the fixed `sync_docs_update.yml` workflow and comprehensive testing strategy. The workflow now properly handles translation updates when English PRs are modified.

## Fixes Applied

### 1. Workflow Dependencies & Validation
- **Added validation step**: Checks for required translation tools before execution
- **Tool validation**: Verifies `pr_analyzer.py`, `sync_and_translate.py`, and `update_translations.py` exist
- **Better error messages**: Clear feedback when validation fails
- **Environment validation**: Checks for required `DIFY_API_KEY` secret

### 2. Script Extraction & Maintainability  
- **Extracted Python script**: Moved embedded script to `tools/translate/update_translations.py`
- **Modular design**: Script can be maintained, tested, and debugged independently
- **Better error handling**: Improved exception handling and status reporting
- **Security validation**: Enhanced path and file validation

### 3. Enhanced Error Reporting
- **Failure notifications**: Added comprehensive error reporting step
- **Context-aware messages**: Different error messages based on which step failed
- **Workflow links**: Direct links to failed workflow runs for debugging

### 4. GitHub API Improvements
- **Explicit tokens**: Added `github-token` parameters to all GitHub API calls
- **Better permissions**: Improved handling of repository permissions
- **Enhanced PR handling**: Better search and management of translation PRs

## Test Branches Created

### `update-test-simple` - Single File Test
**Purpose**: Tests basic single-file English change translation update
**Changes**: 
- Modified `en/documentation/pages/getting-started/introduction.mdx`
- Single line change to test minimal update scenario

**Expected Behavior**:
- Workflow should detect English-only PR
- Find associated translation PR (if exists)
- Update translations for zh-hans and ja-jp
- Comment on both original and translation PRs

### `update-test-multiple` - Multiple Files Test
**Purpose**: Tests handling of multiple English file changes
**Changes**:
- Modified `en/documentation/pages/getting-started/introduction.mdx`
- Modified `en/documentation/pages/getting-started/quick-start.mdx`  
- Modified `en/documentation/pages/getting-started/key-concepts.mdx`

**Expected Behavior**:
- Workflow should process all 3 changed files
- Generate translations for each file
- Update existing translation PR with all changes
- Report comprehensive translation status

### `update-test-docs-json` - Structure Changes Test
**Purpose**: Tests docs.json structure synchronization
**Changes**:
- Modified `docs.json` description text
- Updated navigation structure formatting

**Expected Behavior**:
- Workflow should detect docs.json changes
- Trigger structure synchronization across languages
- Update navigation in zh-hans and ja-jp sections
- Handle both content and structural changes

### `update-test-mixed` - Mixed Content Test (Should Skip)
**Purpose**: Tests that mixed English + translation PRs are skipped
**Changes**:
- Modified `en/documentation/pages/getting-started/introduction.mdx` (English)
- Modified `zh-hans/documentation/pages/getting-started/introduction.mdx` (Chinese)

**Expected Behavior**:
- PR analyzer should categorize as "mixed" 
- Workflow should skip translation update (not English-only)
- Should log appropriate skip message
- No translation PR operations should occur

### `update-test-no-translation-pr` - No Existing PR Test
**Purpose**: Tests behavior when no associated translation PR exists
**Changes**:
- Modified `en/documentation/pages/getting-started/introduction.mdx`

**Expected Behavior**:
- Workflow should detect English-only changes
- Search for associated translation PR and find none
- Gracefully handle missing translation PR case
- Log appropriate message about no existing translation PR

## Testing Instructions

### Step 1: Merge Workflow Fixes
```bash
# Create PR for the workflow fixes
git push origin fix-sync-docs-update-workflow
# Create PR on GitHub and merge to main
```

### Step 2: Test Each Scenario

For each test branch, create a PR and then update it to trigger the `sync_docs_update.yml` workflow:

#### Test Simple Update:
```bash
git checkout update-test-simple
# Make a small additional change
echo "# Additional test change" >> en/documentation/pages/getting-started/introduction.mdx
git add . && git commit -m "Additional test change"
git push origin update-test-simple
```

#### Test Multiple Files:
```bash
git checkout update-test-multiple  
# Make additional changes to trigger sync
git push origin update-test-multiple
```

#### Test docs.json Changes:
```bash
git checkout update-test-docs-json
# Update docs.json again to trigger sync
git push origin update-test-docs-json
```

#### Test Mixed Content (Should Skip):
```bash
git checkout update-test-mixed
# This should be skipped by the workflow
git push origin update-test-mixed
```

#### Test No Translation PR:
```bash
git checkout update-test-no-translation-pr
# This should handle missing translation PR gracefully
git push origin update-test-no-translation-pr
```

### Step 3: Monitor Workflow Execution

For each test:
1. **Check workflow triggers**: Verify `sync_docs_update.yml` runs on PR updates
2. **Validate tool dependencies**: Ensure validation step passes
3. **Monitor PR categorization**: Confirm PR type detection works correctly
4. **Check translation PR handling**: Verify search and update logic
5. **Verify error handling**: Test failure scenarios and error reporting

### Step 4: Validate Results

#### Success Cases (should process):
- `update-test-simple`: Single file translated correctly
- `update-test-multiple`: Multiple files handled properly  
- `update-test-docs-json`: Structure synchronization works

#### Skip Cases (should skip):
- `update-test-mixed`: Mixed content properly detected and skipped

#### Edge Cases:
- `update-test-no-translation-pr`: Missing translation PR handled gracefully

## Expected Workflow Outputs

### Successful Translation Update:
- ✅ Tool validation passes
- ✅ PR categorized as "english" 
- ✅ Translation PR found and updated
- ✅ Translations generated for changed files
- ✅ Comments posted to both PRs
- ✅ Translation PR branch updated with new content

### Skipped (Mixed Content):
- ✅ Tool validation passes
- ✅ PR categorized as "mixed" or "translation"
- ⏭️ Workflow skips translation update steps
- ℹ️ Appropriate skip message logged

### No Translation PR:
- ✅ Tool validation passes  
- ✅ PR categorized as "english"
- ❌ No translation PR found
- ℹ️ Graceful handling with appropriate message

### Validation Failures:
- ❌ Tool validation fails
- 🛑 Workflow stops early
- 💬 Error comment posted to PR
- 📋 Clear next steps provided

## Debugging Guide

### Common Issues:

1. **Tool Validation Fails**:
   - Check that `tools/translate/` directory exists
   - Verify all required Python scripts are present
   - Ensure scripts have correct permissions

2. **PR Categorization Issues**:
   - Check `pr_analyzer.py` is working correctly
   - Verify file path patterns match expected structure
   - Review PR changes are in correct directories

3. **Translation PR Not Found**:
   - Verify branch naming pattern: `docs-sync-pr-{number}`
   - Check that translation PR exists and is open
   - Ensure GitHub API permissions are correct

4. **Translation Failures**:
   - Verify `DIFY_API_KEY` secret is set correctly
   - Check API rate limits and quotas
   - Review translation script error logs

5. **GitHub API Issues**:
   - Ensure `github-token` permissions are sufficient
   - Check repository access and permissions
   - Verify API endpoints are accessible

## Monitoring & Maintenance

### Regular Checks:
- Monitor workflow success rates across different PR types
- Review error patterns and common failure points  
- Update test scenarios as the system evolves
- Maintain test branches with representative changes

### Performance Monitoring:
- Track translation processing times
- Monitor API usage and limits
- Review resource consumption patterns
- Optimize batch processing for large PRs

This comprehensive testing strategy ensures the translation update workflow functions reliably across all expected scenarios while providing clear debugging paths for any issues that arise.