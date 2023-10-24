from autogen import AssistantAgent, GroupChatManager, UserProxyAgent
from autogen.agentchat import GroupChat

config_list = [
    {
        "api_base": "http://localhost:1234/v1",
        "api_type": "open_ai",
        "api_key": "NULL",
    }
]

llm_config = {"config_list": config_list, "seed": 42, "request_timeout": 600,}

administrator = UserProxyAgent(
    name="administrator",
    human_input_mode="NEVER",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    llm_config=llm_config,
    code_execution_config=False,
)

sales = AssistantAgent(
    name="Sales",
    llm_config=llm_config,
    system_message="""
    Sales. You follow an approved plan. You make Sales strategy for your SAAS solution.
""",
)

planner = AssistantAgent(
    name="Planner",
    system_message="""
Planner. Suggest a plan. Revise the plan based on feedback from admin and reviewer, until admin approval.
The plan involve Marketing , Sales reviwer,executor and Product.
Explain the plan first. Be clear which step is performed by Marketing ,executor,Sales,reviewer and Product

""",
    llm_config=llm_config,
)

executor = UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the written task by the planner and report the result.",
    human_input_mode="NEVER",
    llm_config=llm_config,
    code_execution_config={"work_dir":"full_docs"},
)

reviewer = AssistantAgent(
    name="reviewer",
    system_message="""reviewer.Double check plan, claims,from other agents and provide feedback.
    Check whether the plan includes adding verifiable info such as source URL.""",
    llm_config=llm_config,
)
groupchat = GroupChat(
    agents=[administrator, sales, planner, executor,reviewer],
    messages=[],
    max_round=60,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

administrator.initiate_chat(
    manager,
    message=""" 
We want to create a SaaS solution that helps companies optimize their supply chain management.
""",
)
