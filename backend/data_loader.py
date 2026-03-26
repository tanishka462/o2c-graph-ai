import os
import json
import sqlite3
from database import get_connection, init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data")

def load_jsonl(folder_name):
    folder = os.path.join(DATA_PATH, "sap-order-to-cash-dataset", "sap-o2c-data", folder_name)
    records = []
    if not os.path.exists(folder):
        print(f"⚠️ Folder not found: {folder}")
        return records
    for file in os.listdir(folder):
        if file.endswith(".jsonl"):
            with open(os.path.join(folder, file), "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
    return records

def safe(record, key):
    val = record.get(key)
    if val == "" or val is None:
        return None
    return val

def load_all_data():
    conn = get_connection()
    c = conn.cursor()

    print("Loading business_partners...")
    for r in load_jsonl("business_partners"):
        try:
            c.execute("""INSERT OR REPLACE INTO business_partners VALUES (?,?,?,?,?,?,?)""",
                (safe(r,"businessPartner"), safe(r,"customer"), safe(r,"businessPartnerFullName"),
                 safe(r,"businessPartnerName"), safe(r,"industry"), safe(r,"businessPartnerIsBlocked"),
                 safe(r,"creationDate")))
        except: pass

    print("Loading sales_order_headers...")
    for r in load_jsonl("sales_order_headers"):
        try:
            c.execute("""INSERT OR REPLACE INTO sales_order_headers VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (safe(r,"salesOrder"), safe(r,"salesOrderType"), safe(r,"soldToParty"),
                 safe(r,"salesOrganization"), safe(r,"totalNetAmount"), safe(r,"transactionCurrency"),
                 safe(r,"overallDeliveryStatus"), safe(r,"overallOrdReltdBillgStatus"),
                 safe(r,"creationDate"), safe(r,"requestedDeliveryDate")))
        except: pass

    print("Loading sales_order_items...")
    for r in load_jsonl("sales_order_items"):
        try:
            c.execute("""INSERT OR REPLACE INTO sales_order_items VALUES (?,?,?,?,?,?,?,?)""",
                (safe(r,"salesOrder"), safe(r,"salesOrderItem"), safe(r,"material"),
                 safe(r,"requestedQuantity"), safe(r,"requestedQuantityUnit"),
                 safe(r,"netAmount"), safe(r,"transactionCurrency"), safe(r,"productionPlant")))
        except: pass

    print("Loading outbound_delivery_headers...")
    for r in load_jsonl("outbound_delivery_headers"):
        try:
            c.execute("""INSERT OR REPLACE INTO outbound_delivery_headers VALUES (?,?,?,?,?,?)""",
                (safe(r,"deliveryDocument"), safe(r,"creationDate"), safe(r,"shippingPoint"),
                 safe(r,"overallGoodsMovementStatus"), safe(r,"overallPickingStatus"),
                 safe(r,"actualGoodsMovementDate")))
        except: pass

    print("Loading outbound_delivery_items...")
    for r in load_jsonl("outbound_delivery_items"):
        try:
            c.execute("""INSERT OR REPLACE INTO outbound_delivery_items VALUES (?,?,?,?,?,?,?)""",
                (safe(r,"deliveryDocument"), safe(r,"deliveryDocumentItem"),
                 safe(r,"referenceSdDocument"), safe(r,"referenceSdDocumentItem"),
                 safe(r,"plant"), safe(r,"actualDeliveryQuantity"), safe(r,"storageLocation")))
        except: pass

    print("Loading billing_document_headers...")
    for r in load_jsonl("billing_document_headers"):
        try:
            c.execute("""INSERT OR REPLACE INTO billing_document_headers VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (safe(r,"billingDocument"), safe(r,"billingDocumentType"), safe(r,"soldToParty"),
                 safe(r,"totalNetAmount"), safe(r,"transactionCurrency"), safe(r,"companyCode"),
                 safe(r,"fiscalYear"), safe(r,"accountingDocument"), safe(r,"billingDocumentDate"),
                 safe(r,"billingDocumentIsCancelled")))
        except: pass

    print("Loading billing_document_items...")
    for r in load_jsonl("billing_document_items"):
        try:
            c.execute("""INSERT OR REPLACE INTO billing_document_items VALUES (?,?,?,?,?,?,?,?)""",
                (safe(r,"billingDocument"), safe(r,"billingDocumentItem"), safe(r,"material"),
                 safe(r,"billingQuantity"), safe(r,"netAmount"), safe(r,"transactionCurrency"),
                 safe(r,"referenceSdDocument"), safe(r,"referenceSdDocumentItem")))
        except: pass

    print("Loading journal_entries...")
    for r in load_jsonl("journal_entry_items_accounts_receivable"):
        try:
            c.execute("""INSERT OR REPLACE INTO journal_entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (safe(r,"companyCode"), safe(r,"fiscalYear"), safe(r,"accountingDocument"),
                 safe(r,"accountingDocumentItem"), safe(r,"glAccount"), safe(r,"referenceDocument"),
                 safe(r,"customer"), safe(r,"amountInTransactionCurrency"), safe(r,"transactionCurrency"),
                 safe(r,"amountInCompanyCodeCurrency"), safe(r,"postingDate"), safe(r,"documentDate"),
                 safe(r,"accountingDocumentType"), safe(r,"clearingDate"), safe(r,"clearingAccountingDocument")))
        except: pass

    print("Loading payments...")
    for r in load_jsonl("payments_accounts_receivable"):
        try:
            c.execute("""INSERT OR REPLACE INTO payments VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (safe(r,"companyCode"), safe(r,"fiscalYear"), safe(r,"accountingDocument"),
                 safe(r,"accountingDocumentItem"), safe(r,"customer"), safe(r,"invoiceReference"),
                 safe(r,"amountInTransactionCurrency"), safe(r,"transactionCurrency"),
                 safe(r,"clearingDate"), safe(r,"postingDate"), safe(r,"salesDocument")))
        except: pass

    print("Loading products...")
    for r in load_jsonl("products"):
        try:
            c.execute("""INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?,?,?)""",
                (safe(r,"product"), safe(r,"productType"), safe(r,"productGroup"),
                 safe(r,"division"), safe(r,"grossWeight"), safe(r,"netWeight"),
                 safe(r,"weightUnit"), safe(r,"baseUnit"), safe(r,"creationDate")))
        except: pass

    print("Loading product_descriptions...")
    for r in load_jsonl("product_descriptions"):
        try:
            c.execute("""INSERT OR REPLACE INTO product_descriptions VALUES (?,?,?)""",
                (safe(r,"product"), safe(r,"language"), safe(r,"productDescription")))
        except: pass

    print("Loading plants...")
    for r in load_jsonl("plants"):
        try:
            c.execute("""INSERT OR REPLACE INTO plants VALUES (?,?,?,?,?,?)""",
                (safe(r,"plant"), safe(r,"plantName"), safe(r,"salesOrganization"),
                 safe(r,"distributionChannel"), safe(r,"division"), safe(r,"language")))
        except: pass

    conn.commit()
    print("✅ All data loaded!")
    build_edges(conn)
    conn.close()

def build_edges(conn):
    c = conn.cursor()
    print("Building edges...")

    # Customer → SalesOrder
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT soldToParty, 'BusinessPartner', salesOrder, 'SalesOrder', 'PLACED_ORDER'
        FROM sales_order_headers WHERE soldToParty IS NOT NULL
    """)

    # SalesOrder → SalesOrderItem
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT salesOrder, 'SalesOrder', salesOrder||'-'||salesOrderItem, 'SalesOrderItem', 'HAS_ITEM'
        FROM sales_order_items
    """)

    # SalesOrderItem → Product
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT salesOrder||'-'||salesOrderItem, 'SalesOrderItem', material, 'Product', 'CONTAINS_PRODUCT'
        FROM sales_order_items WHERE material IS NOT NULL
    """)

    # SalesOrderItem → DeliveryItem (via referenceSdDocument)
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT odi.referenceSdDocument||'-'||odi.referenceSdDocumentItem,
               'SalesOrderItem',
               odi.deliveryDocument||'-'||odi.deliveryDocumentItem,
               'DeliveryItem',
               'DELIVERED_VIA'
        FROM outbound_delivery_items odi
        WHERE odi.referenceSdDocument IS NOT NULL
    """)

    # DeliveryItem → DeliveryHeader
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT deliveryDocument||'-'||deliveryDocumentItem, 'DeliveryItem',
               deliveryDocument, 'Delivery', 'PART_OF_DELIVERY'
        FROM outbound_delivery_items
    """)

    # DeliveryItem → Plant
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT deliveryDocument||'-'||deliveryDocumentItem, 'DeliveryItem',
               plant, 'Plant', 'SHIPPED_FROM'
        FROM outbound_delivery_items WHERE plant IS NOT NULL
    """)

    # BillingDocument → SalesOrder (via items)
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT billingDocument, 'BillingDocument', referenceSdDocument, 'SalesOrder', 'BILLED_FOR'
        FROM billing_document_items WHERE referenceSdDocument IS NOT NULL
    """)

    # BillingDocument → JournalEntry
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT bdh.billingDocument, 'BillingDocument',
               bdh.accountingDocument, 'JournalEntry', 'POSTED_TO'
        FROM billing_document_headers bdh WHERE bdh.accountingDocument IS NOT NULL
    """)

    # JournalEntry → Payment
    c.execute("""
        INSERT INTO edges (source_id, source_type, target_id, target_type, relationship)
        SELECT DISTINCT p.invoiceReference, 'BillingDocument',
               p.accountingDocument, 'Payment', 'CLEARED_BY'
        FROM payments p WHERE p.invoiceReference IS NOT NULL
    """)

    conn.commit()
    print("✅ Edges built!")

if __name__ == "__main__":
    init_db()
    load_all_data()