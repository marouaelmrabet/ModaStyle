
import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "monitoring.jsonl"

_lock = threading.Lock()

# Configuration des journaux d'erreurs
logging.basicConfig(
    filename=LOG_DIR / "errors.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


def record_request(
    latency_ms,
    status="success",
    error_type=None,
    prompt_tokens=None,
    completion_tokens=None,
    total_tokens=None
):
    """Enregistre les indicateurs d'une requête."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "latency_ms": round(latency_ms, 2),
        "status": status,
        "error_type": error_type,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens
    }

    with _lock:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    if status == "error":
        logging.error("Erreur API : %s", error_type)


def get_monitoring_stats():
    """Calcule les statistiques du monitoring."""

    if not LOG_FILE.exists():
        return {
            "total_requests": 0,
            "successful_requests": 0,
            "errors": 0,
            "error_rate_percent": 0,
            "average_latency_ms": 0,
            "p95_latency_ms": 0,
            "total_tokens": 0,
            "tokens_available": False
        }

    with _lock:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            events = [
                json.loads(line)
                for line in file
                if line.strip()
            ]

    total = len(events)
    errors = sum(event["status"] == "error" for event in events)
    successes = total - errors

    latencies = sorted(
        event["latency_ms"]
        for event in events
    )

    if latencies:
        p95_index = max(0, int(0.95 * len(latencies) + 0.999999) - 1)
        average_latency = round(mean(latencies), 2)
        p95_latency = round(latencies[p95_index], 2)
    else:
        average_latency = 0
        p95_latency = 0

    token_values = [
        event["total_tokens"]
        for event in events
        if event["total_tokens"] is not None
    ]

    error_types = Counter(
        event["error_type"]
        for event in events
        if event["status"] == "error" and event["error_type"]
    )

    return {
        "total_requests": total,
        "successful_requests": successes,
        "errors": errors,
        "error_rate_percent": round(errors / total * 100, 2) if total else 0,
        "average_latency_ms": average_latency,
        "p95_latency_ms": p95_latency,
        "total_tokens": sum(token_values),
        "tokens_available": bool(token_values),
        "error_types": dict(error_types)
    }
def get_quality_stats():
    """Récupère les dernières métriques de qualité du RAG."""

    report_path = PROJECT_ROOT / "reports" / "quality_gate_report.json"

    if not report_path.exists():
        return {
            "available": False,
            "message": "Aucun rapport de qualité disponible."
        }

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    quality = {}

    for result in report.get("results", []):
        name = result["controle"]

        if "configuration B" in name:
            quality[name] = {
                "status": result["statut"],
                "details": result["details"]
            }

    return {
        "available": True,
        "decision": report["decision"],
        "passed": report["passed"],
        "failed": report["failed"],
        "metrics": quality
    }
