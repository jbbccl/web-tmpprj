# tmpprj

FastAPI 后端 + Vue/Vite 前端 + MariaDB。大文件分片上传练手项目。

## 用 Podman + compose 

```bash
podman-compose up -d
podman-compose logs -f backend
podman-compose down
podman-compose down -v 
```

```sh
uv venv --python 3.11 .venv
uv pip install -r backend/requirements.txt

```

VSCodium 里 basedpyright 的解释器配置在 `.vscode/settings.json`（指向 `.venv`），
F5 的调试配置在 `.vscode/launch.json`。
