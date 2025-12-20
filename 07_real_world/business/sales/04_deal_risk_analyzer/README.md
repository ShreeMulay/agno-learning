# Deal Risk Analyzer

Predicts deal closure probability and identifies risks requiring attention.

## Use Cases

- Weekly pipeline reviews
- QBR deal inspection
- Forecast accuracy improvement
- Rep coaching on deal strategy

## Running

```bash
python main.py --deal "Acme Enterprise" --value 250000 --stage negotiation --days 21
```

## Output

- Closure probability (0-100%)
- Risk score and level
- Individual risk factors with mitigation strategies
- Recommended actions prioritized
- Forecast category (commit/upside/pipeline/at_risk)
