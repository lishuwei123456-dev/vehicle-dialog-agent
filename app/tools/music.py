def search_music(keyword: str) -> dict[str, str]:
    return {
        "keyword": keyword,
        "title": keyword,
        "artist": "示例歌手",
        "source": "本地模拟音乐服务",
    }
