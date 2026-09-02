#!/usr/bin/env python3
"""Generate the GitHub profile README from live GitHub data."""
from __future__ import annotations
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
OWNER = os.environ.get("GITHUB_OWNER", "joel220013-sys")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = Path(__file__).resolve().parents[1]
def api(path: str):
    url = "https://api.github.com" + path
    headers = {"Accept":"application/vnd.github+json","User-Agent":"github-profile-generator","X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN: headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response: return json.load(response)
def esc(value: str) -> str: return value.replace("|", "\\|").replace("\n", " ").strip()
def repo_score(repo: dict) -> float:
    return repo.get("stargazers_count",0)*5 + repo.get("forks_count",0)*2 + min(repo.get("size",0)/100,20)
def main() -> None:
    user = api(f"/users/{OWNER}")
    repos = [r for r in api(f"/users/{OWNER}/repos?per_page=100&sort=updated") if not r.get("fork") and r.get("name") != OWNER]
    public_repos, followers, following = user.get("public_repos",len(repos)), user.get("followers",0), user.get("following",0)
    languages: dict[str,int] = {}
    for repo in repos[:30]:
        try:
            for language,count in api(repo["languages_url"].replace("https://api.github.com","" )).items(): languages[language]=languages.get(language,0)+count
        except Exception: pass
    top_languages=sorted(languages.items(),key=lambda x:x[1],reverse=True)[:8]
    featured=sorted(repos,key=repo_score,reverse=True)[:6]
    recent=sorted(repos,key=lambda r:r.get("pushed_at") or "",reverse=True)[:5]
    total_stars=sum(r.get("stargazers_count",0) for r in repos); total_forks=sum(r.get("forks_count",0) for r in repos)
    now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tech_icons={"Python":"python","JavaScript":"javascript","TypeScript":"typescript","Java":"java","C":"c","C++":"cpp","HTML":"html5","CSS":"css3","Shell":"bash","Jupyter Notebook":"jupyter","Go":"go","Rust":"rust"}
    language_badges=" ".join(f'<img src="https://skillicons.dev/icons?i={tech_icons.get(lang,lang.lower().replace(" ",""))}&theme=dark" height="38" alt="{esc(lang)}" />' for lang,_ in top_languages if lang in tech_icons)
    featured_rows=[f'| **[{esc(r["name"])}](https://github.com/{OWNER}/{r["name"]})** | {esc(r.get("description") or "A project built as part of my engineering journey.")} | `{r.get("language") or "Code"}` | ⭐ {r.get("stargazers_count",0)} | `{(r.get("pushed_at") or "")[:10]}` |' for r in featured]
    recent_lines=[f'- **[{esc(r["name"])}](https://github.com/{OWNER}/{r["name"]})** — {esc(r.get("description") or "Active project")} · `{r.get("language") or "Code"}` · updated `{(r.get("pushed_at") or "")[:10]}`' for r in recent]
    readme=f'''<!-- PROFILE-GENERATED:START -->
<div align="center">

# 🛡️ JOEL JOYSON N

### Cybersecurity • Full-Stack Engineering • Applied AI • Ethical Hacking

<p align="center">
  <img src="https://raw.githubusercontent.com/{OWNER}/{OWNER}/main/assets/joel-digital-face.gif" width="300" alt="Animated digital face" />
</p>

<p>
  <a href="https://github.com/{OWNER}"><img src="https://img.shields.io/badge/GitHub-@{OWNER}-111827?style=for-the-badge&logo=github" alt="GitHub" /></a>
  <img src="https://img.shields.io/badge/Focus-Application%20Security-0f766e?style=for-the-badge&logo=shield" alt="Security" />
  <img src="https://img.shields.io/badge/Building-Secure%20Systems-312e81?style=for-the-badge" alt="Secure systems" />
</p>

> **I build security-first software, investigate how systems fail, and turn ideas into working products.**

</div>

---

## ⚡ Live Profile Telemetry

| Signal | Value | Signal | Value |
|---|---:|---|---:|
| 📦 Public repositories | **{public_repos}** | ⭐ Stars received | **{total_stars}** |
| 🍴 Forks received | **{total_forks}** | 👥 Followers | **{followers}** |
| 🔗 Following | **{following}** | 🛰️ Profile engine | **ACTIVE** |

> This section is generated automatically from GitHub data. **Last generated: `{now}`**

---

## 🧬 What I Work On

```text
┌─ CYBERSECURITY
│  ├─ Web Application Security / OWASP
│  ├─ Ethical Hacking & Security Testing
│  ├─ Secure Authentication / RBAC / API Hardening
│  └─ Linux, Networking & Defensive Engineering
│
├─ SOFTWARE ENGINEERING
│  ├─ Full-Stack Web Applications
│  ├─ REST APIs / Databases / Cloud Backends
│  └─ Automation, Testing & DevSecOps
│
└─ APPLIED AI
   ├─ AI-assisted developer tooling
   ├─ RAG / knowledge systems
   └─ Hackathon-ready intelligent MVPs
```

---

## 🧰 Detected Technology Stack

<div align="center">
{language_badges}
</div>

<p align="center">
  <img src="https://skillicons.dev/icons?i=react,nodejs,express,postgres,supabase,docker,git,github,linux,vscode&theme=dark" alt="Engineering stack" />
</p>

---

## 🚀 Featured Projects

| Project | What it is | Primary tech | ⭐ | Last push |
|---|---|---|---:|---|
{chr(10).join(featured_rows)}

---

## 📡 Recent Engineering Activity

{chr(10).join(recent_lines)}

---

## 🛡️ Security Mindset

- **Threat model first:** identify assets, trust boundaries, abuse cases, and attack surfaces before implementation.
- **Secure by default:** validation, least privilege, safe authentication, rate limits, logging, and dependency hygiene.
- **Build + break + fix:** learn by constructing systems, testing their assumptions, and hardening the weak points.
- **Ethical scope:** security testing is performed only on systems and environments where I have permission.

---

## 🎯 Current Direction

**Cybersecurity + Full Stack + AI** — building practical security products, competing in hackathons, and turning experiments into deployable systems.

<div align="center">

### `SECURE → BUILD → BREAK → LEARN → SHIP`

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:312e81,100:0f766e&height=100&section=footer" width="100%" alt="Footer" />

</div>
<!-- PROFILE-GENERATED:END -->

<!-- The workflow regenerates this README from live GitHub data. Do not edit generated content manually. -->
'''
    (ROOT/"README.md").write_text(readme,encoding="utf-8")
if __name__ == "__main__": main()
