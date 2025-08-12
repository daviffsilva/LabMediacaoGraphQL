import os
import time
import json
import requests


TOKEN = os.getenv("GITHUB_TOKEN") or "TOKEN"
URL_GQL = "https://api.github.com/graphql"
URL_REST_SEARCH = "https://api.github.com/search/repositories"
UA = "LabMediacaoGraphQL"


headers_rest = {
    "Authorization": f"bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": UA,
}
headers_gql = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": UA,
}


def get_top100_by_stars():
    params = {
        "q": "stars:>1",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": 1,
    }
    r = requests.get(URL_REST_SEARCH, headers=headers_rest, params=params, timeout=30)
    r.raise_for_status()
    items = r.json().get("items", [])
    return [(it["owner"]["login"], it["name"]) for it in items]


gql_query = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    name
    owner { login }
    createdAt
    updatedAt
    primaryLanguage { name }
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
    issues { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    stargazerCount
  }
}
"""

def fetch_repo_metrics(owner, name):
    payload = {"query": gql_query, "variables": {"owner": owner, "name": name}}
    r = requests.post(URL_GQL, headers=headers_gql, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["repository"]

def main():
    try:
        repos = get_top100_by_stars()
    except Exception as e:
        print("Falha ao listar top 100 via REST:", e)
        return

    collected = []
    for i, (owner, name) in enumerate(repos, 1):
        try:
            rec = fetch_repo_metrics(owner, name)
            collected.append(rec)
            print(f"[{i}/100] OK  {owner}/{name}")
        except Exception as e:
            print(f"[{i}/100] ERRO {owner}/{name}: {e}")
        time.sleep(0.25)

    with open("repos_top100.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": collected}, f, ensure_ascii=False, indent=2)




if __name__ == "__main__":
    main()
