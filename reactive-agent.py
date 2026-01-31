import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import random
import asyncio


# Simulated disaster severity
def get_disaster_severity():
    return random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])


class Monitoring(State):
    async def run(self):
        severity = get_disaster_severity()
        print(f"[Monitoring] Severity detected: {severity}")

        if severity == "HIGH":
            self.set_next_state("PREPARING")
        elif severity == "CRITICAL":
            self.set_next_state("EMERGENCY")
        else:
            self.set_next_state("MONITORING")

        await asyncio.sleep(2)


class PreparingRescue(State):
    async def run(self):
        print("[Preparing Rescue] Mobilizing rescue resources...")
        await asyncio.sleep(2)
        self.set_next_state("EMERGENCY")


class EmergencyResponse(State):
    async def run(self):
        print("[Emergency Response] Executing emergency rescue operations!")
        await asyncio.sleep(2)
        self.set_next_state("MONITORING")


class RescueAgent(Agent):
    async def setup(self):
        print("RescueAgent started.")

        fsm = FSMBehaviour()

        fsm.add_state(name="MONITORING", state=Monitoring(), initial=True)
        fsm.add_state(name="PREPARING", state=PreparingRescue())
        fsm.add_state(name="EMERGENCY", state=EmergencyResponse())

        fsm.add_transition(source="MONITORING", dest="MONITORING")
        fsm.add_transition(source="MONITORING", dest="PREPARING")
        fsm.add_transition(source="MONITORING", dest="EMERGENCY")
        fsm.add_transition(source="PREPARING", dest="EMERGENCY")
        fsm.add_transition(source="EMERGENCY", dest="MONITORING")

        self.add_behaviour(fsm)


async def main():
    agent = RescueAgent("agent-test@xmpp.jp", "abigail111")
    await agent.start()
    await asyncio.sleep(20)
    await agent.stop()


if __name__ == "__main__":
    spade.run(main())
