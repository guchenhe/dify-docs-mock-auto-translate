# Auto-Translate Workflow Testing - Remaining Test Cases

## Phase 2: Navigation Structure Tests

### **2A. English Navigation Only**
- **Action:** Add new section to English navigation in docs.json
- **Expected:** Create translation PR with corresponding zh-hans + ja-jp navigation updates

### **2B. Mixed Navigation Changes**
- **Action:** Modify both English and Chinese navigation sections in docs.json
- **Expected:** Block with mixed-content error (navigation changes detected)

### **2C. Complex Navigation + Content**
- **Action:** Add new English file + add new navigation group + reorder existing items
- **Expected:** Create translation PR with full navigation structure sync

## Phase 3: Security & Limits Tests

### **3A. Large File Test**
- **Action:** Add English file exceeding 10MB limit
- **Expected:** Fail security validation with file size error

### **3B. Too Many Files Test**
- **Action:** Add 55+ English files in single PR
- **Expected:** Fail security validation with file count error

### **3C. Invalid Extensions Test**
- **Action:** Add `en/malicious.exe` or `en/script.php` file
- **Expected:** Fail security validation with extension error

### **3D. Path Traversal Test**
- **Action:** Try adding `en/../../../etc/passwd.md`
- **Expected:** Fail security validation with path traversal error

## Phase 4: Update & Sync Tests

### **4A. PR Update with Content Changes**
- **Action:** Create English PR, let translation PR be created, then update original English PR
- **Expected:** Translation PR automatically updates with new translations

### **4B. PR Update with Navigation Changes**
- **Action:** Create English PR with nav changes, then modify navigation structure again
- **Expected:** Translation PR updates with revised navigation structure

### **4C. Translation PR Closure Behavior**
- **Action:** Close the auto-generated translation PR manually
- **Expected:** System handles gracefully, no further auto-updates to closed PR

### **4D. Concurrent English PRs**
- **Action:** Create 2-3 English PRs simultaneously
- **Expected:** Each gets its own translation PR with proper branch naming

## Phase 5: Edge Cases & Error Handling

### **5A. Empty PR (No Changes)**
- **Action:** Create PR with no actual file changes
- **Expected:** Skip with "no relevant changes" message

### **5B. Non-documentation Changes Only**
- **Action:** Modify only `README.md`, `.github/workflows/`, or `tools/` files
- **Expected:** Skip with "no relevant changes" message

### **5C. Fork PR from External Contributor**
- **Action:** Create PR from forked repository
- **Expected:** Require manual approval before auto-translation proceeds

### **5D. API Key Missing/Invalid**
- **Action:** Remove or corrupt DIFY_API_KEY secret
- **Expected:** Workflow fails gracefully with clear error message

## Test Status
- **Completed:** Tests 1A-1F (Basic Content Operations)
- **Remaining:** Tests 2A-5D (to be executed after basic tests)

## Prerequisites
- DIFY_API_KEY secret must be configured in repository settings
- Repository permissions set for workflow execution
- Valid Dify credentials for actual API translation testing