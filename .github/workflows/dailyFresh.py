import os
import requests

# ✅ 从环境变量读取，而不是写死
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# 查询所有 Done = true 的任务
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

# 把它们全部改回 false
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
