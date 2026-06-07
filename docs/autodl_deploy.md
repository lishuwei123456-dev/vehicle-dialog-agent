# AutoDL 部署文档

## 服务器推荐

本项目的训练任务是 BERT/RoBERTa 文本分类微调，不需要 A100 级别机器。推荐优先选择：

| 配置项 | 推荐 |
| --- | --- |
| GPU | RTX 4090 / RTX 4090D，24GB 显存 |
| CPU | 8 vCPU 或以上 |
| 内存 | 32GB 起，推荐 64GB |
| 系统盘/数据盘 | 80GB 起 |
| 镜像 | PyTorch 2.x + Python 3.10 + CUDA 11.8 |

选择理由：

- 24GB 显存足够完成中文 RoBERTa/BERT 分类微调。
- 价格通常低于 A100，更适合课程设计和毕业设计阶段。
- 前端和 FastAPI 推理服务对 GPU 要求低，训练完成后可切换无卡/低配环境演示。

## 端口规划

| 服务 | 端口 |
| --- | --- |
| FastAPI + 前端 | 8080 |
| Redis | 6379 |

## 环境准备

```bash
git clone https://github.com/lishuwei123456-dev/vehicle-dialog-agent.git
cd vehicle-dialog-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

启动演示服务：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

也可以使用脚本：

```bash
bash scripts/run_autodl.sh
```

训练环境：

```bash
pip install -r requirements-train.txt
python training/scripts/train_transformer_classifier.py \
  --data training/data/intent_sample.jsonl \
  --model hfl/chinese-roberta-wwm-ext \
  --output outputs/intent-roberta
```

## Redis 多轮状态

默认使用内存状态，适合本地调试。部署时可启用 Redis：

```bash
export STATE_BACKEND=redis
export REDIS_URL=redis://127.0.0.1:6379/0
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

如果使用 Docker Compose，本项目会自动启动 Redis：

```bash
docker compose up --build
```

## 可选真实天气

默认天气工具使用本地模拟数据，便于离线演示。如果实例可以访问公网，可切换到 Open-Meteo：

```bash
export WEATHER_PROVIDER=open-meteo
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## AutoDL 使用建议

- 训练时开启 GPU 实例。
- 写文档、调前端、跑接口时使用无卡模式或低配 CPU 环境。
- 模型输出目录 `outputs/` 不建议提交到 Git。
- 如果需要公开模型，建议上传到模型托管平台，并在 README 中提供下载脚本。

## 参考

- AutoDL 官方快速开始文档：https://www.autodl.com/docs/quick_start/
- AutoDL 官方帮助文档：https://www.autodl.com/docs/
