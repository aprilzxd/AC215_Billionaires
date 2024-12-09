from phi.agent import Agent
from phi.llm.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.googlesearch import GoogleSearch
from phi.tools.newspaper_tools import NewspaperTools
from .tools.multisend import multisend
from .tools.stockplotter import StockPlotter
from .prompt import SYSTEM_PROMPT

# Fixed sender email configuration
SENDER_EMAIL = "yananlancelu@gmail.com"
SENDER_NAME = "Huandong, April, Lance, Mingyuan"
SENDER_PASSKEY = "neij kvys dupr owqc"

# Default receiver emails
DEFAULT_RECEIVER_EMAILS = [
    "mingyuan_ma@g.harvard.edu",
    "april_zhang@g.harvard.edu",
    "huandongchang@g.harvard.edu",
    "lance_lu@hms.harvard.edu",
]

# Define the agent with tools
agent = Agent(
    llm=OpenAIChat(model="gpt-4o", stream=True),
    tools=[
        YFinanceTools(
            enable_all = True
        ),
        GoogleSearch(), NewspaperTools(),
        StockPlotter(),
        multisend(
            receiver_email=DEFAULT_RECEIVER_EMAILS,
            sender_email=SENDER_EMAIL,
            sender_name=SENDER_NAME,
            sender_passkey=SENDER_PASSKEY,
        ),
    ],
    markdown=True,
    add_history_to_messages=True,
    description=SYSTEM_PROMPT,
    add_datetime_to_instructions=True
)
