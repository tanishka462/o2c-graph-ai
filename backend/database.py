import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "o2c.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS business_partners (
        businessPartner TEXT PRIMARY KEY,
        customer TEXT,
        businessPartnerFullName TEXT,
        businessPartnerName TEXT,
        industry TEXT,
        businessPartnerIsBlocked TEXT,
        creationDate TEXT
    );

    CREATE TABLE IF NOT EXISTS sales_order_headers (
        salesOrder TEXT PRIMARY KEY,
        salesOrderType TEXT,
        soldToParty TEXT,
        salesOrganization TEXT,
        totalNetAmount REAL,
        transactionCurrency TEXT,
        overallDeliveryStatus TEXT,
        overallOrdReltdBillgStatus TEXT,
        creationDate TEXT,
        requestedDeliveryDate TEXT
    );

    CREATE TABLE IF NOT EXISTS sales_order_items (
        salesOrder TEXT,
        salesOrderItem TEXT,
        material TEXT,
        requestedQuantity REAL,
        requestedQuantityUnit TEXT,
        netAmount REAL,
        transactionCurrency TEXT,
        productionPlant TEXT,
        PRIMARY KEY (salesOrder, salesOrderItem)
    );

    CREATE TABLE IF NOT EXISTS outbound_delivery_headers (
        deliveryDocument TEXT PRIMARY KEY,
        creationDate TEXT,
        shippingPoint TEXT,
        overallGoodsMovementStatus TEXT,
        overallPickingStatus TEXT,
        actualGoodsMovementDate TEXT
    );

    CREATE TABLE IF NOT EXISTS outbound_delivery_items (
        deliveryDocument TEXT,
        deliveryDocumentItem TEXT,
        referenceSdDocument TEXT,
        referenceSdDocumentItem TEXT,
        plant TEXT,
        actualDeliveryQuantity REAL,
        storageLocation TEXT,
        PRIMARY KEY (deliveryDocument, deliveryDocumentItem)
    );

    CREATE TABLE IF NOT EXISTS billing_document_headers (
        billingDocument TEXT PRIMARY KEY,
        billingDocumentType TEXT,
        soldToParty TEXT,
        totalNetAmount REAL,
        transactionCurrency TEXT,
        companyCode TEXT,
        fiscalYear TEXT,
        accountingDocument TEXT,
        billingDocumentDate TEXT,
        billingDocumentIsCancelled TEXT
    );

    CREATE TABLE IF NOT EXISTS billing_document_items (
        billingDocument TEXT,
        billingDocumentItem TEXT,
        material TEXT,
        billingQuantity REAL,
        netAmount REAL,
        transactionCurrency TEXT,
        referenceSdDocument TEXT,
        referenceSdDocumentItem TEXT,
        PRIMARY KEY (billingDocument, billingDocumentItem)
    );

    CREATE TABLE IF NOT EXISTS journal_entries (
        companyCode TEXT,
        fiscalYear TEXT,
        accountingDocument TEXT,
        accountingDocumentItem TEXT,
        glAccount TEXT,
        referenceDocument TEXT,
        customer TEXT,
        amountInTransactionCurrency REAL,
        transactionCurrency TEXT,
        amountInCompanyCodeCurrency REAL,
        postingDate TEXT,
        documentDate TEXT,
        accountingDocumentType TEXT,
        clearingDate TEXT,
        clearingAccountingDocument TEXT,
        PRIMARY KEY (accountingDocument, accountingDocumentItem, fiscalYear)
    );

    CREATE TABLE IF NOT EXISTS payments (
        companyCode TEXT,
        fiscalYear TEXT,
        accountingDocument TEXT,
        accountingDocumentItem TEXT,
        customer TEXT,
        invoiceReference TEXT,
        amountInTransactionCurrency REAL,
        transactionCurrency TEXT,
        clearingDate TEXT,
        postingDate TEXT,
        salesDocument TEXT,
        PRIMARY KEY (accountingDocument, accountingDocumentItem, fiscalYear)
    );

    CREATE TABLE IF NOT EXISTS products (
        product TEXT PRIMARY KEY,
        productType TEXT,
        productGroup TEXT,
        division TEXT,
        grossWeight REAL,
        netWeight REAL,
        weightUnit TEXT,
        baseUnit TEXT,
        creationDate TEXT
    );

    CREATE TABLE IF NOT EXISTS product_descriptions (
        product TEXT,
        language TEXT,
        productDescription TEXT,
        PRIMARY KEY (product, language)
    );

    CREATE TABLE IF NOT EXISTS plants (
        plant TEXT PRIMARY KEY,
        plantName TEXT,
        salesOrganization TEXT,
        distributionChannel TEXT,
        division TEXT,
        language TEXT
    );

    CREATE TABLE IF NOT EXISTS edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        source_type TEXT,
        target_id TEXT,
        target_type TEXT,
        relationship TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized!")