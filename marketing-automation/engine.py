"""Workflow execution engine."""
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Callable
from .models import Workflow, WorkflowStatus, WorkflowExecution, WorkflowNode


class WorkflowEngine:
    """Executes marketing automation workflows."""
    
    def __init__(self):
        self._workflows: Dict[str, Workflow] = {}
        self._executions: Dict[str, WorkflowExecution] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register_handler(self, action_type: str, handler: Callable):
        self._handlers[action_type] = handler
    
    def deploy(self, workflow: Workflow):
        if not workflow.nodes:
            raise ValueError("Workflow must have at least one node")
        workflow.status = WorkflowStatus.ACTIVE
        workflow.updated_at = datetime.utcnow()
        self._workflows[workflow.id] = workflow
    
    def pause(self, workflow_id: str):
        if wf := self._workflows.get(workflow_id):
            wf.status = WorkflowStatus.PAUSED
    
    async def execute(self, workflow_id: str, customer_id: str) -> WorkflowExecution:
        workflow = self._workflows.get(workflow_id)
        if not workflow or workflow.status != WorkflowStatus.ACTIVE:
            raise ValueError("Workflow not active")
        
        execution = WorkflowExecution(
            id=f"exec_{workflow_id}_{customer_id}_{int(datetime.utcnow().timestamp())}",
            workflow_id=workflow_id,
            customer_id=customer_id,
            current_node=workflow.nodes[0].id,
            status="running",
            started_at=datetime.utcnow()
        )
        self._executions[execution.id] = execution
        
        try:
            await self._traverse(execution, workflow)
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
        except Exception as e:
            execution.status = "failed"
            execution.error = str(e)
            execution.completed_at = datetime.utcnow()
        
        return execution
    
    async def _traverse(self, execution: WorkflowExecution, workflow: Workflow):
        visited = set()
        current = execution.current_node
        while current and current not in visited:
            visited.add(current)
            node = next((n for n in workflow.nodes if n.id == current), None)
            if not node:
                break
            if handler := self._handlers.get(node.type):
                await handler(execution.customer_id, node.config)
            execution.current_node = node.next_nodes[0] if node.next_nodes else ""
