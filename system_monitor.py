# system_monitor.py
import psutil

class SystemMonitor:
    def get_health(self):
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "status": "OPERATIONAL"
        }