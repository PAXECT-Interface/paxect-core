#!/usr/bin/env python3
"""
PAXECT Demo 07 – SelfTune Adaptive Loop
---------------------------------------
Simulates adaptive epsilon-greedy tuning with persistent state.

Each run:
 - Loads last epsilon & cycle from /tmp
 - Performs 10 cycles of exploit/explore
 - Adjusts epsilon based on performance
 - Saves new state back to disk
"""

import json, random, time, tempfile
from pathlib import Path

STATE_PATH = Path(tempfile.gettempdir()) / "paxect_demo_07_selftune_state.json"
CYCLES = 10

def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"cycle": 0, "epsilon": 0.3}

def save_state(state):
    STATE_PATH.write_text(json.dumps(state))

def run_cycle(state):
    eps = state["epsilon"]
    cycle = state["cycle"] + 1
    mode = "explore" if random.random() < eps else "exploit"
    reward = random.uniform(0.2, 1.0) if mode == "exploit" else random.uniform(0.0, 0.8)
    success = reward > 0.7
    # adjust epsilon: decay if successful exploit, increase slightly if not
    if success and mode == "exploit":
        eps = max(0.05, eps * 0.95)
    elif not success:
        eps = min(0.5, eps + 0.05)
    state.update({"cycle": cycle, "epsilon": round(eps, 3)})
    return {"cycle": cycle, "mode": mode, "reward": round(reward, 3),
            "success": success, "epsilon_next": round(eps, 3)}

def main():
    print("=== PAXECT Demo 07 – SelfTune Adaptive Loop ===")
    state = load_state()
    print(f"Loaded state: {state}")
    history = []
    for _ in range(CYCLES):
        res = run_cycle(state)
        history.append(res)
        print(f"[cycle {res['cycle']:03d}] mode={res['mode']:<7} reward={res['reward']:.3f} "
              f"success={res['success']} -> epsilon={res['epsilon_next']}")
        time.sleep(0.2)
    save_state(state)
    print(f"\nFinal state saved to {STATE_PATH}: {state}")
    return history

if __name__ == "__main__":
    main()
