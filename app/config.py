import os
import os
from pathlib import Path

# Этот код сделает путь "железным" и понятным для системы
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, "expenses.db")