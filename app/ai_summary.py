import random

def generate_mock_summary(df):
    event_types = df["event_type"].value_counts().to_dict() if "event_type" in df.columns else {}
    ips = df["source_ip"].value_counts().head(3).to_dict() if "source_ip" in df.columns else {}

    summary = [
        "• Detected common event patterns in the uploaded logs.",
        "• No critical anomalies detected.",
        "• Frequent events observed:",
    ]

    for event, count in event_types.items():
        summary.append(f"   - {event}: {count} occurrences")

    if ips:
        summary.append("• Top source IPs observed:")
        for ip, count in ips.items():
            summary.append(f"   - {ip} ({count} logs)")

    summary.append("• Recommend further analysis for any login_failure events.")
    
    if random.random() > 0.7:
        summary.append("• No signs of brute force or unusual login bursts.")

    return "\n".join(summary)
