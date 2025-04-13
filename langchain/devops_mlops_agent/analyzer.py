def classify_severity(log_entry):
    keywords = {
        "critical": ["exception", "outage", "panic"],
        "high": ["failed", "error"],
        "medium": ["timeout", "retry"],
        "low": ["info", "connected"]
    }
    for sev, words in keywords.items():
        if any(w in log_entry.lower() for w in words):
            return sev
    return "unknown"

def assign_team(log_entry):
    if "db" in log_entry.lower():
        return "DBA Team"
    elif "auth" in log_entry.lower():
        return "Security Team"
    elif "timeout" in log_entry.lower():
        return "Networking Team"
    else:
        return "DevOps Team"
