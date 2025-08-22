import os
import csv
import time
import json
import requests
from datetime import datetime

TOKEN = os.getenv("GITHUB_TOKEN") or "TOKEN"  
URL_GQL = "https://api.github.com/graphql"
URL_REST_SEARCH = "https://api.github.com/search/repositories"
UA = "LabMediacaoGraphQL"

headers_rest = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": UA,
}
headers_gql = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": UA,
}

# -------- Sprint 2: listar 1000 (10 páginas de 100) --------
def list_top_repos_rest(limit=1000, per_page=100, max_retries=3):
    owners_names = []
    pages = (limit + per_page - 1) // per_page
    for page in range(1, pages + 1):
        params = {
            "q": "stars:>1",
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }
        attempt = 0
        while True:
            attempt += 1
            r = requests.get(URL_REST_SEARCH, headers=headers_rest, params=params, timeout=60)

            if r.status_code == 403:
                reset = r.headers.get("X-RateLimit-Reset")
                wait = max(30, (int(reset) - int(time.time())) if reset else 60)
                print(f"[REST] 403 rate-limited. Aguardando {wait}s...")
                time.sleep(wait)
                continue
            if r.status_code >= 500 and attempt <= max_retries:
                wait = 1.6 ** (attempt - 1)
                print(f"[REST] {r.status_code} (página {page}). Retry em {wait:.1f}s...")
                time.sleep(wait)
                continue
            r.raise_for_status()
            break

        items = r.json().get("items", [])
        owners_names.extend([(it["owner"]["login"], it["name"]) for it in items])
        print(f"[REST] Página {page}/{pages}: +{len(items)} repos")
        time.sleep(0.4)


    owners_names = list(dict.fromkeys(owners_names))[:limit]
    return owners_names

# -------- GraphQL: suas métricas (RQ01–RQ06) --------
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

def fetch_repo_metrics(owner, name, max_retries=4):
    payload = {"query": gql_query, "variables": {"owner": owner, "name": name}}
    for attempt in range(1, max_retries + 1):
        r = requests.post(URL_GQL, headers=headers_gql, json=payload, timeout=60)
        if r.status_code >= 500 and attempt < max_retries:
            wait = 1.6 ** (attempt - 1)
            print(f"[GQL] {r.status_code} {owner}/{name} — retry em {wait:.1f}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        data = r.json()
        if "errors" in data:

            raise RuntimeError(data["errors"])
        return data["data"]["repository"]

def iso_to_date(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).date().isoformat()
    except Exception:
        return iso

def main():
    N = 1000
    print(f"==> Listando top {N} repositórios por estrelas (REST)...")
    try:
        repos = list_top_repos_rest(limit=N, per_page=100)
    except Exception as e:
        print("Falha ao listar via REST:", e)
        return
    print(f"Total para coletar (GQL): {len(repos)}")

    rows = []
    for i, (owner, name) in enumerate(repos, 1):
        try:
            rec = fetch_repo_metrics(owner, name)
            if not rec:
                raise RuntimeError("Resposta vazia")
            row = {
                "owner": rec["owner"]["login"],
                "name": rec["name"],
                "createdAt": rec["createdAt"],
                "updatedAt": rec["updatedAt"],
                "createdDate": iso_to_date(rec["createdAt"]),
                "updatedDate": iso_to_date(rec["updatedAt"]),
                "primaryLanguage": (rec["primaryLanguage"]["name"] if rec["primaryLanguage"] else None),
                "mergedPRs": rec["pullRequests"]["totalCount"],
                "releases": rec["releases"]["totalCount"],
                "issuesTotal": rec["issues"]["totalCount"],
                "issuesClosed": rec["closedIssues"]["totalCount"],
                "stargazers": rec["stargazerCount"],
            }
            row["issuesClosedRatio"] = (
                round(row["issuesClosed"] / row["issuesTotal"], 4) if row["issuesTotal"] else None
            )
            rows.append(row)
            print(f"[{i}/{N}] OK  {owner}/{name}")
        except Exception as e:
            print(f"[{i}/{N}] ERRO {owner}/{name}: {e}")
        time.sleep(0.18)  # folga para rate limit

    # JSON completo
    with open("repos_top1000.json", "w", encoding="utf-8") as jf:
        json.dump(rows, jf, ensure_ascii=False, indent=2)


    fieldnames = [
        "owner", "name",
        "createdAt", "updatedAt", "createdDate", "updatedDate",
        "primaryLanguage",
        "mergedPRs", "releases",
        "issuesTotal", "issuesClosed", "issuesClosedRatio",
        "stargazers",
    ]
    with open("repos_top1000.csv", "w", encoding="utf-8", newline="") as cf:
        w = csv.DictWriter(cf, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)



if __name__ == "__main__":
    main()
