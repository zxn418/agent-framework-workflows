import logging
from typing import Annotated

from dotenv import load_dotenv

from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import HandoffBuilder
from agent_framework.devui import serve

from db import EservicesDB
from agent_instructions import AgentInstructions


# ============================================================
# Configuration
# ============================================================

load_dotenv()

logging.basicConfig(level=logging.INFO)


# ============================================================
# Database Tools
# ============================================================

@tool()
def fetch_customer(
    customer_id: Annotated[int, "The CustomerID to search for"]
) -> list[dict]:
    """
    Fetch customer information from the Customer table.
    """

    db = EservicesDB()

    return db.get_customer(customer_id)


@tool()
def fetch_food_item(
    food_item_id: Annotated[int, "The FoodItemID to search for"]
) -> list[dict]:
    """
    Fetch food item information from the FoodItem table.
    """

    db = EservicesDB()

    return db.get_food_item(food_item_id)


@tool()
def fetch_order(
    order_id: Annotated[int, "The OrderID to search for"]
) -> list[dict]:
    """
    Fetch order information from the Orders table.
    """

    db = EservicesDB()

    return db.get_order(order_id)


@tool()
def fetch_order_details(
    order_id: Annotated[int, "The OrderID to search for"]
) -> list[dict]:
    """
    Fetch all items belonging to an order.
    """

    db = EservicesDB()

    return db.get_order_details(order_id)


@tool()
def fetch_payment(
    order_id: Annotated[int, "The OrderID to search for"]
) -> list[dict]:
    """
    Fetch payment information for an order.
    """

    db = EservicesDB()

    return db.get_payments(order_id)


# ============================================================
# OpenAI Client
# ============================================================

client = OpenAIChatClient()


# ============================================================
# Router Agent
# ============================================================

router_agent = Agent(
    client=client,
    name="RouterAgent",
    description=(
        "Routes customer enquiries to the correct specialist. "
        "Customer questions go to CustomerAgent. "
        "Food/menu questions go to FoodItemAgent. "
        "Order questions go to OrderAgent. "
        "Payment questions go to PaymentAgent."
    ),
    instructions=AgentInstructions.ROUTER_AGENT,
    require_per_service_call_history_persistence=True,
)


# ============================================================
# Customer Agent
# ============================================================

customer_agent = Agent(
    client=client,
    name="CustomerAgent",
    description=(
        "Handles customer information enquiries such as "
        "customer name, phone, address, customer code, and customer ID."
    ),
    instructions=AgentInstructions.CUSTOMER_AGENT,
    tools=[fetch_customer],
    require_per_service_call_history_persistence=True,
)


# ============================================================
# Food Item Agent
# ============================================================

food_item_agent = Agent(
    client=client,
    name="FoodItemAgent",
    description=(
        "Handles food item and menu enquiries such as "
        "item names, prices, and food item IDs."
    ),
    instructions=AgentInstructions.FOOD_ITEM_AGENT,
    tools=[fetch_food_item],
    require_per_service_call_history_persistence=True,
)


# ============================================================
# Order Agent
# ============================================================

order_agent = Agent(
    client=client,
    name="OrderAgent",
    description=(
        "Handles order enquiries including order status, "
        "customer information attached to an order, order date, "
        "and order items."
    ),
    instructions=AgentInstructions.ORDER_AGENT,
    tools=[
        fetch_order,
        fetch_order_details,
    ],
    require_per_service_call_history_persistence=True,
)


# ============================================================
# Payment Agent
# ============================================================

payment_agent = Agent(
    client=client,
    name="PaymentAgent",
    description=(
        "Handles payment enquiries including payment amount, "
        "payment method, payment date, and order payment information."
    ),
    instructions=AgentInstructions.PAYMENT_AGENT,
    tools=[fetch_payment],
    require_per_service_call_history_persistence=True,
)


# ============================================================
# Termination Condition
# ============================================================

def terminate_after_specialist(conversation) -> bool:
    """
    End the workflow when one of the specialist agents
    has produced a normal assistant response.
    """

    specialist_names = {
        "CustomerAgent",
        "FoodItemAgent",
        "OrderAgent",
        "PaymentAgent",
    }

    return any(
        message.role == "assistant"
        and message.author_name in specialist_names
        for message in conversation
    )


# ============================================================
# Handoff Workflow
# ============================================================

workflow = (
    HandoffBuilder(
        name="EServicesRequestRouter",
        description="Routes EServices enquiries to the correct specialist agent.",
        participants=[
            router_agent,
            customer_agent,
            food_item_agent,
            order_agent,
            payment_agent,
        ],
        output_from=[router_agent],
        intermediate_output_from="all_other",
    )
    .with_start_agent(router_agent)

    # Router → specialists
    .add_handoff(
        router_agent,
        [
            customer_agent,
            food_item_agent,
            order_agent,
            payment_agent,
        ],
    )

    # Specialists → Router
    .add_handoff(customer_agent, [router_agent])
    .add_handoff(food_item_agent, [router_agent])
    .add_handoff(order_agent, [router_agent])
    .add_handoff(payment_agent, [router_agent])

    .build()
)

# ============================================================
# DevUI
# ============================================================

if __name__ == "__main__":

    serve(
    entities=[workflow],
    host="127.0.0.1",
    port=8081,
    auto_open=True,
    auth_enabled=True,
)