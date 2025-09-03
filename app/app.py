import random
import os
import string
import time
import threading
import uuid
import json
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

TEMPLATES_HP = [
    "Wingardium Leviosa! A feather floats gracefully.",
    "Expecto Patronum! A silvery guardian bursts forth.",
    "Accio metrics! Fetching performance insights.",
    "Alohomora: unlocking a stubborn cache.",
    "Lumos maxima—lighting up the debug logs.",
    "Finite Incantatem: rolling back a miscast deploy.",
    "Protego! Rate limiter shield engaged.",
    "Azkaban outage averted. Re-routing traffic.",
    "Mischief managed: cleanup task completed.",
    "Felix Felicis run—error odds temporarily reduced."
]

TEMPLATES_SW = [
    "The Force will be with you. Always.",
    "Do. Or do not. There is no try.",
    "I’ve got a bad feeling about this log.",
    "Execute Order 66: terminating connections.",
    "Red Five standing by—heartbeat confirmed.",
    "It’s a trap! Circuit breaker triggered.",
    "Hyperdrive offline. Fallback initiated.",
    "You were the chosen one! Crash on startup.",
    "These aren’t the logs you’re looking for.",
    "The logs awaken: anomaly detected."
]

PATHS_HP = [
    "/hogwarts/spells/cast",
    "/hogwarts/potions/brew",
    "/hogwarts/commonroom/entry",
    "/hogwarts/quidditch/score",
    "/hogwarts/darkarts/defense"
]

PATHS_SW = [
    "/rebellion/base/status",
    "/empire/orders/execute",
    "/jedi/temple/train",
    "/sith/temple/ruleoftwo",
    "/falcon/maintenance/log"
]

TEMPLATES = TEMPLATES_HP + TEMPLATES_SW
PATHS = PATHS_HP + PATHS_SW
METHODS = ["GET", "POST", "PUT", "DELETE"]
HTTP_URL = os.environ.get('HTTP_URL',"http://undefined.local")
FILE_PATH = os.environ.get('FILE_PATH',"/dev/null")

def _now():
    return datetime.now(timezone.utc)

def _floor_to_minute(dt: datetime, minutes: int) -> datetime:
    discard = timedelta(
        minutes=dt.minute % minutes,
        seconds=dt.second,
        microseconds=dt.microsecond
    )
    return dt - discard

def _is_spike(now):
    floored = _floor_to_minute(now, 15)
    return (now - floored).seconds < 180  # 3-minute spike window

def _choose_status_code(base_success_rate=0.95, spike=False) -> int:
    if spike:
        error_chance = 0.20
    else:
        error_chance = 1.0 - base_success_rate

    if random.random() > error_chance:
        return 200

    return random.choice(
        [400, 401, 403, 404, 408, 429] if random.random() < 0.7
        else [500, 502, 503, 504]
    )

def _response_time_ms(base_min=100, base_max=1500, spike=False):
    if spike and random.random() < 0.3:
        return random.randint(1500, 3000)
    return random.randint(base_min, base_max)

def _pick_event_type(status_code: int) -> str:
    if status_code >= 500:
        return "ERROR"
    if status_code >= 400:
        return "WARN"
    return "INFO"

def _generate_log_json():
    now = _now()
    message = random.choice(TEMPLATES)
    path = random.choice(PATHS)
    method = random.choice(METHODS)
    spike = _is_spike(now)
    status_code = _choose_status_code(spike=spike)
    return json.dumps({
        "timestamp": now.isoformat(),
        "message": message,
        "path": path,
        "log_level": _pick_event_type(status_code),
        "status_code": status_code,
        "response_time": _response_time_ms(spike=spike),
        "method": method
    })

def _generate_log_pipe():
    now = _now()
    message = random.choice(TEMPLATES)
    path = random.choice(PATHS)
    method = random.choice(METHODS)
    spike = _is_spike(now)
    status_code = _choose_status_code(spike=spike)
    return (
        f"{now.isoformat()} | "
        f"MESSAGE={message} "
        f"PATH={path} "
        f"LOG_LEVEL={_pick_event_type(status_code)} "
        f"STATUS_CODE={status_code} "
        f"RESPONSE_TIME={_response_time_ms(spike=spike)} "
        f"METHOD={method}"
    )

def emit_logs(log_fn, label: str, rate_per_sec: int = 100):
    success_count = 0
    last_log = time.time()
    while True:
        start = time.time()
        for _ in range(rate_per_sec):
            log = log_fn()
            try:
                if HTTP_URL != "http://undefined.local":
                    resp = requests.post(HTTP_URL, data=log, headers={"Content-Type": "application/json"}, timeout=5)
                    if resp.status_code == 200:
                        success_count += 1
                elif FILE_PATH != "/dev/null":
                    if not os.path.exists(os.path.dirname(FILE_PATH)):
                        os.makedirs(os.path.dirname(FILE_PATH))
                    with open(FILE_PATH, "a") as f:
                        f.write(log)
                else:
                    print(log, flush=True)
            except Exception as e:
                print(f"[{label}] Failed to send log: {e}")

def main():
    json_thread = threading.Thread(target=emit_logs, args=(_generate_log_json, "JSON"))
    pipe_thread = threading.Thread(target=emit_logs, args=(_generate_log_pipe, "PIPE"))
    json_thread.start()
    pipe_thread.start()
    json_thread.join()
    pipe_thread.join()

if __name__ == "__main__":
    main()
