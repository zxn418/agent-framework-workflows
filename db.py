import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class EservicesDB:

    def __init__(self):

        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_DATABASE")
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")

        driver = "ODBC Driver 18 for SQL Server"

        # ----------------------------------------------------
        # Validate configuration
        # ----------------------------------------------------

        if not server:
            raise ValueError(
                "DB_SERVER is missing from .env"
            )

        if not database:
            raise ValueError(
                "DB_DATABASE is missing from .env"
            )

        if not username:
            raise ValueError(
                "DB_USERNAME is missing from .env"
            )

        if not password:
            raise ValueError(
                "DB_PASSWORD is missing from .env"
            )

        # ----------------------------------------------------
        # SQL Server connection
        # ----------------------------------------------------

        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )

        connection_url = (
            "mssql+pyodbc:///?odbc_connect="
            + quote_plus(connection_string)
        )

        self.engine = create_engine(
            connection_url,
            pool_pre_ping=True,
        )

    # ========================================================
    # GENERIC QUERY
    # ========================================================

    def execute_query(
        self,
        query: str,
        params: dict | None = None,
    ) -> list[dict]:

        with self.engine.connect() as connection:

            result = connection.execute(
                text(query),
                params or {},
            )

            return [
                dict(row._mapping)
                for row in result
            ]

    # ========================================================
    # CUSTOMER
    # ========================================================

    def get_customer(
        self,
        customer_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            CustomerID,
            CustomerCode,
            FullName,
            Phone,
            Address
        FROM Customer
        WHERE CustomerID = :customer_id
        """

        return self.execute_query(
            query,
            {
                "customer_id": customer_id
            },
        )

    # ========================================================
    # FOOD ITEM
    # ========================================================

    def get_food_item(
        self,
        food_item_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            FoodItemID,
            ItemName,
            Price
        FROM FoodItem
        WHERE FoodItemID = :food_item_id
        """

        return self.execute_query(
            query,
            {
                "food_item_id": food_item_id
            },
        )

    # ========================================================
    # ORDER
    # ========================================================

    def get_order(
        self,
        order_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            o.OrderID,
            o.CustomerID,
            c.CustomerCode,
            c.FullName,
            o.OrderDate,
            o.Status
        FROM Orders o
        LEFT JOIN Customer c
            ON o.CustomerID = c.CustomerID
        WHERE o.OrderID = :order_id
        """

        return self.execute_query(
            query,
            {
                "order_id": order_id
            },
        )

    # ========================================================
    # ORDER DETAILS
    # ========================================================

    def get_order_details(
        self,
        order_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            od.OrderDetailID,
            od.OrderID,
            od.FoodItemID,
            f.ItemName,
            od.Quantity,
            od.UnitPrice,
            (od.Quantity * od.UnitPrice) AS LineTotal
        FROM OrderDetail od
        LEFT JOIN FoodItem f
            ON od.FoodItemID = f.FoodItemID
        WHERE od.OrderID = :order_id
        ORDER BY od.OrderDetailID
        """

        return self.execute_query(
            query,
            {
                "order_id": order_id
            },
        )

    # ========================================================
    # COMPLETE ORDER
    # ========================================================

    def get_complete_order(
        self,
        order_id: int,
    ) -> dict:

        return {
            "order": self.get_order(order_id),
            "order_details": self.get_order_details(order_id),
            "payments": self.get_payments(order_id),
        }

    # ========================================================
    # PAYMENT
    # ========================================================

    def get_payments(
        self,
        order_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            PaymentID,
            OrderID,
            Amount,
            PaymentMethod,
            PaymentDate
        FROM Payment
        WHERE OrderID = :order_id
        ORDER BY PaymentDate
        """

        return self.execute_query(
            query,
            {
                "order_id": order_id
            },
        )

    # ========================================================
    # CUSTOMER ORDERS
    # ========================================================

    def get_customer_orders(
        self,
        customer_id: int,
    ) -> list[dict]:

        query = """
        SELECT
            o.OrderID,
            o.CustomerID,
            o.OrderDate,
            o.Status
        FROM Orders o
        WHERE o.CustomerID = :customer_id
        ORDER BY o.OrderDate DESC
        """

        return self.execute_query(
            query,
            {
                "customer_id": customer_id
            },
        )

    # ========================================================
    # TEST CONNECTION
    # ========================================================

    def test_connection(self) -> bool:

        try:

            with self.engine.connect() as connection:

                connection.execute(
                    text("SELECT 1")
                )

            return True

        except Exception as error:

            print(
                f"Database connection failed: {error}"
            )

            return False


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

if __name__ == "__main__":

    db = EservicesDB()

    if db.test_connection():

        print(
            "Database connection successful!"
        )

    else:

        print(
            "Database connection failed."
        )