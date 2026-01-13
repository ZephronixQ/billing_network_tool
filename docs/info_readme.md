## Примеры запуска команд

### GPON (ONU)

```bash
python3 main.py --gpon XCTFAF21084E
```

Полный вывод диагностического окна GPON находится здесь:

📄 **[gpon_output.md](./gpon_output.md)**

### IPoE — диагностика (read-only)

```bash
python3 main.py --ipoe 192.168.1.24 11
```

Полный вывод диагностического окна IPoE:

📄 **[ipoe_output.md](./ipoe_output.md)**

### IPoe — управление интерфейсом

```bash
python3 main.py --ipoe 192.168.1.24 11 --restart
python3 main.py --ipoe 192.168.1.24 11 --disable
python3 main.py --ipoe 192.168.1.24 11 --enable
```

### GPON — управление интерфейсом

```bash
python3 main.py --gpon GPON00D758A0 --restart
python3 main.py --gpon GPON00D758A0 --disable
python3 main.py --gpon GPON00D758A0 --enable
python3 main.py --gpon GPON00D758A0 --remove
```

#### Конфигурация через CLI:

```bash
python3 main.py --gpon-conf --user Admin13012026 --olt 192.11.2.16 --interface 1/1/9 --enable
```

Действия логируются в `core/security/gpon_conf_actions.log`. Допустимые пользователи определены в `core/security/gpon_conf_auth.py`.

### Информационный статус

**GPON:**

```bash
python3 main.py --gpon-info-status --patch device
```

**IPoE:**

```bash
python3 main.py --ipoe-info-status --patch device
```

Результаты сохраняются в:

* `core/operations/info/output/gpon_status_result.txt`
* `core/operations/info/output/ipoe_status_result.txt`

Полный вывод окна информационного статуса:

📄 **[info_status.md](./info_status.md)**

---