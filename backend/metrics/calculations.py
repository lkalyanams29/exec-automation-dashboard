from __future__ import annotations
from collections import Counter
from typing import Iterable

def pass_rate(passed:int, failed:int)->float:
    """Passed / (Passed + Failed); skipped/error are excluded."""
    return round(passed/(passed+failed)*100,2) if passed+failed else 0.0
def failure_rate(passed:int, failed:int)->float: return round(100-pass_rate(passed,failed),2) if passed+failed else 0.0
def growth_percent(new_tests:int, start_of_period_total:int)->float: return round(new_tests/start_of_period_total*100,2) if start_of_period_total else 0.0
def change_percent(current:float, previous:float)->float: return round((current-previous)/previous*100,2) if previous else 0.0
def flaky_score(statuses:Iterable[str], minimum:int=5)->float:
    values=[s.upper() for s in statuses]; counts=Counter(values); total=counts["PASSED"]+counts["FAILED"]
    if total<minimum or not counts["PASSED"] or not counts["FAILED"]: return 0.0
    return round(counts["FAILED"]/total*100,2)
def health_status(value:float, green:float=95, yellow:float=90)->str:
    return "GREEN" if value>=green else "YELLOW" if value>=yellow else "RED"
