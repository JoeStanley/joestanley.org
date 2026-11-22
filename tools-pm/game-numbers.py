#!/usr/bin/env python3
"""The numbers the waiting game and the ranking game state in words (spec J5).

  python3 tools-pm/game-numbers.py          prints them, to copy into data/pm/waitgame.yaml and rankgame.yaml
  python3 tools-pm/game-numbers.py check    exits 1, naming each number, if the data says something else

The waiting game is exact: three jobs built one at a time, each costing what it's really worth every week until it's
live. Each job's worth is one of a few values, each as likely, so every plan's cost is worked out in every outcome.
The ranking game is simulated: 30 stores, every one late on 1 order in 10, ranked each week by their late rate. Its
trial, five small stores with a fix against the small stores without it, is worked out exactly.
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

def wait_values(job):
    """What a job may really be worth each week, each as likely: its values, or its outcomes' values."""
    return job["values"] if "values" in job else [o["value"] for o in job["outcomes"]]


def wait_total(jobs, order, worth, start=0):
    """What the waiting costs: each job costs what it's worth each week for every week until it's live, the weeks
    it's being built and any weeks the team stops first included."""
    by = {j["id"]: j for j in jobs}
    week, total = start, 0
    for jid in order:
        week += by[jid]["weeks"]
        total += worth[jid] * week
    return total


def wait_best(jobs, worth, first=(), start=0):
    """The cheapest order by what's known, keeping the jobs already picked first."""
    rest = [j["id"] for j in jobs if j["id"] not in first]
    return min((list(first) + list(o) for o in itertools.permutations(rest)), key=lambda o: wait_total(jobs, o, worth, start))


def wait_numbers(d):
    jobs = d["jobs"]
    ids = [j["id"] for j in jobs]
    est = {j["id"]: sum(wait_values(j)) / len(wait_values(j)) for j in jobs}
    bet = next(j for j in jobs if "outcomes" in j)
    T = d["test_weeks"]
    cd3 = wait_best(jobs, est)
    out = {"weeks": sum(j["weeks"] for j in jobs), "estimate": est, "cd3": cd3,
           "biggest": sorted(ids, key=lambda i: -est[i]), "rules": {}, "best": {}}
    out["board"] = out["weeks"] + T
    # A test could move the order only if some answer inside its range gives a different one.
    out["moves"] = [j["id"] for j in jobs if any(wait_best(jobs, dict(est, **{j["id"]: v})) != cd3 for v in wait_values(j))]
    worlds = []
    for combo in itertools.product(*[[(j["id"], v) for v in wait_values(j)] for j in jobs]):
        worlds.append(dict(combo))
    outcome = {o["value"]: o["id"] for o in bet["outcomes"]}

    def plan(key, w):
        if key == "est":
            return wait_total(jobs, cd3, w)
        if key == "biggest":
            return wait_total(jobs, out["biggest"], w)
        if key == "stop":  # the team waits for every answer, then builds the cheapest order
            return wait_total(jobs, wait_best(jobs, w, start=T), w, T)
        if key == "test":  # the surest top job first, the bet tested meanwhile, the next pick made on its answer
            known = dict(est, **{bet["id"]: w[bet["id"]]})
            return wait_total(jobs, wait_best(jobs, known, first=cd3[:1]), w)
        if key == "best":
            return wait_total(jobs, wait_best(jobs, w), w)

    for key in list(d["rules"]) + ["best"]:
        by = {}
        for w in worlds:
            by.setdefault(outcome[w[bet["id"]]], []).append(plan(key, w))
        row = {k: sum(v) / len(v) for k, v in by.items()}
        row["average"] = sum(sum(v) for v in by.values()) / len(worlds)
        (out["best"] if key == "best" else out["rules"].setdefault(key, {})).update({k: round(v) for k, v in row.items()})
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
    tot = dict(small_worst=0.0, small_best=0.0, stay=0.0, worse_rank=0.0, worse_in_worst=0.0, worse_alone=0.0, trial_in_worst=0.0)
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
        p3 = p.copy()
        p3[:d["trial"]["stores"]] = d["trial"]["late"]
        t = rng.binomial(sizes, p3) / sizes
        tot["trial_in_worst"] += sum(1 for i in np.argsort(-(t + tie))[:5] if i < d["trial"]["stores"])
    avg = {k: v / runs for k, v in tot.items()}
    return {
        "small_worst": round(avg["small_worst"], 1),
        "small_best": round(avg["small_best"], 1),
        "stay": round(avg["stay"], 1),
        "worse_rank": round(avg["worse_rank"]),
        "worse_in_worst": round(100 * avg["worse_in_worst"]),
        "worse_alone": round(100 * avg["worse_alone"]),
        "trial_in_worst": round(avg["trial_in_worst"], 1),
    }


