from typing import Dict, Optional

import chainlit as cl
from chainlit.input_widget import Select


from src.model import train_model, vanna



@cl.step(language="sql", name="Vanna")
async def gen_query(human_query: str):
    sql_query = vanna.generate_sql(human_query, allow_llm_to_see_data=True)
    return sql_query

@cl.step(name="Vanna")
async def execute_query(query):
    current_step = cl.context.current_step
    df = vanna.run_sql(query)
    current_step.output = df.head().to_markdown(index=False)

    return df

@cl.step(name="Plot", language="python")
async def plot(human_query, sql, df):
    current_step = cl.context.current_step
    plotly_code = vanna.generate_plotly_code(question=human_query, sql=sql, df=df)
    fig = vanna.get_plotly_figure(plotly_code=plotly_code, df=df)

    current_step.output = plotly_code
    return fig

@cl.step(type="run", name="SQL Query")
async def chain(human_query: str):
    sql_query = await gen_query(human_query)
    df = await execute_query(sql_query)
    fig = await plot(human_query, sql_query, df)

    elements = [cl.Plotly(name="chart", figure=fig, display="inline")]
    await cl.Message(content=human_query, elements=elements, author="Vanna").send()

@cl.on_message
async def main(message: cl.Message):
    await chain(message.content)


# @cl.header_auth_callback
# def header_auth_callback(headers: Dict) -> Optional[cl.User]:
#   # Verify the signature of a token in the header (ex: jwt token)
#   # or check that the value is matching a row from your database
#   if headers.get("test-header") == "test-value":
#     return cl.User(identifier="admin", metadata={"role": "admin", "provider": "header"})
#   else:
#     return None


@cl.on_settings_update
async def setup_agent(settings):
    selected_model = settings.get('Model')
    vanna.set_model(selected_model)



@cl.on_chat_start
async def setup():
    # await cl.Avatar(
    #     name="Vanna",
    #     url="https://app.vanna.ai/vanna.svg",
    # ).send()

    await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=[
                    "gpt-4o-mini",
                    "gpt-3.5-turbo",
                    "gpt-4o",
                ],
                initial_index=0,
            )
        ]
    ).send()

    res = await cl.AskActionMessage(
        content="Para empezar ¿Quieres reentrenar el modelo?",
        actions=[
            cl.Action(name="continue", value="ok", label="Si"),
            cl.Action(name="cancel", value="no", label="No"),
        ],
    ).send()

    if res and res.get("value") == "ok":
        train_model()