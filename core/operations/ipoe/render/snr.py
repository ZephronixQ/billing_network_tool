from core.operations.ipoe.adapter.SNR.tables.snr_report import print_port_report


class SNRRenderer:
    def render(self, data: dict, port: str) -> None:
        if data.get("unsupported"):
            print("\n⚠ Устройство не поддерживается")
            print(f"MODEL : {data.get('model')}")
            return

        print_port_report(
            port=port,
            model=data.get("model"),
            iface=data.get("port", {}),
            mac=data.get("mac"),
            logs=data.get("logs", []),
        )
