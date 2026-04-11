import requests

memos = [
    {
        "project": "BellyUp",
        "title": "Bug Fix: XML Syntax Corruption in .alp",
        "text": "Fixed critical compilation failures caused by HTML entity encoding (&lt;, &gt;) for Java generics inside the .alp XML. Standardized java.util.ArrayDeque and Map declarations."
    },
    {
        "project": "BellyUp",
        "title": "Logic Fix: Real-time Seat Utilization Tracking",
        "text": "Resolved 0% Seat Usage bug. Implemented Headcount sync: incrementing occupiedSeats in executeTableAssignment and decrementing in pedSink1 onExit. Formula: (occupiedSeats / 402 * 100)."
    },
    {
        "project": "BellyUp",
        "title": "Feature: Expansion to 8-Station Food Tracking",
        "text": "Scaled buffet station tracking from 4 to 8 (Seafood, Dim Sum, Buffet, Beverage, Meat, Sushi, Candies, Ice Cream). Injected corresponding DataSet XML blocks and updated the main event loop for background recording."
    },
    {
        "project": "BellyUp",
        "title": "Discovery: Operations Diagnostic - Busboy Bottleneck",
        "text": "Simulation analysis revealed high customer balking (327+ lost) is primarily caused by 100% busboy utilization. 8 busboys cannot keep up with the arrival rate (3.5/min) and 5.5min clean time, leaving tables dirty and lobbies full."
    }
]

url = "http://localhost:37777/api/memory/save"
for memo in memos:
    try:
        response = requests.post(url, json=memo)
        print(f"Saved '{memo['title']}': {response.status_code}")
    except Exception as e:
        print(f"Failed to save '{memo['title']}': {e}")
