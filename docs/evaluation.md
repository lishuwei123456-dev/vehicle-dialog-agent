# 评测方案

## 指标

| 层级 | 指标 |
| --- | --- |
| 拒识 | Accuracy、Precision、Recall、F1 |
| 意图识别 | Accuracy、Top-K Accuracy、Macro-F1 |
| 槽位抽取 | Slot Precision、Slot Recall、Slot F1 |
| 端到端 | Task Success Rate、平均响应时间、P95 响应时间 |

## 当前内置评测

启动服务后访问：

```bash
curl http://127.0.0.1:8080/v1/evaluation/sample
```

该接口运行一组小样例，返回语义链路的基础准确率。正式评测时应扩展 `app/evaluation/evaluator.py`，增加更多多轮样本和边界样本。

也可以直接运行脚本：

```bash
python scripts/evaluate_sample.py
```

## 评测数据建议

- 每个意图至少 100 条样例。
- 每个槽位覆盖常见表达、口语表达和缺省表达。
- 拒识样本应包含闲聊、噪声、半截句、无意义重复和超范围问题。
- 多轮样本应包含“第一个”“换一个”“打开它”等指代表达。