def binom(n, p):
    """The chance of each count of late orders, 0 to n."""
    from math import exp, lgamma, log
    return [exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * log(p) + (n - k) * log(1 - p)) for k in range(n + 1)]


def trial_odds(d, weeks):
    """Exactly, in 100 trials: how often the stores with the fix, all their orders together, look better than the
    small stores without it, and how often worse, after this many weeks."""
    small = d["sizes"][0]
    n_fix, n_rest = d["trial"]["stores"] * small["orders"] * weeks, (small["stores"] - d["trial"]["stores"]) * small["orders"] * weeks
    a, b = binom(n_fix, d["trial"]["late"]), binom(n_rest, d["late"])
    better = worse = 0.0
    for x, pa in enumerate(a):
        for y, pb in enumerate(b):
            if x * n_rest < y * n_fix:
                better += pa * pb
            elif x * n_rest > y * n_fix:
                worse += pa * pb
    return round(100 * better), round(100 * worse)


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
        for k in ("weeks", "board", "cd3", "moves"):
            if w[k] != wn[k]:
                bad.append(f"waitgame.yaml: {k} is {w[k]}, and the jobs give {wn[k]}")
        for j in w["jobs"]:
            if j["estimate"] != wn["estimate"][j["id"]]:
                bad.append(f"waitgame.yaml: {j['id']}'s estimate is {j['estimate']}, and its range averages {wn['estimate'][j['id']]:g}")
        if w["rules"]["est"]["order"] != wn["cd3"] or w["rules"]["biggest"]["order"] != wn["biggest"] or w["rules"]["test"]["order"] != wn["cd3"][:1]:
            bad.append("waitgame.yaml: a plan's order isn't the one its rule gives")
        for key, row in wn["rules"].items():
            for k, v in row.items():
                if w["rules"][key][k] != v:
                    bad.append(f"waitgame.yaml: {key} costs {v} {'on average' if k == 'average' else 'if swap approvals ' + ('flops' if k == 'flop' else k)}, not {w['rules'][key][k]}")
        if w["best"] != wn["best"]:
            bad.append(f"waitgame.yaml: knowing every number costs {wn['best']}, not {w['best']}")
        if r["funnel"] != funnel(r):
            bad.append(f"rankgame.yaml: the funnel is {r['funnel']}, and the sizes give {funnel(r)}")
        for k in ("worst", "best"):
            if sum(row[k] for row in r["example"]) != 5:
                bad.append(f"rankgame.yaml: the recorded week's five {k} add up to {sum(row[k] for row in r['example'])}")
        rn = rank_numbers(r, 20000, seed=7)
        tol = {"small_worst": 0.15, "small_best": 0.15, "stay": 0.15, "worse_rank": 1, "worse_in_worst": 3, "worse_alone": 3, "trial_in_worst": 0.15}
        for k, v in rn.items():
            if abs(r["averages"][k] - v) > tol[k]:
                bad.append(f"rankgame.yaml: averages.{k} is {r['averages'][k]}, and a fresh run gives about {v}")
        for weeks, key in ((1, "one"), (8, "eight")):
            better, worse = trial_odds(r, weeks)
            if r["averages"].get(f"trial_better_{key}") != better or r["averages"].get(f"trial_worse_{key}") != worse:
                bad.append(f"rankgame.yaml: after {key} week{'s' if weeks > 1 else ''} the fix looks better {better} and worse {worse} times in 100, not {r['averages'].get(f'trial_better_{key}')} and {r['averages'].get(f'trial_worse_{key}')}")
        for b in bad:
            print(b)
        sys.exit(1 if bad else 0)
    print("waitgame.yaml")
    print(yaml.safe_dump({k: wn[k] for k in ("weeks", "board", "estimate", "cd3", "moves", "rules", "best")}, sort_keys=False, default_flow_style=None))
    print("rankgame.yaml")
    av = rank_numbers(r, 200000)
    for weeks, key in ((1, "one"), (8, "eight")):
        av[f"trial_better_{key}"], av[f"trial_worse_{key}"] = trial_odds(r, weeks)
    print(yaml.safe_dump({"funnel": funnel(r), "averages": av}, sort_keys=False, default_flow_style=None))


if __name__ == "__main__":
    main()
