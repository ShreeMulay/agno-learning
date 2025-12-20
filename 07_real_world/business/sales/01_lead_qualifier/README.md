# Lead Qualifier

Scores and qualifies sales leads based on company research and fit criteria.

## Use Cases

- Prioritizing outreach in a large lead list
- Enriching CRM data with company intelligence
- Automating initial lead qualification for SDRs
- Identifying hot leads that need immediate attention

## Patterns Used

- **Tools**: DuckDuckGo for company research and news
- **Structured Output**: Pydantic models ensure consistent scoring format

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| company_name | str | "Acme Corp" | Company to research |
| contact_email | str | "john@acme.com" | Lead's email address |
| industry | str | "technology" | Target industry filter |
| min_employees | int | 50 | Minimum company size |

## Running

```bash
# Default demo
python main.py

# Qualify a specific company
python main.py --company "Stripe" --email "sales@stripe.com"

# With custom criteria
python main.py --company "Notion" --industry "productivity" --min-employees 100
```

## Example Output

```
LEAD SCORE: 85/100 (HOT)

Company: Stripe
Industry: Fintech / Payments
Size: Enterprise (1000+ employees)

✅ Fit Signals:
  • Recently raised funding
  • Actively hiring for relevant roles
  • Uses modern tech stack

⚠️  Risk Signals:
  • May have existing solution in place

💡 Recommended Action:
Schedule discovery call within 48 hours. Reference their recent 
expansion news as conversation opener.
```

## Customization

### Adjust Scoring Criteria

Modify the instructions in `get_agent()` to change:
- Industry requirements
- Company size thresholds
- Specific signals to look for

### Add More Data Sources

Replace or extend `DuckDuckGoTools()` with:
- LinkedIn API for contact info
- Clearbit for company enrichment
- Crunchbase for funding data

### Integrate with CRM

Call `get_agent()` from your CRM integration:

```python
from main import get_agent, LeadScore

agent = get_agent(config={"industry": "healthcare"})
response = agent.run(f"Qualify: {lead.company_name}")

if response.parsed:
    lead.score = response.parsed.qualification_score
    lead.save()
```
