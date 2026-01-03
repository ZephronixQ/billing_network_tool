from core.operations.ipoe.adapter.base import BaseIPoEAdapter
from core.operations.ipoe.adapter.SNR.query import build_query_plan
from core.operations.ipoe.adapter.SNR.constants import (
    SNR_MODEL_PORTS,
)
from core.operations.ipoe.adapter.SNR.commands import (
    DISABLE_PAGING,
    SHOW_VERSION,
)
from core.operations.ipoe.common.utils import (
    normalize_port,
    parse_snr_device_model,
)
from core.connection.telnet import (
    send_ipoe,
    SNR_PROMPT_RE,
)

class SNRIPoeAdapter(BaseIPoEAdapter):
    vendor = "SNR"

    async def collect(self, port: str) -> dict:
        port = normalize_port(port)

        await send_ipoe(
            self.reader,
            self.writer,
            [DISABLE_PAGING],
            prompt_re=SNR_PROMPT_RE,
        )

        raw_version = await send_ipoe(
            self.reader,
            self.writer,
            [SHOW_VERSION],
            prompt_re=SNR_PROMPT_RE,
        )
        model = parse_snr_device_model(raw_version)

        if model not in SNR_MODEL_PORTS:
            return {
                "unsupported": True,
                "model": model,
            }

        result = {
            "unsupported": False,
            "model": model,
        }

        for step in build_query_plan(port, model):
            # обычные команды
            if step["commands"]:
                raw = await send_ipoe(
                    self.reader,
                    self.writer,
                    [step["commands"]],
                    prompt_re=SNR_PROMPT_RE,
                    handle_paging=step.get("paging", False),
                )
                result[step["key"]] = step["parser"](raw)
            else:
                # специальные сборщики (logs и т.п.)
                result[step["key"]] = await step["parser"](
                    self.reader,
                    self.writer,
                    port,
                )

        return result
