# Sales Email Drafter

Generates personalized cold outreach emails based on prospect research.

## Use Cases

- Cold outreach campaigns
- Multi-touch email sequences
- Personalized follow-ups
- Account-based marketing

## Patterns Used

- **Tools**: DuckDuckGo for prospect/company research
- **Memory**: SQLite for conversation history across email sequences

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prospect_name | str | "Sarah Johnson" | Contact's name |
| company_name | str | "TechCorp" | Target company |
| your_company | str | "SalesBot Inc" | Your company name |
| product | str | "AI Sales Assistant" | Product being sold |
| email_type | str | "cold" | cold/follow_up/breakup |

## Running

```bash
# Default demo
python main.py

# Custom prospect
python main.py --prospect "John Smith" --company "Acme Corp"

# Follow-up email (with session for context)
python main.py --type follow_up --session john_acme
```

## Example Output

```
📧 Subject: Quick question about TechCorp's expansion

Hi Sarah,

Noticed TechCorp just opened a new office in Austin - congrats!

With rapid growth comes sales complexity. We help teams like yours
close 30% more deals without hiring more reps.

Worth a 15-min chat to see if there's a fit?

Best,
[Your name]

🎯 Personalization Used:
  • Referenced Austin office opening from recent news
  • Growth-related pain point

📞 CTA: 15-minute exploratory call
⏰ Follow up: 3 business days
```
