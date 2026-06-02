from dataclasses import dataclass

# 1. dataclass frozen=True 속성으로 값의 불변성 강제
@dataclass(frozen=True)
class PostVO:
    title: str
    content: str

    # 2. 객체 초기화 시 비즈니스 무결성 및 제약 조건 검증
    def __post_init__(self):
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("제목은 비어 있을 수 없습니다.")
        if len(self.title) > 100:
            raise ValueError("제목은 100자를 초과할 수 없습니다.")
