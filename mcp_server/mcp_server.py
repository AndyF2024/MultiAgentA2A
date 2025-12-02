# ============================================================
# CUSTOM MCP SERVER (REQUIRED BY HOMEWORK)
# ============================================================

class MCPServer:
    """
    Custom MCP server exposing database operations as tools.
    Matches homework requirements exactly.
    """

    def __init__(self, db: DatabaseSetup):
        # DO NOT use db.cursor here (created in main thread)
        self.db = db

        # ✔ open your own connection WITH thread sharing allowed
        self.conn = sqlite3.connect("support.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    # ---------------------------------------------------
    # 1. get_customer(customer_id)
    # ---------------------------------------------------
    def get_customer(self, customer_id: int):
        self.cur.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )
        return self.cur.fetchone()

    # ---------------------------------------------------
    # 2. list_customers(status, limit)
    # ---------------------------------------------------
    def list_customers(self, status: str, limit: int = 50):
        self.cur.execute(
            "SELECT * FROM customers WHERE status = ? LIMIT ?",
            (status, limit)
        )
        return self.cur.fetchall()

    # ---------------------------------------------------
    # 3. update_customer(customer_id, data)
    # data is a dict like {"email":"...", "phone":"..."}
    # ---------------------------------------------------
    def update_customer(self, customer_id: int, data: dict):
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + [customer_id]

        self.cur.execute(
            f"UPDATE customers SET {set_clause}, updated_at = datetime('now') WHERE id = ?",
            values
        )
        self.db.conn.commit()
        return {"status": "ok", "updated": data}

    # ---------------------------------------------------
    # 4. create_ticket(customer_id, issue, priority)
    # ---------------------------------------------------
    def create_ticket(self, customer_id: int, issue: str, priority="medium"):
        self.cur.execute(
            """
            INSERT INTO tickets (customer_id, issue, status, priority, created_at)
            VALUES (?, ?, 'open', ?, datetime('now'))
            """,
            (customer_id, issue, priority)
        )
        self.db.conn.commit()
        return {"status": "ticket_created", "issue": issue, "priority": priority}

    # ---------------------------------------------------
    # 5. get_customer_history(customer_id)
    # ---------------------------------------------------
    def get_customer_history(self, customer_id: int):
        self.cur.execute(
            "SELECT * FROM tickets WHERE customer_id = ?",
            (customer_id,)
        )
        return self.cur.fetchall()

    def get_billing_context(self, customer_id: int):
        """
        Billing info not stored in DB → gracefully return 'none available'.
        Required for Scenario 2.
        """
        return {
            "customer_id": customer_id,
            "billing_available": False,
            "message": "No billing information exists for this customer."
        }
