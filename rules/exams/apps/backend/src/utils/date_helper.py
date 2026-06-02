from datetime import datetime, timezone

def get_utc_now() -> datetime:
    """시스템 표준 UTC 시간을 반환하는 순수 헬퍼 함수"""
    return datetime.now(timezone.utc)
