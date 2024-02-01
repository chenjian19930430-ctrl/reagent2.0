"""Marketing automation API."""
from fastapi import APIRouter
from .models import Workflow, WorkflowExecution
from .engine import WorkflowEngine
from .campaigns import CampaignManager

router = APIRouter(prefix="/api/v1/automation", tags=["automation"])
engine = WorkflowEngine()
campaigns = CampaignManager()


@router.post("/workflows", response_model=Workflow)
async def create_workflow(workflow: Workflow):
    engine.deploy(workflow)
    return workflow


@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow(workflow_id: str, customer_id: str):
    return await engine.execute(workflow_id, customer_id)


@router.post("/campaigns", response_model=dict)
async def create_campaign(name: str, description: str = ""):
    return campaigns.create_campaign(name, description)
