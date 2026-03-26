import os
import re
import google.generativeai as genai
from database import get_connection
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SCHEMA = """
Tables:

business_partners
sales_order_headers
sales_order_items
outbound_delivery_headers
outbound_delivery_items
billing_document_headers
billing_document_items
journal_entries
payments
products
product_descriptions
plants
edges
"""

SYSTEM_PROMPT = f"""
You generate SQLite SQL queries.

Database tables:
{SCHEMA}

Rules:
1 Return only SQL
2 Use LIMIT 20
3 Use correct table names
4 No explanation
5 Return NOT_RELATED only if totally unrelated

Examples:

show customers →
SELECT * FROM business_partners LIMIT 20;

show sales orders →
SELECT * FROM sales_order_headers LIMIT 20;

show journal entries →
SELECT * FROM journal_entries LIMIT 20;
"""


# SQL generator
def generate_sql(user_question):

    question = user_question.lower()

    # detect numbers (document ids)
    numbers = re.findall(r'\d+', question)

    if numbers:

        doc_id = numbers[0]

        return f"""
        SELECT *
        FROM journal_entries
        WHERE accountingDocument = '{doc_id}'
        LIMIT 20
        """

    # keyword mapping rules

    if "journal" in question:

        return "SELECT * FROM journal_entries LIMIT 20"

    if "customer" in question or "business" in question:

        return "SELECT * FROM business_partners LIMIT 20"

    if "sales" in question or "order" in question:

        return "SELECT * FROM sales_order_headers LIMIT 20"

    if "product" in question:

        return "SELECT * FROM products LIMIT 20"

    if "payment" in question:

        return "SELECT * FROM payments LIMIT 20"

    if "billing" in question or "invoice" in question:

        return "SELECT * FROM billing_document_headers LIMIT 20"

    if "delivery" in question:

        return "SELECT * FROM outbound_delivery_headers LIMIT 20"


    # AI fallback

    try:

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(

            f"{SYSTEM_PROMPT}\nUser question:{user_question}\nSQL:"
        )

        if not response.text:

            return "NOT_RELATED"

        sql = response.text.strip()

        sql = sql.replace("```sql","")
        sql = sql.replace("```","")

        return sql

    except Exception as e:

        print("SQL GENERATION ERROR:", e)

        return "NOT_RELATED"



# SQL execution
def execute_sql(sql):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        data = [dict(zip(columns,row)) for row in rows]

        return columns,data

    except Exception as e:

        print("SQL EXECUTION ERROR:", e)

        return [],str(e)

    finally:

        conn.close()



# Answer formatting
def format_answer(user_question, sql, columns, rows):

    try:

        if isinstance(rows,str):

            return "SQL error occurred"

        if len(rows)==0:

            return "No data found"

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
User asked: {user_question}

SQL executed:
{sql}

Columns:
{columns}

Data:
{rows[:10]}

Explain what this data shows in simple business language.
Mention number of records.
"""

        response = model.generate_content(prompt)

        if response.text:

            return response.text.strip()

        return f"Found {len(rows)} records"

    except Exception as e:

        print("FORMAT ERROR:", e)

        return f"Found {len(rows)} records"



# Main chat function
def answer_question(user_question):

    try:

        sql = generate_sql(user_question)

        if sql == "NOT_RELATED":

            return {

                "answer":"Question not related to dataset",

                "sql":None,

                "data":[]
            }

        columns,rows = execute_sql(sql)

        answer = format_answer(

            user_question,

            sql,

            columns,

            rows
        )

        return {

            "answer":answer,

            "sql":sql,

            "data":rows if isinstance(rows,list) else []

        }

    except Exception as e:

        print("ANSWER ERROR:", e)

        return {

            "answer":"System error occurred",

            "sql":None,

            "data":[]
        }