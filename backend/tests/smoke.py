#!/usr/bin/env python3
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("SMOKE_BASE", "http://127.0.0.1:8001").rstrip("/")
USER = os.environ.get("SMOKE_USER", "smoke_user")
PASSWD = os.environ.get("SMOKE_PASSWD", "smoke_pass_123")
# 单个请求的超时。设短一点：后端崩在崩溃循环里时，连接会被"接受但不应答"，
# 超时太长会让整个 smoke 卡到外层超时，反而看不到是哪一项失败。
REQ_TIMEOUT = float(os.environ.get("SMOKE_TIMEOUT", "8"))

_results = []


def check(name, ok, detail=""):
    _results.append((name, bool(ok)))
    mark = "✅" if ok else "❌"
    line = f"  {mark} {name}"
    if detail and not ok:
        line += f"\n       └─ {detail}"
    print(line, flush=True)


def call(method, path, *, json_body=None, headers=None, body=None, ctype=None):
    url = BASE + path
    h = dict(headers or {})
    data = body
    if json_body is not None:
        data = json.dumps(json_body).encode()
        h["Content-Type"] = "application/json"
    if ctype:
        h["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=REQ_TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # 连不上等
        return 0, f"{type(e).__name__}: {e}"


def multipart(fields, files):
    """files: {字段名: (文件名, bytes)}"""
    boundary = "----smoke" + str(int(time.time() * 1000))
    buf = b""
    for k, v in fields.items():
        buf += (
            f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'
        ).encode()
    for k, (fname, content) in files.items():
        buf += (
            f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; '
            f'filename="{fname}"\r\nContent-Type: application/octet-stream\r\n\r\n'
        ).encode()
        buf += content + b"\r\n"
    buf += f"--{boundary}--\r\n".encode()
    return buf, f"multipart/form-data; boundary={boundary}"


def main():
    print(f"=== smoke 基线 @ {BASE} ===")
    print(f"    用户 {USER}  ·  {time.strftime('%H:%M:%S')}")

    # 1. 注册（已存在也算通过 —— 用户是固定复用的）
    st, raw = call("POST", "/registry", json_body={"usrname": USER, "passwd": PASSWD})
    check("POST /registry", raw.strip() in ("1", "-2"), f"HTTP {st} body={raw[:100]}")

    # 2. 登录拿 token
    st, raw = call("POST", "/login", json_body={"usrname": USER, "passwd": PASSWD})
    token, uid = None, None
    try:
        j = json.loads(raw)
        token, uid = j.get("token"), j.get("id")
    except Exception:
        pass
    check("POST /login 拿到 token", bool(token), f"HTTP {st} body={raw[:120]}")

    # 3. 用户名查重（已存在应返回 0）
    st, raw = call("POST", "/checkTmpName", json_body={"usrname": USER})
    check("POST /checkTmpName 返回 0", raw.strip() == "0", f"HTTP {st} body={raw[:80]}")

    if not token:
        print("\n  登录失败，后面的鉴权流程无法继续")
        return 1

    auth = {"token": token}

    # 4. 鉴权端点
    st, raw = call("GET", "/home/info", headers=auth)
    ok = False
    try:
        ok = json.loads(raw).get("usr_name") == USER
    except Exception:
        pass
    check("GET /home/info（token 鉴权）", ok, f"HTTP {st} body={raw[:120]}")

    st, raw = call("GET", "/home/", headers=auth)
    check("GET /home/", st == 200, f"HTTP {st} body={raw[:80]}")

    # 5. 分片上传：把一段内容切成 3 片
    payload = ("smoke payload " + str(int(time.time())) + "\n").encode() * 8
    third = max(1, len(payload) // 3)
    chunks = [payload[i : i + third] for i in range(0, len(payload), third)]
    fname = f"smoke_{int(time.time())}.bin"
    base = 0
    upload_ok = True
    for i, chunk in enumerate(chunks):
        digest = hashlib.md5(chunk).hexdigest()
        body, ctype = multipart(
            {
                "hash": digest,
                "start": base,
                "end": base + len(chunk),
                "index": str(i),
                "file_name": fname,
            },
            {"blob": (f"chunk{i}", chunk)},
        )
        st, raw = call("POST", "/home/upload_f", headers=auth, body=body, ctype=ctype)
        if "114514" not in raw:
            upload_ok = False
            print(f"       分片 {i} 失败：HTTP {st} {raw[:120]}")
        base += len(chunk)
    check(f"POST /home/upload_f × {len(chunks)} 片", upload_ok)

    # 6. 读回调（memo）
    st, raw = call("GET", f"/home/finish_file/{fname}", headers=auth)
    ok = False
    try:
        d = json.loads(raw)
        ok = isinstance(d, dict) and len(d) == len(chunks)
    except Exception:
        pass
    check("GET /home/finish_file/{name}", ok, f"HTTP {st} body={raw[:140]}")

    # 7. 合并 + 入库
    st, raw = call("GET", f"/home/upload_f_end/{fname}?n=smoke&cc=0", headers=auth)
    ok = False
    try:
        j = json.loads(raw)
        ok = j.get("detail") == "上传成功"
    except Exception:
        pass
    check("GET /home/upload_f_end/{name}（合并入库）", ok, f"HTTP {st} body={raw[:140]}")

    # 8. 文件列表（当前是半成品，只验证可达性）
    st, raw = call("GET", "/home/my_file", headers=auth)
    check("GET /home/my_file（可达）", st == 200, f"HTTP {st} body={raw[:100]}")

    # 9. 注销
    st, raw = call("GET", "/logout", headers=auth)
    check("GET /logout", st == 200, f"HTTP {st} body={raw[:100]}")

    # 10. 无 token 时鉴权端点应被拒
    st, raw = call("GET", "/home/info")
    check("GET /home/info 无 token 被拒", "usr_name" not in raw, f"HTTP {st} body={raw[:100]}")

    # 11. 并发登录。以前 main.py 里有个全局 Lock 把并发卡成 1（忙就回 503 并发锁），
    #     那是在绕开「模块级 Session 单例被所有请求共用」。
    #     改成每请求一个 Session（Depends(get_db)）之后不该再有 503。
    conc_ok, conc_bad = [], []
    def _login_once():
        _, r = call("POST", "/login", json_body={"usrname": USER, "passwd": PASSWD})
        (conc_ok if '"token"' in r else conc_bad).append(r)
    import threading
    threads = [threading.Thread(target=_login_once) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    check("并发登录 8 个全部成功（无并发锁）", len(conc_ok) == 8,
          f"成功 {len(conc_ok)} / 失败 {len(conc_bad)}: {conc_bad[:1]}")

    passed = sum(1 for _, ok in _results if ok)
    total = len(_results)
    print(f"\n=== {passed}/{total} 通过 ===")
    if passed != total:
        print("    失败的项：")
        for name, ok in _results:
            if not ok:
                print(f"      - {name}")
    print(f"\n（本次上传落地在 backend/files/{uid}/{fname}/ ，需要的话手动清）")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
