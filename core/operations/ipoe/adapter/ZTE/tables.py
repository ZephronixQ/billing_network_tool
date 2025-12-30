# core/operations/ipoe/adapter/zte/tables.py

def print_device_info(info: dict):
    print("\n===== DEVICE INFO =====")
    print("Vendor :", info.get("vendor", "N/A"))
    print("Model  :", info.get("model", "N/A"))
    print("Ports  :", info.get("ports", "N/A"))
    print("Speed  :", info.get("speed", "N/A"))


def print_port_info(port: str, data: dict):
    print(f"\n------------ [PORT {port}] ------------")
    print("\n===== LINK =====")

    state = data.get("state", "N/A")
    speed = data.get("speed", "N/A")

    # нормализуем состояние
    if data.get("is_down") is True:
        state = "DOWN"

    print("STATE  :", state)
    print("SPEED  :", speed)

