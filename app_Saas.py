
from autogen import AssistantAgent, GroupChatManager, UserProxyAgent
from autogen.agentchat import GroupChat

config_list = [
    {
        "api_base": "http://localhost:1234/v1",
        "api_type": "open_ai",
        "api_key": "NULL",
    }
]

llm_config = {"config_list": config_list, "seed": 42, "request_timeout": 600,
              "temperature": 0,}

admin = UserProxyAgent(
    name="admin",
    human_input_mode="NEVER",
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
                      Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    llm_config=llm_config,
    code_execution_config=False,
)

Marketing = AssistantAgent(
    name="Marketing",
    llm_config=llm_config,
    system_message="Marketing. You Adhere to an approved plan and develop a marketing strategy for your SaaS product."""
)

Sales = AssistantAgent(
    name="Sales",
    llm_config=llm_config,
    system_message="""
    Sales.You execute an approved plan and formulate a sales strategy for your SaaS solution.".
""",
)

Planner = AssistantAgent(
    name="Planner",
    system_message="""
Planner.Propose a plan and iteratively refine it based on feedback from the admin and 
critic until it obtains admin approval. 
Begin by providing a clear explanation of the plan, 
specifying which steps are carried out by the Marketing, Sales,critic, and Product teams.

""",
    llm_config=llm_config,
)

Product = AssistantAgent(
    name="Product",
    llm_config=llm_config,
    system_message="""Product.You Adhere to an approved plan and ensure the accurate implementation of specifications for the SaaS-based product.
""",)


critic = AssistantAgent(
    name="critic",
    system_message="""critic.Thoroughly review the plan and claims from other agents and offer feedback. Additionally,
    ensure the plan includes verifiable information, such as source URLs.""",
    llm_config=llm_config,
)
groupchat = GroupChat(
    agents=[admin, Sales,Marketing,Product,Planner,critic],
    messages=[],
    max_round=500,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

admin.initiate_chat(
    manager,
    message=""" 
develop a SaaS solution designed to streamline and enhance supply chain management for businesses.
""",
)
