from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from config import DOWNLOAD_DIR, TASK_CLEANUP_TIME, MAX_WORKERS
from json_utils import load_tasks, save_tasks, load_keys
from auth import check_memory_limit
import yt_dlp, os, threading, json, time, shutil
from yt_dlp.utils import download_range_func

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
# ... existing code ... 