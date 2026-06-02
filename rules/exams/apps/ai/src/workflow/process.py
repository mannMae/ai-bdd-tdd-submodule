from typing import TypedDict, Annotated
import operator
from src.outbound.gateway import ModelGateway

class WorkflowState(TypedDict):
    input_text: str
    intermediate_steps: Annotated[list, operator.add]
    final_output: str
    status: str

# 1. 상태(Context) 제어 및 다단계 LLM 루프/의사결정만 처리
class AgentWorkflow:
    def __init__(self, model_gateway: ModelGateway):
        self.model_gateway = model_gateway

    async def run(self, text: str) -> dict:
        # 상태 초기화
        state: WorkflowState = {
            "input_text": text,
            "intermediate_steps": [],
            "final_output": "",
            "status": "pending"
        }
        
        # 1단계: 외부 LLM 프롬프트 호출
        llm_response = await self.model_gateway.call_llm(state["input_text"])
        state["intermediate_steps"].append("llm_first_call")
        
        # 2단계: 결과 컨텍스트 가공 후 상태 확정
        state["final_output"] = f"Processed: {llm_response}"
        state["status"] = "completed"
        return state
