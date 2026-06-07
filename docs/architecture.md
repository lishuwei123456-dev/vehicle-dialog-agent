# 系统架构

本系统面向智能座舱任务型对话场景，将自然语言指令转换成可执行的结构化动作。

## 核心链路

1. 入口层接收用户指令。
2. 拒识模块判断输入是否有效。
3. 意图识别模块输出任务类型。
4. 槽位抽取模块生成结构化参数。
5. Function Calling Planner 生成函数调用计划。
6. MCP 风格工具注册中心执行工具。
7. 车机模拟器更新状态。
8. 前端展示模块链路、JSON 和车机状态。

## 模块说明

| 模块 | 位置 | 说明 |
| --- | --- | --- |
| Gateway | `app/api/` | HTTP 接口和静态前端托管 |
| Reject | `app/nlu/reject_classifier.py` | 拒识二分类 baseline |
| Intent | `app/nlu/intent_classifier.py` | 意图识别 baseline，可替换为 BERT/RoBERTa |
| Slot | `app/nlu/slot_extractor.py` | 槽位抽取和标准化 |
| Function Calling | `app/llm/function_calling.py` | 函数 schema 和调用计划 |
| MCP Registry | `app/mcp/registry.py` | 工具统一注册和调用 |
| Tools | `app/tools/` | 地图、音乐、天气工具 |
| State | `app/dialogue/state_store.py` | 内存/Redis 多轮状态 |
| Cockpit | `app/cockpit/` | 车机端状态模拟 |

## 可替换设计

在线演示默认使用可解释 baseline，保证无需 GPU 也能运行。训练环境可用 `training/scripts/train_transformer_classifier.py` 微调 BERT/RoBERTa，然后将 `IntentClassifier` 替换为模型推理服务。
