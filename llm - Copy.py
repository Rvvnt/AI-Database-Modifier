class AgentAdapter:
    # Provider-neutral model boundary. Connect the approved LLM here.
    def propose_change(self, task, context):
        return {"status":"adapter_required","explanation":"Repository context is ready for the approved LLM provider.","patch":""}
