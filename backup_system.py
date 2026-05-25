# backup_system.py
import shutil
import os

def take_backup(filename):
    backup_name = filename + ".bak"
    shutil.copyfile(filename, backup_name)
    return backup_name

def restore_backup(filename):
    backup_name = filename + ".bak"
    if os.path.exists(backup_name):
        shutil.copyfile(backup_name, filename)
        return True
    return False