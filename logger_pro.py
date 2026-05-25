# logger_pro.py
import logging

logging.basicConfig(filename='varlik.log', level=logging.INFO)

def log_event(action, detail):
    logging.info(f"ACTION: {action} | DETAIL: {detail}")