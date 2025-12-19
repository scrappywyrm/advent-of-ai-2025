# Day 6: Festival Feedback Triage - Technical Specification

## Overview

The Festival Feedback Triage system automatically triages GitHub Issues using Goose AI, acting as the "Winter Festival Coordinator Bot." When an issue is created or updated, a GitHub Actions workflow triggers Goose to analyze the content, categorize it, apply appropriate labels, and respond with helpful comments.

## 1. User Stories

### Story 1: Bug Report Submission
**As a festival attendee,**  
When I submit a bug report issue on GitHub,  
The system should:
- Automatically label it as "Bug 🐛" and "High Priority"
- Post an apologetic comment acknowledging the frustration
- Show empathy for the user experience issue

### Story 2: Feature Request Submission  
**As a festival attendee,**  
When I submit a feature request issue on GitHub,  
The system should:
- Automatically label it as "Feature ✨"
- Post a thank-you comment appreciating the creativity
- Mention passing the request to "the elves" (development team)

### Story 3: Question Submission
**As a festival attendee,**  
When I submit a question issue on GitHub,  
The system should:
- Automatically label it as "Question ❓"
- Post a helpful answer consistent with the winter festival theme
- Provide guidance or information relevant to the question

### Story 4: Urgent Issue Submission
**As a festival attendee,**  
When I submit an urgent issue (determined by keywords or severity),  
The system should:
- Automatically label it as "Urgent 🔥" in addition to the category label
- Prioritize the response and escalate appropriately

## 2. Architecture

### 2.1 GitHub Actions Trigger Flow
```
GitHub Issue Created/Updated
    ↓
GitHub Actions Workflow Triggered (.github/workflows/triage.yml)
    ↓
Checkout Repository Code
    ↓
Setup Python Environment
    ↓
Install Goose CLI
    ↓
Execute Goose with Festival Triage Policy
    ↓
Goose Analyzes Issue & Executes GitHub CLI Commands
```

### 2.2 Authentication Flow

**GitHub Token Authentication:**
- Repository secrets contain `GITHUB_TOKEN` (automatically provided by GitHub)
- Used for: `gh` CLI authentication for issue management (labels, comments)
- Permissions: `issues: write`, `pull-requests: read`

**OpenRouter API Authentication:**
- Repository secrets contain `OPENROUTER_API_KEY` (manually configured)  
- Used for: Goose AI model access for issue analysis
- Passed as environment variable to Goose process

### 2.3 Issue Processing Logic
```
Issue Content (Title + Body)
    ↓
Goose AI Analysis (via OpenRouter)
    ↓
Category Determination: Bug 🐛 | Feature ✨ | Question ❓ | Urgent 🔥
    ↓
Sentiment Analysis: Positive | Negative | Neutral
    ↓
Label Application (via GitHub CLI)
    ↓
Comment Generation & Posting (via GitHub CLI)
```

### 2.4 Data Flow
1. **Input:** Issue number, title, and body from GitHub webhook
2. **Processing:** Goose analyzes content using triage policy
3. **Output:** Applied labels and posted comment via GitHub API

## 3. Workflow Steps

### 3.1 GitHub Actions Workflow (`.github/workflows/triage.yml`)

```yaml
# Step 1: Trigger Configuration
name: Festival Feedback Triage
on:
  issues:
    types: [opened, edited]

# Step 2: Job Definition
jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
      
    steps:
    # Step 3: Repository Checkout  
    - name: Checkout repository
      uses: actions/checkout@v4
      
    # Step 4: Python Environment Setup
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    # Step 5: Goose Installation
    - name: Install Goose
      run: |
        pip install goose-ai
        
    # Step 6: GitHub CLI Authentication
    - name: Configure GitHub CLI
      run: |
        echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token
        
    # Step 7: Goose Execution
    - name: Run Festival Triage
      env:
        OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        ISSUE_NUMBER: ${{ github.event.issue.number }}
        ISSUE_TITLE: ${{ github.event.issue.title }}
        ISSUE_BODY: ${{ github.event.issue.body }}
      run: |
        goose run --policy-file Day06/policies/triage_policy.md \
          --env ISSUE_NUMBER="$ISSUE_NUMBER" \
          --env ISSUE_TITLE="$ISSUE_TITLE" \
          --env ISSUE_BODY="$ISSUE_BODY"
```

### 3.2 Goose Command Execution Flow

1. **Environment Setup:** Goose receives issue data via environment variables
2. **Policy Loading:** Loads `/Day06/policies/triage_policy.md`
3. **AI Analysis:** Uses OpenRouter API to analyze issue content
4. **GitHub CLI Commands:** Executes label and comment operations
5. **Completion:** Returns success/failure status to GitHub Actions

## 4. Security & Permissions

### 4.1 Required GitHub Permissions

**Repository Settings → Actions → General → Workflow permissions:**
- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

**Specific Permissions in Workflow:**
```yaml
permissions:
  issues: write        # Required: Create/edit issue labels and comments
  contents: read       # Required: Access repository files and policies
  pull-requests: read  # Optional: Future enhancement for PR triage
```

### 4.2 Required Repository Secrets

**Path: Repository Settings → Secrets and Variables → Actions**

**Secret 1: `GITHUB_TOKEN`**
- **Type:** Automatically provided by GitHub Actions
- **Purpose:** Authenticate GitHub CLI operations
- **Scope:** Repository access for issue management
- **No manual setup required**

**Secret 2: `OPENROUTER_API_KEY`**  
- **Type:** Manual configuration required
- **Purpose:** Authenticate Goose AI model access
- **Source:** OpenRouter account API key
- **Format:** `sk-or-...` (OpenRouter API key format)

### 4.3 Security Considerations

**Principle of Least Privilege:**
- GitHub token limited to repository scope only
- OpenRouter key restricted to Goose AI usage only
- Workflow only triggers on issue events (not all repository events)

**Data Privacy:**
- Issue content processed by AI model (OpenRouter)
- No persistent storage of issue data beyond GitHub
- API keys stored securely in GitHub Secrets

**Rate Limiting:**
- GitHub API: 1000 requests/hour per repository
- OpenRouter API: Depends on subscription tier
- Workflow limited to issue creation/edit events only

### 4.4 Secret Configuration Steps

1. **OpenRouter API Key Setup:**
   ```bash
   # Navigate to: https://openrouter.ai/keys
   # Create new API key
   # Copy key value (starts with sk-or-)
   ```

2. **GitHub Repository Secret Setup:**
   ```
   1. Go to Repository → Settings → Secrets and Variables → Actions
   2. Click "New repository secret"
   3. Name: OPENROUTER_API_KEY
   4. Value: [paste OpenRouter API key]
   5. Click "Add secret"
   ```

3. **Verification:**
   ```bash
   # GitHub Token is automatically available as ${{ secrets.GITHUB_TOKEN }}
   # OpenRouter key available as ${{ secrets.OPENROUTER_API_KEY }}
   ```

## 5. Error Handling & Monitoring

### 5.1 Failure Scenarios
- **OpenRouter API failure:** Workflow continues, logs error
- **GitHub CLI failure:** Workflow fails, issue remains unlabeled  
- **Goose installation failure:** Workflow fails immediately
- **Policy file missing:** Goose fails with clear error message

### 5.2 Monitoring
- **GitHub Actions logs:** Full execution trace available
- **Issue activity:** Labels and comments visible in issue timeline
- **Failure notifications:** GitHub sends email on workflow failures

---

**Ready for Implementation:** This specification provides complete technical requirements for implementing the Festival Feedback Triage system. The workflow file can be created once this specification is approved.
