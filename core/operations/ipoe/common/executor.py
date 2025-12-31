from core.connection.telnet import send_ipoe


async def execute_cli_plan(reader, writer, plan: list[dict]) -> dict:
    result = {}

    for step in plan:
        raw = await send_ipoe(
            reader,
            writer,
            step["commands"],
        )
        result[step["key"]] = step["parser"](raw)

    return result
