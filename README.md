# GitHub API E2E Tests

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Testing-green?logo=pytest)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange)
![GitHub API](https://img.shields.io/badge/GitHub-REST_API-black?logo=github)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-blue?logo=githubactions)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=githubactions)
![Slack](https://img.shields.io/badge/Slack-Notifications-4A154B?logo=slack)
![JSON Schema](https://img.shields.io/badge/JSON-Schema-red)
![HTML Reports](https://img.shields.io/badge/Reports-HTML-success)
![E2E Testing](https://img.shields.io/badge/Testing-E2E-yellow)
![Automation](https://img.shields.io/badge/QA-Automation-brightgreen)

End-to-end API automation framework for testing GitHub workflows using Python, Pytest, and GitHub REST APIs.

This project focuses on real-world GitHub scenarios such as:
- Repository lifecycle management
- Pull request workflows
- Branch protection
- Collaborator invitations
- Webhooks
- Issues
- Permission validation
- Negative and edge-case testing

The framework is designed using a scalable POM-inspired architecture for API automation.

---

# 🚀 Tech Stack

- Python 3.12
- Pytest
- Requests
- Pytest HTML Report
- GitHub REST API
- GitHub Actions
- Slack Notifications
- JSON Schema Validation

---

# ✨ Features

## ✅ End-to-End GitHub Workflow Testing

The framework simulates real GitHub user behavior:
- Create repositories
- Create/delete branches
- Open pull requests
- Merge pull requests
- Add reviewers
- Manage issues
- Add collaborators
- Create webhooks

---

## ✅ Negative Testing

Includes validation for:
- Unauthorized access
- Invalid tokens
- Duplicate repositories
- Invalid branch operations
- Permission restrictions
- Read-only token limitations

---

## ✅ CI/CD Integration

Integrated with GitHub Actions:
- Automatic execution on pull requests
- Conditional test execution
- HTML report generation
- Downloadable artifacts
- Slack notifications

---

# 📁 Project Structure

```plaintext
github-api-e2e-tests/
│
├── .github/
│   └── workflows/
│       └── e2e-tests.yml
│
├── api/
│   ├── github_api_client.py
│   ├── repository_api.py
│   ├── branch_api.py
│   ├── commit_api.py
│   ├── content_api.py
│   ├── issue_api.py
│   ├── pr_api.py
│   ├── pr_comment_api.py
│   ├── pr_review_api.py
│   ├── invitation_api.py
│   ├── repo_collab_api.py
│   ├── user_api.py
│   └── webhook_api.py
│
├── base/
│   └── base_test.py
│
├── models/
│   ├── branch_data_model/
│   ├── issue_data_model/
│   ├── pull_request_data_model/
│   ├── repo_data_model/
│   ├── user_data_model/
│   └── webhook_data_model/
│
├── reports/
│   └── e2e-report.html
│
├── test_data/
│   ├── repo_data.py
│   ├── pr_data.py
│   └── user_data.py
│
├── tests/
│   └── e2e/
│
├── utils/
│   ├── assertion.py
│   ├── config.py
│   └── decorators.py
│
├── .env
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```
```

---

# ⚙️ Setup

## 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd github-api-e2e-tests
```

---

## 2️⃣ Create Virtual Environment

### Mac/Linux

```bash
python3 -m venv github_venv
source github_venv/bin/activate
```

### Windows

```bash
python -m venv github_venv
github_venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
TOKEN=your_github_token
BASE_URL=https://api.github.com
USERNAME=your_username
PASSWORD=your_password
COLLABORATOR_TOKEN=your_collaborator_token
COLLABORATOR=your_collaborator_username
READ_ONLY_TOKEN=your_read_only_token
```

---

# ▶️ Running Tests

## Run All E2E Tests

```bash
pytest tests/e2e -v
```

---

## Generate HTML Report

```bash
pytest tests/e2e -v --html=reports/e2e-report.html --self-contained-html
```

---

# 📊 CI/CD Pipeline

The project uses GitHub Actions for continuous integration.

Workflow file:

```plaintext
.github/workflows/e2e-tests.yml
```

---

# 🔄 Pipeline Trigger Logic

The pipeline runs ONLY when:
- A pull request is opened
- A pull request is updated
- A pull request is reopened
- A pull request is edited

AND the pull request title contains:

```plaintext
run test
```

Example PR title:

```plaintext
run test - add new repository lifecycle tests
```

This prevents unnecessary CI execution and helps control GitHub Actions usage.

---

# 🚀 CI/CD Workflow Steps

The pipeline automatically:

1. Downloads project source code
2. Installs Python
3. Installs project dependencies
4. Sends Slack start notification
5. Runs E2E tests
6. Generates HTML report
7. Uploads report as downloadable artifact
8. Sends Slack success/failure notification

---

# 🔔 Slack Notifications

The pipeline sends two types of notifications:

## 🚀 Pipeline Started

Example:

```plaintext
🚀 E2E pipeline started
```

Includes:
- GitHub Actions run link

---

## ✅ Success Notification

Example:

```plaintext
✅ E2E tests passed!
```

Includes:
- GitHub Actions run link

---

## ❌ Failure Notification

Example:

```plaintext
❌ E2E tests failed!
```

Includes:
- Failed test names
- GitHub Actions run link

---

# 📄 HTML Test Reports

The pipeline automatically generates:

```plaintext
reports/e2e-report.html
```

The report is uploaded as a downloadable GitHub Actions artifact.

---

# 🧪 Example Test Scenarios

## Repository Flows
- Repository lifecycle flow
- Duplicate repository creation
- Repository permission validation

## Pull Request Flows
- PR creation flow
- Draft → Ready for review transition
- Merge conflict detection
- PR comment lifecycle

## Branch Flows
- Branch lifecycle
- Branch protection
- Branch deletion validation

## Collaborator Flows
- Collaborator invitation lifecycle
- Invitation rejection flow

## Security Flows
- Unauthorized scope rejection
- Read-only token validation

---

---

## ✅ Dynamic Resource Management with Fixtures

The framework heavily uses Pytest fixtures to dynamically create and manage temporary GitHub resources during test execution.

Fixtures help:
- Reduce duplicated setup logic
- Improve test isolation
- Keep tests independent
- Automatically clean up resources

---

## ✅ Temporary Resources Created by Fixtures

Fixtures can dynamically create:
- Temporary repositories
- Temporary branches
- Pull requests

This allows fully isolated E2E execution without relying on manually created test data.

---

## ✅ Automatic Cleanup

Fixtures also handle teardown operations automatically.

Examples:
- Delete temporary repositories
- Remove temporary branches
- remove pull requests

This prevents stale resources from remaining in the GitHub account.

---

## ✅ Example Fixture
Check the full fixture code in conftest.py. The following example is a shorthand version to show how it looks.

```python
@pytest.fixture
def create_temporary_repo(repository_api):

    repository_name = f"test-repo-{uuid.uuid4()}"

    repo_api.create_repo_for_authenticated_user(payload)
    
    ...............

    yield repository_name

    repository_api.delete_repo(repo_name)
```

This fixture:
1. Creates a temporary repository
2. Provides it to the test
3. Automatically deletes it after execution


# 🧱 Framework Design Principles

This framework follows:
- Separation of concerns
- Reusable API layers
- Centralized configuration
- Data-driven testing
- Maintainable architecture
- POM-inspired API design

---

# 🔥 CI/CD Best Practices Used

- Environment secrets
- Artifact uploads
- Failure-aware pipelines
- Slack integration
- Conditional workflow execution
- Pipefail handling
- Self-contained HTML reports

---

# 📌 Future Improvements

- Docker support
- Parallel test execution
- Retry mechanism
- Allure report publishing
- GraphQL API testing
- Performance testing
- Contract testing

---

# 👨‍💻 Author

Built for practicing:
- API Automation
- End-to-End Testing
- CI/CD
- GitHub API workflows
- Professional QA architecture