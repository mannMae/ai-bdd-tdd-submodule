from langchain_core.prompts import PromptTemplate

# 1. System Prompt Template
SYSTEM_PROMPT = """당신은 의료 데이터 분석 AI 비서입니다. 
주어진 신호 데이터를 기반으로 상태를 감지하여 보고하십시오.
"""

# 2. User Input Template
USER_PROMPT_TEMPLATE = PromptTemplate.from_template(
    "이전 상태 기록: {history}\n현재 신호 데이터: {current_signal}\n위험 상태 여부를 판정해 주세요."
)
