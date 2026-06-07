import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.evaluation.evaluator import EvalCase, evaluate_cases


CASES = [
    EvalCase("导航去北京南站", "NAVIGATE"),
    EvalCase("带我去上海虹桥站", "NAVIGATE"),
    EvalCase("播放周杰伦的歌", "PLAY_MUSIC"),
    EvalCase("查询北京天气", "WEATHER_QUERY"),
    EvalCase("深圳今天会不会下雨", "WEATHER_QUERY"),
    EvalCase("打开空调", "VEHICLE_CONTROL"),
    EvalCase("关闭车窗", "VEHICLE_CONTROL"),
]


if __name__ == "__main__":
    print(evaluate_cases(CASES))
