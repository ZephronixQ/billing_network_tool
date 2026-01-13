# Проект "Billing Network Tool"

## Цель и описание

**Billing Network Tool** — учебно-практический асинхронный CLI-инструмент для диагностики и управления оборудованием доступа (**GPON / IPoE**), ориентированный на **стабильную работу в одной Telnet-сессии** и **строго контролируемое выполнение команд**.  

Проект помогает:

* автоматизировать сетевые операции (GPON, OLT, ONU, IPOE);
* взаимодействовать с сетевым оборудованием через Telnet/CLI;
* структурировать код и использовать модульный подход;
* работать с логами, диагностикой и мониторингом сетевых компонентов.

Проект предназначен для инженеров, которые хотят перейти от ручного администрирования к программному управлению сетями с использованием Python и современных инженерных практик.

[![Latest Version](https://img.shields.io/github/tag/ZephronixQ/billing_network_tool.svg)](https://github.com/ZephronixQ/billing_network_tool/releases)
[![Download Count](https://img.shields.io/github/downloads/ZephronixQ/billing_network_tool/total)](https://github.com/ZephronixQ/billing_network_tool/releases)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://github.com/ZephronixQ/billing_network_tool/tree/main/docs)

---

### Поддерживаемое оборудование

**GPON:**

* ZTE ZXAN OLT (модели C300 и C320)

**IPoE:**

* DLINK (DGS-1100-10/ME, DES-1210-28/ME)
* ELTEX (MES2348B, MES1124MB)
* SNR (S2965-8T, S2965-24T, S2985G-24T, S2985G-48T, S2990G-48T)
* ZTE (ZXR10-2992E)

> Поддержка охватывает диагностику (read-only) и контролируемое управление портами для всех перечисленных моделей.

---

### Принципы работы

* **One Session – One Request:** все команды выполняются в рамках одной Telnet-сессии без переподключений.
* **Строгий контроль CLI prompt** (`>`, `#`, `(cfg)#`) для корректного чтения вывода.
* **Отсутствие повторных retry-циклов и sleep-based polling.**
* **Разделение read-only и контролируемых операций** — изменения конфигурации выполняются только при явном подтверждении и поддерживаются для всех вендоров через единый интерфейс управления.
* **Безопасность и стабильность:** операции, влияющие на конфигурацию или состояние оборудования, изолированы от диагностических команд.
* 
---

## Использование

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/ZephronixQ/billing_network_tool.git
    ```

2. Установите зависимости:

    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. Ознакомьтесь с доступными командами проекта:

    ```bash
    python3 main.py --help
    ```

---

## Примеры запуска команд

См. файл [info_readme.md](docs/info_readme.md) для информации о запуске команд.

---

## Архитектура проекта

Полная актуальная схема проекта находится здесь:

📄 **[cheme.txt](./cheme.txt)**

(включает GPON + IPoE, adapters, parsers, tables, render и vendor-логику)

---

## Лицензия

См. файл [LICENSE](LICENSE) для информации о лицензии.

## Вклад

Прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) для информации о том, как внести вклад в проект.

## Журнал изменений

См. файл [CHANGELOG.md](docs/CHANGELOG.md) для истории изменений.

## Список задач

См. файл [TODO.md](docs/TODO.md) для текущих задач и планов развития.

## Кодекс поведения

Участвуя в проекте, вы соглашаетесь соблюдать наш [кодекс поведения](CODE_OF_CONDUCT.md).
