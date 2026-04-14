import hashlib
import time
import random
import os
import json
import uuid
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn
from typing import Optional

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()

# --- 路径配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOID_DIR = os.path.join(BASE_DIR, ".void")
INDEX_FILE = os.path.join(VOID_DIR, "index")
LOG_FILE = os.path.join(VOID_DIR, "history.json")
CONFIG_FILE = os.path.join(VOID_DIR, "config.json")
STASH_FILE = os.path.join(VOID_DIR, "stash.json")

def init_storage():
    if not os.path.exists(VOID_DIR): os.makedirs(VOID_DIR)
    defaults = {
        INDEX_FILE: [], LOG_FILE: [], STASH_FILE: [],
        CONFIG_FILE: {"user": {"name": "Void_Walker", "email": "none@void.local"}, "branch": "main"}
    }
    for path, data in defaults.items():
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2)

def get_data(f): init_storage(); return json.load(open(f, "r", encoding="utf-8"))
def set_data(f, d): json.dump(d, open(f, "w", encoding="utf-8"), indent=2)

# --- 1. 配置与初始化 ---

@app.command()
def init():
    """初始化虚空仓库"""
    init_storage()
    console.print(f"[bold green]Initialized empty Void repository in {BASE_DIR}/.void/[/]")

@app.command()
def config(
    global_flag: bool = typer.Option(False, "--global"),
    name: str = typer.Option(None, "--user.name", "--name"),
    email: str = typer.Option(None, "--user.email", "--email")
):
    """配置身份"""
    cfg = get_data(CONFIG_FILE)
    if name or email:
        if name: cfg["user"]["name"] = name
        if email: cfg["user"]["email"] = email
        set_data(CONFIG_FILE, cfg)
        console.print(f"[green]Identity updated.[/]")
    console.print(f"[cyan]Current:[/] {cfg['user']['name']} <{cfg['user']['email']}>")

# --- 2. 基础操作 ---

@app.command()
def add(item: str):
    """添加概念到暂存区"""
    staged = get_data(INDEX_FILE)
    target = f"Everything_in_{os.path.basename(BASE_DIR)}" if item == "." else item
    if target not in staged:
        staged.append(target)
        set_data(INDEX_FILE, staged)
    console.print(f"[white]indexed: {target}[/]")

@app.command()
def commit(m: str = typer.Option(..., "--message", "-m"), all: bool = typer.Option(False, "-a")):
    """提交快照"""
    staged = get_data(INDEX_FILE)
    if all and not staged: staged = ["Auto_detected_void_change"]
    if not staged:
        console.print("[yellow]nothing to commit, working tree clean[/]")
        return
    cfg, history = get_data(CONFIG_FILE), get_data(LOG_FILE)
    h = hashlib.sha1(str(uuid.uuid4()).encode()).hexdigest()
    with console.status("[white]Collapsing dimensions..."): time.sleep(0.5)
    history.insert(0, {"hash": h, "message": m, "author": cfg["user"], "branch": cfg["branch"], "date": time.ctime()})
    set_data(LOG_FILE, history); set_data(INDEX_FILE, [])
    console.print(f"[{cfg['branch']} {h[:7]}] {m}\n {len(staged)} concepts dissolved.")

@app.command()
def status():
    """查看状态"""
    staged, cfg = get_data(INDEX_FILE), get_data(CONFIG_FILE)
    console.print(f"[white]On branch [bold]{cfg['branch']}[/][/]")
    if not staged: console.print("nothing to commit, working tree clean")
    else:
        console.print("Changes to be committed:")
        for i in staged: console.print(f"\t[green]new concept:   {i}[/]")

@app.command()
def log(oneline: bool = typer.Option(False, "--oneline")):
    """查看历史"""
    history = get_data(LOG_FILE)
    for e in history:
        if oneline: console.print(f"[yellow]{e['hash'][:7]}[/] [white]{e['message']}[/]")
        else: console.print(f"[yellow]commit {e['hash']}[/]\nAuthor: {e['author']['name']} <{e['author']['email']}>\nDate: {e['date']}\n\n    {e['message']}\n")

# --- 3. 撤销、恢复与 Stash ---

@app.command()
def reset(hard: bool = typer.Option(False, "--hard")):
    """重置暂存区"""
    set_data(INDEX_FILE, [])
    console.print("[red]HEAD is now at last commit.[/]" if hard else "Unstaged changes.")

@app.command()
def stash(do_pop: bool = typer.Option(False, "--pop")):
    """暂存/弹出 (stash/pop)"""
    st, idx, cfg = get_data(STASH_FILE), get_data(INDEX_FILE), get_data(CONFIG_FILE)
    if do_pop:
        if not st: console.print("[yellow]No stash found.[/]"); return
        set_data(INDEX_FILE, st.pop()); set_data(STASH_FILE, st)
        console.print("Dropped stash@{0} and restored state.")
    else:
        if not idx: console.print("[yellow]No changes to stash.[/]"); return
        st.append(idx); set_data(STASH_FILE, st); set_data(INDEX_FILE, [])
        console.print(f"Saved WIP on {cfg['branch']}")

# --- 4. 分支操作 (支持 checkout -b) ---

@app.command()
def branch(name: Optional[str] = typer.Argument(None)):
    """列出或创建分支"""
    cfg = get_data(CONFIG_FILE)
    if not name: console.print(f"* [green]{cfg['branch']}[/]\n  master\n  dev")
    else: console.print(f"Branch '{name}' created.")

@app.command()
def checkout(name: str = typer.Argument(...), b: bool = typer.Option(False, "-b")):
    """切换或新建并切换分支"""
    cfg = get_data(CONFIG_FILE)
    if b: console.print(f"Switched to a new branch '{name}'")
    else: console.print(f"Switched to branch '{name}'")
    cfg["branch"] = name
    set_data(CONFIG_FILE, cfg)

# --- 5. 远程协作 (肌肉记忆优化版) ---

@app.command()
def remote(action: Optional[str] = typer.Argument(None), name: Optional[str] = typer.Argument(None), url: Optional[str] = typer.Argument(None)):
    """管理远程仓库"""
    if action == "add" and name and url: console.print(f"Added remote {name} {url}")
    else: console.print("origin  https://void-cloud.sentinx.local/repos (fetch/push)")

@app.command()
def push(remote: Optional[str] = typer.Argument(None), branch: Optional[str] = typer.Argument(None)):
    """上传 (支持 void push origin main)"""
    r, b = remote or "origin", branch or get_data(CONFIG_FILE)["branch"]
    with Progress(SpinnerColumn(), TextColumn(f"[bold blue]Pushing to {r}/{b}..."), BarColumn()) as p:
        t = p.add_task("", total=100)
        for _ in range(10): time.sleep(0.05); p.advance(t, 10)
    console.print(f"To https://void-cloud.sentinx.local\n   [green]main -> {b}[/]")

@app.command()
def pull(remote: Optional[str] = typer.Argument(None), branch: Optional[str] = typer.Argument(None)):
    """拉取 (支持 void pull origin main)"""
    r = remote or "origin"
    console.print(f"Fetching {r}..."); time.sleep(0.3)
    console.print("Fast-forwarded to latest entropy.")

if __name__ == "__main__": app()
