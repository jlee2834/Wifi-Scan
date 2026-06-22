import pywifi
from pywifi import const
import time
import json
import pandas as pd
from datetime import datetime
from pathlib import Path


SCAN_SECONDS = 5
OUTPUT_DIR = Path("wifi_scans")


def clean_ssid(ssid):
    try:
        ssid = ssid.encode("latin1").decode("utf-8", errors="ignore")
    except Exception:
        pass

    ssid = ssid.strip()
    return ssid if ssid else "<Hidden SSID>"


def get_encryption(akm):
    if const.AKM_TYPE_NONE in akm:
        return "Open"
    if const.AKM_TYPE_WPA3 in akm:
        return "WPA3"
    if const.AKM_TYPE_WPA2 in akm:
        return "WPA2"
    if const.AKM_TYPE_WPA2PSK in akm:
        return "WPA2-PSK"
    if const.AKM_TYPE_WPA in akm:
        return "WPA"
    if const.AKM_TYPE_WPAPSK in akm:
        return "WPA-PSK"
    return "Unknown"


def get_band(freq):
    if freq < 3000:
        return "2.4 GHz"
    elif freq < 6000:
        return "5 GHz"
    else:
        return "6 GHz"


def get_channel(freq):
    if 2412 <= freq <= 2472:
        return int((freq - 2407) / 5)
    if freq == 2484:
        return 14
    if 5000 <= freq <= 5900:
        return int((freq - 5000) / 5)
    if 5955 <= freq <= 7115:
        return int((freq - 5950) / 5)
    return "Unknown"


def signal_quality(dbm):
    if dbm >= -50:
        return 100
    if dbm <= -100:
        return 0
    return 2 * (dbm + 100)


def security_warning(encryption):
    if encryption == "Open":
        return "Unsafe - Open Network"
    if encryption in ["WPA", "WPA-PSK"]:
        return "Weak - Old WPA"
    if encryption == "Unknown":
        return "Unknown Security"
    return "OK"


def scan_wifi():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        raise RuntimeError("No WiFi adapter found.")

    iface = interfaces[0]

    print(f"Using adapter: {iface.name()}")
    print(f"Scanning for {SCAN_SECONDS} seconds...")

    iface.scan()
    time.sleep(SCAN_SECONDS)

    results = iface.scan_results()
    networks = {}

    for n in results:
        ssid = clean_ssid(n.ssid)
        encryption = get_encryption(n.akm)
        band = get_band(n.freq)
        channel = get_channel(n.freq)
        quality = signal_quality(n.signal)

        entry = {
            "SSID": ssid,
            "BSSID": n.bssid,
            "Signal dBm": n.signal,
            "Signal Quality %": quality,
            "Frequency MHz": n.freq,
            "Band": band,
            "Channel": channel,
            "Encryption": encryption,
            "Security Warning": security_warning(encryption),
        }

        # De-dupe by BSSID, keeping strongest reading
        if n.bssid not in networks or n.signal > networks[n.bssid]["Signal dBm"]:
            networks[n.bssid] = entry

    return sorted(networks.values(), key=lambda x: x["Signal dBm"], reverse=True)


def save_results(networks):
    OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = OUTPUT_DIR / f"wifi_scan_{timestamp}"

    json_file = f"{base}.json"
    csv_file = f"{base}.csv"
    html_file = f"{base}.html"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(networks, f, indent=4)

    df = pd.DataFrame(networks)
    df.to_csv(csv_file, index=False)

    html = df.to_html(index=False, escape=False)

    full_html = f"""
    <html>
    <head>
        <title>WiFi Scan Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f5f5f5;
            }}
            h1 {{
                color: #222;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                background: white;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ccc;
                text-align: left;
            }}
            th {{
                background: #222;
                color: white;
            }}
            tr:nth-child(even) {{
                background: #eee;
            }}
        </style>
    </head>
    <body>
        <h1>WiFi Scan Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        {html}
    </body>
    </html>
    """

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("\nSaved:")
    print(f"- {json_file}")
    print(f"- {csv_file}")
    print(f"- {html_file}")


def print_results(networks):
    print("\n=== WiFi Networks Found ===")

    if not networks:
        print("No networks found.")
        return

    for net in networks:
        print(
            f"{net['SSID']} | "
            f"{net['BSSID']} | "
            f"{net['Signal dBm']} dBm | "
            f"{net['Signal Quality %']}% | "
            f"CH {net['Channel']} | "
            f"{net['Band']} | "
            f"{net['Encryption']} | "
            f"{net['Security Warning']}"
        )


def main():
    try:
        networks = scan_wifi()
        print_results(networks)
        save_results(networks)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
