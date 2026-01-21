import requests

NOTION_TOKEN = "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"
DATABASE_ID = "2ef97086dda68091973acb15183ea5ac"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 1. 查询所有 Done = true 的任务
query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

query_payload = {
    "filter": {
        "property": "Done",
        "checkbox": {
            "equals": True
        }
    }
}

response = requests.post(query_url, headers=headers, json=query_payload)
tasks = response.json().get("results", [])

# 2. 把它们全部改回 false
for task in tasks:
    page_id = task["id"]
    update_url = f"https://api.notion.com/v1/pages/{page_id}"

    update_payload = {
        "properties": {
            "Done": {
                "checkbox": False
            }
        }
    }

    requests.patch(update_url, headers=headers, json=update_payload)

print(f"Reset {len(tasks)} tasks.")
