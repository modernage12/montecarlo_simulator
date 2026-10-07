from main import calcola_drawdown, run_simulation, calcola_statistiche
import pytest


def test_drawdown():
    assert calcola_drawdown(1000, 900) == 10
    assert calcola_drawdown(1000, 1000) == 0


def test_simulation():
    approx_balance_first = pytest.approx(1218.99, abs=0.01)
    approx_balance_second = pytest.approx(904.38, abs=0.01)
    approx_drawdown = pytest.approx(9.56, abs=0.01)

    balance, win_count, drawdown, storico = run_simulation(1000, 1, 100, 2, 10)

    assert balance == approx_balance_first
    assert win_count == 10
    assert drawdown == 0
    assert len(storico) == 11  # 11 perchè partiamo da [0] che contiene il capitale iniziale


def test_statistiche():
    lista_balance = [1200, 850, 1500]
    lista_drawdown = [8, 22, 5]
    capitale = 1000
    soglia = 20

    risultati = calcola_statistiche(lista_balance, lista_drawdown, soglia, capitale)

    assert risultati['media_balance'] == pytest.approx(1183.33, abs=0.01)
    assert risultati['media_drawdown'] == pytest.approx(11.67, abs=0.01)
    assert risultati['mediana_balance'] == pytest.approx(1200, abs=0.01)
    assert risultati['mediana_drawdown'] == pytest.approx(8, abs=0.01)
    assert risultati['max_balance'] == pytest.approx(1500, abs=0.01)
    assert risultati['min_balance'] == pytest.approx(850, abs=0.01)
    assert risultati['min_drawdown'] == pytest.approx(5, abs=0.01)
    assert risultati['max_drawdown'] == pytest.approx(22, abs=0.01)
    assert risultati['count_violazione_drawdown'] == pytest.approx(1)
    assert risultati['perc_violazione_drawdown'] == pytest.approx(33.33, abs=0.01)
    assert risultati['gain_medio'] == pytest.approx(18.33, abs=0.01)
    assert risultati['gain_mediano'] == pytest.approx(20, abs=0.01)
