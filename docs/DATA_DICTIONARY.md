
# Procurement Management System - Data Dictionary

## 1. Department
- department_id: Primary key, unique text.
- department_name: Required department name.
- manager_name: Department manager.

## 2. Requester
- requester_id: Primary key.
- requester_name: Required name.
- email: Unique email.
- department_id: Foreign key.
- active: 1 = Active, 0 = Inactive.

## 3. Budget
- budget_id: Primary key.
- department_id: Foreign key.
- fiscal_year: Financial year.
- allocated_amount: Allocated INR.
- reserved_amount: Reserved INR.
- spent_amount: Spent INR.

## 4. Supplier
- supplier_id: Primary key.
- supplier_code: Unique supplier code.
- supplier_name: Supplier name.
- active: Supplier status.
- risk_flag: 1 = Risk, 0 = Normal.
- currency: INR or other currency.

## 5. Purchase Request
- request_id: Primary key.
- requester_id: Foreign key.
- department_id: Foreign key.
- budget_id: Foreign key.
- request_date: Request creation date.
- status: Request lifecycle status.
- estimated_total: Estimated purchase value.
- justification: Business reason.

## 6. Request Line
- line_id: Primary key.
- request_id: Foreign key.
- item_name: Requested item.
- category: Item category.
- quantity: Positive integer.
- unit_price: INR per unit.
- line_total: Quantity multiplied by unit price.

## 7. RFQ
- rfq_id: Primary key.
- request_id: Purchase request reference.
- issue_date: RFQ creation date.
- due_date: Quotation deadline.
- status: OPEN, EVALUATED or AWARDED.
- sourcing_type: COMPETITIVE or SINGLE_SOURCE.

## 8. Supplier Quote
- quote_id: Primary key.
- rfq_id: RFQ reference.
- supplier_id: Supplier reference.
- quote_date: Quote submission date.
- expiry_date: Expiration date.
- currency: Quotation currency.
- delivery_days: Expected delivery duration.
- subtotal: Quoted item value.
- freight: Transportation cost.
- tax: Applicable tax.
- total_landed_cost: Subtotal + freight + tax.
- status: RECEIVED, EXPIRED or SELECTED.
- rationale: Supplier selection explanation.

## 9. Approval
- approval_id: Primary key.
- request_id: Purchase request reference.
- approval_level: Approval authority.
- approver: Approver.
- decision: APPROVED, REJECTED or PENDING.
- decision_date: Decision date.
- comments: Approval explanation.

## 10. Purchase Order
- po_id: Primary key.
- request_id: Request reference.
- quote_id: Selected quote.
- supplier_id: Supplier reference.
- order_date: Purchase order date.
- status: Purchase order lifecycle status.
- total_amount: Purchase order amount.
- approved_flag: Approval evidence indicator.

## 11. Purchase Order Line
- po_line_id: Primary key.
- po_id: Purchase order reference.
- request_line_id: Original request line.
- description: Ordered item.
- quantity: Ordered quantity.
- unit_price: Awarded landed unit price.
- line_total: Quantity multiplied by unit price.

## 12. Delivery
- delivery_id: Primary key.
- po_id: Purchase order reference.
- delivery_date: Delivery date.
- quantity_received: Received quantity.
- status: PARTIAL or COMPLETE.
- notes: Delivery information.

## 13. Audit Event
- event_id: Primary key.
- entity_type: Affected entity.
- entity_id: Affected record.
- action: Recorded action.
- old_value: Previous value.
- new_value: New value.
- actor: Person or system.
- event_time: Event timestamp.

## 14. Exception Record
- exception_id: Primary key.
- entity_type: Affected entity.
- entity_id: Affected record.
- issue_type: Exception classification.
- reason: Exception explanation.
- detected_at: Detection date.
