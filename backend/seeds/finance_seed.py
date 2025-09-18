# seeds/finance_seed.py
from sqlalchemy.orm import Session
from backend.models.finance.finance import Account, ReportingGroup, ReportingStatement, AccountType

def seed_reporting_groups(db: Session):
    groups = [
        {"name": "Current Assets", "statement": ReportingStatement.BALANCE_SHEET, "order": 1},
        {"name": "Non-Current Assets", "statement": ReportingStatement.BALANCE_SHEET, "order": 2},
        {"name": "Current Liabilities", "statement": ReportingStatement.BALANCE_SHEET, "order": 3},
        {"name": "Non-Current Liabilities", "statement": ReportingStatement.BALANCE_SHEET, "order": 4},
        {"name": "Equity", "statement": ReportingStatement.BALANCE_SHEET, "order": 5},
        {"name": "Revenue", "statement": ReportingStatement.INCOME_STATEMENT, "order": 6},
        {"name": "Cost of Goods Sold", "statement": ReportingStatement.INCOME_STATEMENT, "order": 7},
        {"name": "Operating Expenses", "statement": ReportingStatement.INCOME_STATEMENT, "order": 8},
        {"name": "Other Income/Expenses", "statement": ReportingStatement.INCOME_STATEMENT, "order": 9},
        {"name": "Cash Flow Accounts", "statement": ReportingStatement.CASH_FLOW, "order": 10},
    ]

    for g in groups:
        rg = db.query(ReportingGroup).filter(ReportingGroup.name == g["name"]).first()
        if not rg:
            db.add(ReportingGroup(**g))
    db.commit()

def seed_accounts(db: Session):
    accounts = [
        # Assets
        {"code": "1000", "name": "Cash & Bank", "type": AccountType.ASSET, "reporting_group_id": 1},
        {"code": "1010", "name": "Petty Cash", "type": AccountType.ASSET, "parent_account_id": 1, "reporting_group_id": 1},
        {"code": "1020", "name": "Bank Account 1", "type": AccountType.ASSET, "parent_account_id": 1, "reporting_group_id": 1},
        {"code": "1100", "name": "Accounts Receivable", "type": AccountType.ASSET, "is_control_account": True, "reporting_group_id": 1},
        {"code": "1200", "name": "Inventory", "type": AccountType.ASSET, "is_control_account": True, "reporting_group_id": 1},
        {"code": "1210", "name": "Raw Materials", "type": AccountType.ASSET, "parent_account_id": 5, "reporting_group_id": 1},
        {"code": "1220", "name": "Work In Progress", "type": AccountType.ASSET, "parent_account_id": 5, "reporting_group_id": 1},
        {"code": "1230", "name": "Finished Goods", "type": AccountType.ASSET, "parent_account_id": 5, "reporting_group_id": 1},

        # Liabilities
        {"code": "2000", "name": "Accounts Payable", "type": AccountType.LIABILITY, "is_control_account": True, "reporting_group_id": 3},
        {"code": "2100", "name": "Accrued Expenses", "type": AccountType.LIABILITY, "reporting_group_id": 3},
        {"code": "2200", "name": "Loans Payable", "type": AccountType.LIABILITY, "reporting_group_id": 4},

        # Equity
        {"code": "3100", "name": "Share Capital", "type": AccountType.EQUITY, "reporting_group_id": 5},
        {"code": "3200", "name": "Retained Earnings", "type": AccountType.EQUITY, "reporting_group_id": 5},

        # Revenue
        {"code": "4000", "name": "Sales Revenue", "type": AccountType.REVENUE, "reporting_group_id": 6},
        {"code": "4010", "name": "Domestic Sales", "type": AccountType.REVENUE, "parent_account_id": 15, "reporting_group_id": 6},
        {"code": "4020", "name": "Export Sales", "type": AccountType.REVENUE, "parent_account_id": 15, "reporting_group_id": 6},

        # COGS
        {"code": "5000", "name": "Cost of Goods Sold", "type": AccountType.EXPENSE, "reporting_group_id": 7},

        # Expenses
        {"code": "5100", "name": "Operating Expenses", "type": AccountType.EXPENSE, "reporting_group_id": 8},
        {"code": "5110", "name": "Salaries & Wages", "type": AccountType.EXPENSE, "parent_account_id": 19, "reporting_group_id": 8},
        {"code": "5120", "name": "Rent & Utilities", "type": AccountType.EXPENSE, "parent_account_id": 19, "reporting_group_id": 8},
        {"code": "5130", "name": "Depreciation", "type": AccountType.EXPENSE, "parent_account_id": 19, "reporting_group_id": 8},
        {"code": "5140", "name": "Marketing & Advertising", "type": AccountType.EXPENSE, "parent_account_id": 19, "reporting_group_id": 8},

        # Other Income/Expenses
        {"code": "6000", "name": "Other Income", "type": AccountType.REVENUE, "reporting_group_id": 9},
        {"code": "6100", "name": "Other Expenses", "type": AccountType.EXPENSE, "reporting_group_id": 9},
    ]

    for a in accounts:
        acc = db.query(Account).filter(Account.code == a["code"]).first()
        if not acc:
            db.add(Account(**a))
    db.commit()

def run_seed(db: Session):
    seed_reporting_groups(db)
    seed_accounts(db)
    print("✅ Chart of Accounts seeded successfully")
