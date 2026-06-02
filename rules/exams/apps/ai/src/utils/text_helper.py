import re

def clean_text(text: str) -> str:
    """텍스트 특수문자 제거 및 공백 정규화 처리를 수행하는 순수 함수"""
    cleaned = re.sub(r"[^\w\s]", "", text)
    return cleaned.strip()
