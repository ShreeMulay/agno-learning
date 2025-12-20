"""
Example #031: Invoice Processor
Category: business/finance

DESCRIPTION:
Extracts data from invoices, validates against purchase orders, and routes
for approval. Handles various invoice formats and identifies discrepancies.

PATTERNS:
- Knowledge (invoice processing rules)
- Workflows (extract → validate → route)
- Structured Output (InvoiceData)

ARGUMENTS:
- invoice_text (str): Invoice content. Default: sample
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "invoice_text": """
    INVOICE #INV-2024-0892
    
    From: TechSupplies Inc.
    123 Vendor Street, Suite 400
    San Francisco, CA 94102
    
    To: Acme Corporation
    456 Client Avenue
    New York, NY 10001
    
    Date: December 15, 2024
    Due Date: January 14, 2025
    PO Reference: PO-2024-0456
    
    Items:
    1. Enterprise Software License (Annual) - Qty: 50 - $200/unit = $10,000
    2. Implementation Services - 40 hours @ $150/hr = $6,000
    3. Training Sessions - 3 sessions @ $500 = $1,500
    
    Subtotal: $17,500
    Tax (8.5%): $1,487.50
    Shipping: $0
    
    TOTAL DUE: $18,987.50
    
    Payment Terms: Net 30
    Bank: First National Bank
    Account: ****4567
    Routing: ****8901
    """,
}


class LineItem(BaseModel):
    description: str = Field(description="Item description")
    quantity: float = Field(description="Quantity")
    unit_price: float = Field(description="Price per unit")
    total: float = Field(description="Line total")


class InvoiceData(BaseModel):
    invoice_number: str = Field(description="Invoice number")
    vendor_name: str = Field(description="Vendor/supplier name")
    vendor_address: str = Field(description="Vendor address")
    client_name: str = Field(description="Client/buyer name")
    invoice_date: str = Field(description="Invoice date")
    due_date: str = Field(description="Payment due date")
    po_reference: Optional[str] = Field(default=None, description="Purchase order reference")
    line_items: list[LineItem] = Field(description="Invoice line items")
    subtotal: float = Field(description="Subtotal before tax")
    tax_amount: float = Field(description="Tax amount")
    tax_rate: Optional[float] = Field(default=None, description="Tax rate percentage")
    total_amount: float = Field(description="Total amount due")
    payment_terms: str = Field(description="Payment terms")
    validation_status: str = Field(description="valid/needs_review/rejected")
    validation_issues: list[str] = Field(default_factory=list, description="Any issues found")
    approval_routing: str = Field(description="Who should approve")
    confidence_score: int = Field(ge=0, le=100, description="Extraction confidence")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Invoice Processor",
        instructions=[
            "You are an expert accounts payable specialist.",
            "Extract and validate invoice data accurately.",
            "",
            "Extraction Rules:",
            "- Extract all line items with quantities and prices",
            "- Verify math (quantities × prices = line totals)",
            "- Check subtotal + tax = total",
            "- Identify PO references for matching",
            "",
            "Validation Checks:",
            "- All required fields present",
            "- Math calculations correct",
            "- Due date is reasonable",
            "- Tax rate within normal range (0-15%)",
            "",
            "Approval Routing:",
            "- Under $1,000: Auto-approve",
            "- $1,000-$10,000: Manager approval",
            "- $10,000-$50,000: Director approval",
            "- Over $50,000: VP/CFO approval",
        ],
        output_schema=InvoiceData,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Invoice Processor - Demo")
    print("=" * 60)
    
    invoice = config.get("invoice_text", DEFAULT_CONFIG["invoice_text"])
    
    response = agent.run(f"Extract and validate this invoice:\n\n{invoice}")
    result = response.content
    
    if isinstance(result, InvoiceData):
        print(f"\n📄 Invoice: {result.invoice_number}")
        print(f"Vendor: {result.vendor_name}")
        print(f"Date: {result.invoice_date} | Due: {result.due_date}")
        print(f"PO: {result.po_reference or 'N/A'}")
        
        print(f"\n📋 Line Items:")
        for item in result.line_items:
            print(f"  • {item.description}: {item.quantity} × ${item.unit_price:.2f} = ${item.total:.2f}")
        
        print(f"\n💰 Totals:")
        print(f"  Subtotal: ${result.subtotal:,.2f}")
        print(f"  Tax ({result.tax_rate or 0}%): ${result.tax_amount:,.2f}")
        print(f"  TOTAL: ${result.total_amount:,.2f}")
        
        status_icon = "✅" if result.validation_status == "valid" else "⚠️"
        print(f"\n{status_icon} Status: {result.validation_status.upper()}")
        if result.validation_issues:
            for issue in result.validation_issues:
                print(f"  ⚠️ {issue}")
        print(f"👤 Route to: {result.approval_routing}")
        print(f"🎯 Confidence: {result.confidence_score}%")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Invoice Processor")
    parser.add_argument("--invoice", "-i", type=str, default=DEFAULT_CONFIG["invoice_text"])
    args = parser.parse_args()
    agent = get_agent(config={"invoice_text": args.invoice})
    run_demo(agent, {"invoice_text": args.invoice})


if __name__ == "__main__":
    main()
