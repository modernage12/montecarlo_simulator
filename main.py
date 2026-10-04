import random

def simula_operazione(win_rate):
    result = random.random() <= (win_rate/100)

    return result

def run_simulation(win_rate):
    win_count = 0

    for index in range(1000):
        if simula_operazione(win_rate):
            win_count += 1

    return win_count

print(run_simulation(int(input("Inserisci win rate: "))))


