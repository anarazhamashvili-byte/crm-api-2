from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL credentials
DB_HOST = "127.0.0.1"
DB_USER = "crm_user"
DB_PASSWORD = "ChangeMe_Strong1!"
DB_NAME = "crmdata"

# 🔒 Hardcoded API key (you can also load from env vars)
API_KEY = "a3f9b8c2d1e44f7a9c0d5e6f8a7b2c1d9e0f3a4b5c6d7e8f9a0b1c2d3e4f5a6b"

def get_filtered_orders(order_number=None, phone_number=None, personal_id=None):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        where_clauses = []
        params = []

        if order_number:
            where_clauses.append("order_number = %s")
            params.append(order_number)
        if phone_number:
            where_clauses.append("phone_number = %s")
            params.append(phone_number)
        if personal_id:
            where_clauses.append("personal_id = %s")
            params.append(personal_id)

        if not where_clauses:
            return {"error": "You must filter by order_number, phone_number, or personal_id"}

        sql = f"SELECT * FROM orders WHERE {' AND '.join(where_clauses)}"
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        return {"orders": rows}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@app.route("/api/orders", methods=["GET"])
def orders_endpoint():
    # 🔒 Check API key
    key = request.args.get("api_key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    order_number = request.args.get("order_number")
    phone_number = request.args.get("phone_number")
    personal_id = request.args.get("personal_id")

    result = get_filtered_orders(order_number, phone_number, personal_id)

    if "error" in result:
        return jsonify(result), 400 if result["error"].startswith("You must") else 500

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)