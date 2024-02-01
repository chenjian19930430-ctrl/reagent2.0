"""Campaign management."""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .models import Workflow, WorkflowNode, TriggerType, ActionType


class CampaignManager:
    """Manages marketing campaigns."""
    
    def __init__(self):
        self._campaigns: Dict[str, dict] = {}
    
    def create_campaign(self, name: str, description: str = "") -> dict:
        campaign = {
            "id": f"camp_{int(datetime.utcnow().timestamp())}",
            "name": name,
            "description": description,
            "status": "draft",
            "created_at": datetime.utcnow(),
            "workflow_id": None,
        }
        self._campaigns[campaign["id"]] = campaign
        return campaign
    
    def build_welcome_workflow(self, campaign_id: str) -> Workflow:
        today = datetime.utcnow()
        return Workflow(
            id=f"wf_{campaign_id}",
            name="Welcome Series",
            description="New customer welcome email sequence",
            trigger=TriggerType.EVENT,
            trigger_config={"event": "customer.signup"},
            nodes=[
                WorkflowNode(id="n1", type="send_email", config={"template": "welcome_1"}, next_nodes=["n2"]),
                WorkflowNode(id="n2", type="delay", config={"duration_hours": 24}, next_nodes=["n3"]),
                WorkflowNode(id="n3", type="send_email", config={"template": "welcome_2"}, next_nodes=["n4"]),
                WorkflowNode(id="n4", type="delay", config={"duration_hours": 72}, next_nodes=["n5"]),
                WorkflowNode(id="n5", type="update_segment", config={"segment": "engaged"}, next_nodes=[]),
            ],
            created_at=today,
            updated_at=today,
        )
    
    def build_abandoned_cart_workflow(self, campaign_id: str) -> Workflow:
        today = datetime.utcnow()
        return Workflow(
            id=f"wf_{campaign_id}_cart",
            name="Abandoned Cart Recovery",
            description="Recover abandoned shopping carts",
            trigger=TriggerType.EVENT,
            trigger_config={"event": "cart.abandoned"},
            nodes=[
                WorkflowNode(id="n1", type="delay", config={"duration_minutes": 30}, next_nodes=["n2"]),
                WorkflowNode(id="n2", type="send_email", config={"template": "cart_reminder_1"}, next_nodes=["n3"]),
                WorkflowNode(id="n3", type="delay", config={"duration_hours": 24}, next_nodes=["n4"]),
                WorkflowNode(id="n4", type="send_sms", config={"template": "cart_reminder_2"}, next_nodes=[]),
            ],
            created_at=today,
            updated_at=today,
        )
