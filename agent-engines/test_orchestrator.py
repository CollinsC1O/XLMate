import unittest
import asyncio
from main import AgentOrchestrator, EngineType, DeploymentState

class TestAgentOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AgentOrchestrator()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_register_engine(self):
        engine_id = "test-engine"
        result = self.loop.run_until_complete(
            self.orchestrator.register_engine(engine_id, EngineType.CUSTOM)
        )
        self.assertTrue(result)
        self.assertIn(engine_id, self.orchestrator.engines)
        self.assertEqual(self.orchestrator.engines[engine_id]["type"], "custom")

    def test_deploy_engine_success(self):
        engine_id = "test-deploy"
        self.loop.run_until_complete(
            self.orchestrator.register_engine(engine_id, EngineType.LEELA)
        )
        result = self.loop.run_until_complete(
            self.orchestrator.deploy_engine(engine_id)
        )
        self.assertTrue(result)
        status = self.orchestrator.get_engine_status(engine_id)
        self.assertEqual(status["pipeline"]["state"], DeploymentState.ACTIVE.value)
        self.assertEqual(status["engine"]["status"], "deployed")

    def test_deploy_engine_not_found(self):
        engine_id = "non-existent"
        result = self.loop.run_until_complete(
            self.orchestrator.deploy_engine(engine_id)
        )
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
