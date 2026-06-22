# WiFi Scan

A Python-based WiFi scanner that discovers nearby wireless networks and exports the results to JSON, CSV, and HTML reports.

## Features

- Detect nearby WiFi networks
- Signal strength in dBm and quality percentage
- Channel identification
- 2.4 GHz, 5 GHz, and 6 GHz band detection
- Encryption detection
- Security warnings for weak or open networks
- Duplicate BSSID filtering
- Sort networks by signal strength
- Export results to:
  - JSON
  - CSV
  - HTML

---

## Requirements

- Python 3.9+
- Wireless adapter capable of scanning
- Windows or Linux

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/wifi-scanner.git
cd wifi-scanner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Dependencies

- pywifi
- pandas

---

## Usage

Run:

```bash
python wifi_scanner.py
```

The program will:

1. Scan nearby WiFi networks.
2. Sort networks by signal strength.
3. Display results in the console.
4. Save reports into the `wifi_scans/` folder.

---

## Example Output

```
=== WiFi Networks Found ===

HomeWiFi | 9C:AB:CD:12:34:56 | -42 dBm | 100% | CH 149 | 5 GHz | WPA2-PSK | OK

GuestWiFi | 10:22:33:44:55:66 | -68 dBm | 64% | CH 6 | 2.4 GHz | Open | Unsafe - Open Network
```

---

## Generated Reports

Each scan generates:

```
wifi_scans/
├── wifi_scan_2026-06-22_10-15-30.json
├── wifi_scan_2026-06-22_10-15-30.csv
└── wifi_scan_2026-06-22_10-15-30.html
```

---

## Signal Quality Scale

| Signal (dBm) | Quality |
|--------------|---------|
| -50 or better | Excellent |
| -60 | Very Good |
| -70 | Good |
| -80 | Fair |
| -90 | Poor |
| -100 | Very Weak |

---

## Security Ratings

| Encryption | Rating |
|------------|--------|
| Open | Unsafe |
| WPA / WPA-PSK | Weak |
| WPA2 | Secure |
| WPA3 | Most Secure |

---

## Project Structure

```
wifi-scanner/
│
├── wifi_scanner.py
├── requirements.txt
├── README.md
└── wifi_scans/
```

## Future Improvements

- Live scanning mode
- Channel congestion analysis
- Vendor lookup from MAC addresses
- Graphical dashboard
- Nearby device history
- Heatmaps
- Network change alerts
- SQLite database logging

## License

MIT License
