#!/usr/bin/env python3
"""The numbers the waiting game and the ranking game state in words (spec J5).

  python3 tools-pm/game-numbers.py          prints them, to copy into data/pm/waitgame.yaml and rankgame.yaml
  python3 tools-pm/game-numbers.py check    exits 1, naming each number, if the data says something else

The waiting game is exact: three jobs built one at a time, each costing its cost of delay every week until it's live.
The ranking game is simulated: 30 stores, every one late on 1 order in 10, ranked each week by their late rate.
Its averages come from many simulated weeks, so the check allows for the small wobble a different run gives.
"""
import itertools
import os
import sys

import numpy as np
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "pm")


def load(name):
    return yaml.safe_load(open(os.path.join(DATA, name), encoding="utf-8"))


# ---------- the waiting game ----------

def wait_total(jobs, order):
    """What the waiting costs: each job costs its weekly cost of delay for every week until it's live,
    the weeks it's being built included. Returns the total and the week each job goes live."""
    by = {j["id"]: j for j in jobs}
    week, total, live = 0, 0, {}
    for jid in order:
        week += by[jid]["weeks"]
        live[jid] = week
        total += by[jid]["cost"] * week
    return total, live


def wait_numbers(d):
    jobs = d["jobs"]
    every = []
    for order in itertools.permutations([j["id"] for j in jobs]):
        total, live = wait_total(jobs, order)
        every.append({"order": list(order), "total": total})
    every.sort(key=lambda e: e["total"])
    out = {"weeks": sum(j["weeks"] for j in jobs), "best": every[0]["total"], "worst": every[-1]["total"],
           "every": every, "rules": {}}
    for key, rule in d["rules"].items():
        out["rules"][key] = wait_total(jobs, rule["order"])[0]
    # the rule a reader can't guess: highest cost of delay per week of work first
    out["cd3"] = sorted((j for j in jobs), key=lambda j: -j["cost"] / j["weeks"])
    return out


# ---------- the ranking game ----------

def rank_sizes(d):
    return np.array(sum(([g["orders"]] * g["stores"] for g in d["sizes"]), []))


def rank_numbers(d, runs, seed=2026):
    rng = np.random.default_rng(seed)
    sizes = rank_sizes(d)
    n = len(sizes)
    small = d["sizes"][0]["stores"]
    worse = n - 1  # the last large store is the one that really is worse
    se = np.sqrt(d["late"] * (1 - d["late"]) / sizes)
    tot = dict(small_worst=0.0, small_best=0.0, stay=0.0, worse_rank=0.0, worse_in_worst=0.0, worse_alone=0.0)
    for _ in range(runs):
        tie = rng.random(n) * 1e-9  # ties break at random, as the page's own sort does
        p = np.full(n, d["late"])
        a = rng.binomial(sizes, p) / sizes
        b = rng.binomial(sizes, p) / sizes
        worst_a = set(np.argsort(-(a + tie))[:5])
        worst_b = set(np.argsort(-(b + tie))[:5])
        best_a = set(np.argsort(a + tie)[:5])
        tot["small_worst"] += sum(1 for i in worst_a if i < small)
        tot["small_best"] += sum(1 for i in best_a if i < small)
        tot["stay"] += len(worst_a & worst_b)
        p2 = p.copy()
        p2[worse] = d["worse_late"]
        c = rng.binomial(sizes, p2) / sizes
        order = list(np.argsort(-(c + tie)))
        k = order.index(worse) + 1
        tot["worse_rank"] += k
        tot["worse_in_worst"] += k <= 5
        out = np.abs(c - d["late"]) > d["funnel_z"] * se
        tot["worse_alone"] += bool(out[worse]) and int(out.sum()) == 1
    avg = {k: v / runs for k, v in tot.items()}
    return {
        "small_worst": round(avg["small_worst"], 1),
        "small_best": round(avg["small_best"], 1),
        "stay": round(avg["stay"], 1),
        "worse_rank": round(avg["worse_rank"]),
        "worse_in_worst": round(100 * avg["worse_in_worst"]),
        "worse_alone": round(100 * avg["worse_alone"]),
    }


def funnel(d):
    """The range chance allows at each size: the late rate plus or minus funnel_z standard errors, in percent."""
    out = []
    for g in d["sizes"]:
        se = (d["late"] * (1 - d["late"]) / g["orders"]) ** 0.5
        out.append([round(max(0.0, d["late"] - d["funnel_z"] * se) * 100, 1), round((d["late"] + d["funnel_z"] * se) * 100, 1)])
    return out


def main():
    check = len(sys.argv) > 1 and sys.argv[1] == "check"
    w, r = load("waitgame.yaml"), load("rankgame.yaml")
    wn = wait_numbers(w)
    bad = []
    if check:
        if w["weeks"] != wn["weeks"]:
            bad.append(f"waitgame.yaml: weeks is {w['weeks']}, and the jobs take {wn['weeks']}")
        for key, total in wn["rules"].items():
            if w["rules"][key]["total"] != total:
                bad.append(f"waitgame.yaml: {key} costs {total}, not {w['rules'][key]['total']}")
        if [e["total"] for e in w["every"]] != [e["total"] for e in wn["every"]] or [e["order"] for e in w["every"]] != [e["order"] for e in wn["every"]]:
            bad.append("waitgame.yaml: the six orders and their totals aren't what the jobs give, cheapest first")
        if w["cd3"] != [j["id"] for j in wn["cd3"]]:
            bad.append(f"waitgame.yaml: cd3 is {w['cd3']}, and cost of delay per week of work puts them {[j['id'] for j in wn['cd3']]}")
        if r["funnel"] != funnel(r):
            bad.append(f"rankgame.yaml: the funnel is {r['funnel']}, and the sizes give {funnel(r)}")
        for k in ("worst", "best"):
            if sum(row[k] for row in r["example"]) != 5:
                bad.append(f"rankgame.yaml: the recorded week's five {k} add up to {sum(row[k] for row in r['example'])}")
        rn = rank_numbers(r, 20000, seed=7)
        tol = {"small_worst": 0.15, "small_best": 0.15, "stay": 0.15, "worse_rank": 1, "worse_in_worst": 3, "worse_alone": 3}
        for k, v in rn.items():
            if abs(r["averages"][k] - v) > tol[k]:
                bad.append(f"rankgame.yaml: averages.{k} is {r['averages'][k]}, and a fresh run gives about {v}")
        for b in bad:
            print(b)
        sys.exit(1 if bad else 0)
    print("waitgame.yaml")
    print(yaml.safe_dump({"weeks": wn["weeks"], "rules": wn["rules"], "every": wn["every"], "cd3": [j["id"] for j in wn["cd3"]]}, sort_keys=False))
    print("rankgame.yaml")
    print(yaml.safe_dump({"funnel": funnel(r), "averages": rank_numbers(r, 200000)}, sort_keys=False, default_flow_style=None))


if __name__ == "__main__":
    main()
