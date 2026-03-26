from database import get_connection

def get_graph_data(limit=200):
    conn = get_connection()
    c = conn.cursor()

    nodes = {}
    edges = []

    # Fetch edges
    c.execute("SELECT * FROM edges LIMIT ?", (limit,))
    edge_rows = c.fetchall()

    for row in edge_rows:
        sid = row["source_id"]
        stype = row["source_type"]
        tid = row["target_id"]
        ttype = row["target_type"]
        rel = row["relationship"]

        if sid not in nodes:
            nodes[sid] = {"id": sid, "type": stype, "label": f"{stype}\n{sid[:15]}"}
        if tid not in nodes:
            nodes[tid] = {"id": tid, "type": ttype, "label": f"{ttype}\n{tid[:15]}"}

        edges.append({"from": sid, "to": tid, "label": rel})

    return list(nodes.values()), edges

def get_node_details(node_id: str, node_type: str):
    conn = get_connection()
    c = conn.cursor()
    details = {}

    try:
        if node_type == "BusinessPartner":
            c.execute("SELECT * FROM business_partners WHERE businessPartner=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "SalesOrder":
            c.execute("SELECT * FROM sales_order_headers WHERE salesOrder=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "SalesOrderItem":
            parts = node_id.split("-")
            if len(parts) >= 2:
                so = parts[0]
                item = parts[1]
                c.execute("SELECT * FROM sales_order_items WHERE salesOrder=? AND salesOrderItem=?", (so, item))
                row = c.fetchone()
                if row: details = dict(row)

        elif node_type == "Delivery":
            c.execute("SELECT * FROM outbound_delivery_headers WHERE deliveryDocument=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "BillingDocument":
            c.execute("SELECT * FROM billing_document_headers WHERE billingDocument=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "JournalEntry":
            c.execute("SELECT * FROM journal_entries WHERE accountingDocument=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "Payment":
            c.execute("SELECT * FROM payments WHERE accountingDocument=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "Product":
            c.execute("""SELECT p.*, pd.productDescription FROM products p
                        LEFT JOIN product_descriptions pd ON p.product=pd.product AND pd.language='EN'
                        WHERE p.product=?""", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

        elif node_type == "Plant":
            c.execute("SELECT * FROM plants WHERE plant=?", (node_id,))
            row = c.fetchone()
            if row: details = dict(row)

    except Exception as e:
        details = {"error": str(e)}
    finally:
        conn.close()

    return details

def get_node_connections(node_id: str):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT * FROM edges 
        WHERE source_id=? OR target_id=?
        LIMIT 50
    """, (node_id, node_id))

    rows = c.fetchall()
    conn.close()

    return [dict(row) for row in rows]