from backend.metrics.calculations import pass_rate, failure_rate, growth_percent, flaky_score, health_status
def test_rates(): assert pass_rate(95,5)==95 and failure_rate(95,5)==5
def test_rates_empty(): assert pass_rate(0,0)==0
def test_growth(): assert growth_percent(42,1242)==3.38
def test_flaky(): assert flaky_score(["PASSED"]*7+["FAILED"]*3)==30
def test_stable_not_flaky(): assert flaky_score(["PASSED"]*10)==0
def test_health(): assert [health_status(x) for x in (96,92,89)]==["GREEN","YELLOW","RED"]
