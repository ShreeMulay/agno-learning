# Security Guidelines

This document outlines security practices for the Agno Learning Hub project.

## API Keys & Credentials

### Never Commit Secrets

**NEVER** commit any of the following to version control:

- API keys (OpenRouter, OpenAI, Anthropic, etc.)
- OAuth tokens or credentials
- Database connection strings with passwords
- Service account JSON files
- Private keys (.pem, .key)
- Any file named `*_secret*`, `*_credentials*`, `*_token*`

### Where to Store Credentials

1. **Local Development**: Use `.env` file (already in .gitignore)
   ```bash
   # .env
   OPENROUTER_API_KEY=sk-or-...
   GITHUB_TOKEN=ghp_...
   ```

2. **CI/CD**: Use GitHub Actions secrets or similar
   ```yaml
   env:
     OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
   ```

3. **Production**: Use environment variables or secret managers

### Required Environment Variables

See `shared/integrations/api_helpers.py` for the full list. Key ones:

| Variable | Service | Required For |
|----------|---------|--------------|
| `OPENROUTER_API_KEY` | OpenRouter | All examples (default provider) |
| `OPENAI_API_KEY` | OpenAI | Alternative provider |
| `ANTHROPIC_API_KEY` | Anthropic | Alternative provider |
| `GITHUB_TOKEN` | GitHub | Code-related examples |
| `SLACK_BOT_TOKEN` | Slack | Communication examples |

## Code Security

### Validating User Input

Always validate and sanitize user input in examples:

```python
# Good: Validate input
def process_email(email: str) -> str:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValueError("Invalid email format")
    return email

# Bad: Using unsanitized input
def process_email(email: str) -> str:
    return f"Processing {email}"  # Could contain malicious content
```

### SQL Injection Prevention

When examples use SQL:

```python
# Good: Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Bad: String interpolation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### File Path Security

When examples work with files:

```python
from pathlib import Path

# Good: Restrict to safe directory
def read_file(filename: str) -> str:
    safe_dir = Path("./data").resolve()
    file_path = (safe_dir / filename).resolve()
    
    if not file_path.is_relative_to(safe_dir):
        raise ValueError("Path traversal detected")
    
    return file_path.read_text()

# Bad: Unrestricted file access
def read_file(filename: str) -> str:
    return open(filename).read()  # Could read any file!
```

## Demo Mode

All examples should work without real credentials by using demo/mock data:

```python
def get_data(api_key: str | None = None):
    if not api_key:
        # Return demo data instead of failing
        return load_demo_data("sample_leads.json")
    
    return api.fetch_real_data(api_key)
```

## Reporting Vulnerabilities

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email the maintainers directly
3. Provide detailed steps to reproduce
4. Allow reasonable time for a fix before disclosure

## Security Checklist for Contributors

Before submitting code:

- [ ] No API keys or tokens in code
- [ ] No hardcoded passwords or secrets
- [ ] User input is validated
- [ ] SQL queries are parameterized
- [ ] File paths are restricted to safe directories
- [ ] Demo mode works without credentials
- [ ] Sensitive data is not logged
- [ ] External URLs are validated

## Dependencies

- Keep dependencies updated for security patches
- Use `uv pip list --outdated` to check
- Review changelogs before updating major versions
- Prefer well-maintained packages with active security response
