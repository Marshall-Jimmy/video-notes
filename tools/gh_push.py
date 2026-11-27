#!/usr/bin/env python
"""把本地 HEAD 的内容推送到 GitHub —— 走 REST API，不走 git 协议。

为什么需要它：本机的 HTTP 代理只放通了 api.github.com，github.com:443 连不上，
`git push` 会卡在 "Failed to connect to github.com:443 over proxy"。而 gh 的 API
是可用的，所以用 Git Data API 直接建 blob/tree/commit 再移动分支指针。

用法:
    python tools/gh_push.py                 # 推送最新提交到 main
    python tools/gh_push.py --dry-run
    python tools/gh_push.py --branch main --repo owner/name

注意:
    * 它把「本地 HEAD 的 tree + 本地 HEAD 的提交信息」做成一个新 commit，
      父提交是**远端当前 main**。所以本地与远端历史不共享祖先，但内容完全一致。
    * 远端 tree 已与本地 HEAD 一致时直接跳过（不会产生空提交）。
    * 需要 `gh auth login` 过，脚本用 `gh auth token` 取令牌。
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"


def git(*args, raw=False):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args],
                       capture_output=True, check=True)
    return p.stdout if raw else p.stdout.decode().strip()


def make_api(token: str):
    def api(method, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(f"{API}{path}", data=data, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "vidsum-gh-push")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                body = r.read().decode()
                return json.loads(body) if body.strip() else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:300]
            raise SystemExit(f"{method} {path} -> {e.code}: {detail}")

    return api


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None, help="owner/name，默认从 origin 解析")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--message", default=None, help="默认用本地 HEAD 的提交信息")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo = args.repo
    if not repo:
        url = git("remote", "get-url", "origin")
        repo = url.rstrip("/").removesuffix(".git").split("github.com")[-1].lstrip(":/")
    token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    if not token:
        raise SystemExit("拿不到 gh 令牌，先 gh auth login")
    api = make_api(token)

    local_tree = git("rev-parse", "HEAD^{tree}")
    ref = api("GET", f"/repos/{repo}/git/ref/heads/{args.branch}")
    remote_head = ref["object"]["sha"]
    remote_tree = api("GET", f"/repos/{repo}/git/commits/{remote_head}")["tree"]["sha"]

    print(f"repo      {repo}")
    print(f"local     HEAD tree {local_tree[:10]}")
    print(f"remote    {args.branch} {remote_head[:10]} tree {remote_tree[:10]}")

    if local_tree == remote_tree:
        print("远端内容已与本地 HEAD 一致，无需推送。")
        return 0

    entries = []
    lines = [l for l in git("ls-tree", "-r", "-z", "HEAD", raw=True).split(b"\0") if l]
    for i, line in enumerate(lines, 1):
        meta, path = line.split(b"\t", 1)
        mode, _typ, sha = meta.decode().split()
        content = git("cat-file", "blob", sha, raw=True)
        blob = api("POST", f"/repos/{repo}/git/blobs",
                   {"content": base64.b64encode(content).decode(), "encoding": "base64"})
        assert blob["sha"] == sha, f"blob sha 不一致: {path!r}"
        entries.append({"path": path.decode("utf-8"), "mode": mode,
                        "type": "blob", "sha": blob["sha"]})
        if i % 25 == 0 or i == len(lines):
            print(f"  blobs {i}/{len(lines)}")

    if args.dry_run:
        print(f"[dry-run] 将推送 {len(entries)} 个文件")
        return 0

    tree = api("POST", f"/repos/{repo}/git/trees", {"tree": entries})
    if tree["sha"] != local_tree:
        print(f"⚠ 远端树 {tree['sha'][:10]} 与本地 {local_tree[:10]} 不一致（可能被 .gitattributes 影响）")

    message = args.message or git("log", "-1", "--format=%B")
    an, ae, ad = git("log", "-1", "--format=%an%x00%ae%x00%aI").split("\x00")
    commit = api("POST", f"/repos/{repo}/git/commits", {
        "message": message, "tree": tree["sha"], "parents": [remote_head],
        "author": {"name": an, "email": ae, "date": ad},
        "committer": {"name": an, "email": ae, "date": ad},
    })
    api("PATCH", f"/repos/{repo}/git/refs/heads/{args.branch}",
        {"sha": commit["sha"], "force": False})
    print(f"✔ 已推送 {commit['sha'][:10]}  → https://github.com/{repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
