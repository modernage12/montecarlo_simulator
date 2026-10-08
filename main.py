import random
import statistics
import matplotlib

matplotlib.use("TkAgg")  # Necessario su PyCharm per bug IDE
import matplotlib.pyplot as plt

# Limiti a input utente
MAX_THRESHOLD = 100
MIN_THRESHOLD = 0


def simula_esito(win_rate):
    """Simula l'esito di un trade (win/loss) in base al tasso di win rate"""

    return random.random() <= (win_rate / 100)


def simula_operazione(capitale, rischio_perc, win_rate, risk_to_reward):
    """Simula un'intera operazione calcolando perdita/guadagno in base all'esito e risk to reward"""
    rischio_trade = (capitale * rischio_perc) / 100
    new_balance = capitale
    operazione_vinta = simula_esito(win_rate)

    if operazione_vinta:
        new_balance += (rischio_trade * risk_to_reward)
    else:
        new_balance -= rischio_trade

    return new_balance, operazione_vinta


def calcola_drawdown(max_balance, new_balance):
    """Calcola e restituisce il drawdown calcolato su picco del balance vs balance attuale"""

    return ((max_balance - new_balance) / max_balance) * 100


def run_simulation(capitale, rischio_perc, win_rate, risk_to_reward, n_operazioni):
    """Simula l'esito di una serie di trade e ne restituisce le statistiche"""
    win_count = 0
    max_balance = capitale
    new_balance = capitale
    max_drawdown = 0
    storico_balance = [capitale]

    for _ in range(n_operazioni):
        new_balance, trade_vinto = simula_operazione(new_balance, rischio_perc, win_rate, risk_to_reward)
        storico_balance.append(new_balance)

        if trade_vinto:
            win_count += 1
        if new_balance > max_balance:
            max_balance = new_balance
        else:
            drawdown = calcola_drawdown(max_balance, new_balance)
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    return new_balance, win_count, max_drawdown, storico_balance


def run_montecarlo(capitale, rischio_perc, win_rate, risk_to_reward, n_operazioni, n_simulazioni):
    """Avvia la simulazione Monte Carlo e ne ritorna i risultati di bilancio e drawdown di ogni singola simulazione"""
    balance_finale = []
    drawdown_finale = []
    storico_balance_finale = []
    mediana_simulazioni = []

    for _ in range(n_simulazioni):
        balance, _win_count, max_drawdown, storico_balance = run_simulation(capitale, rischio_perc, win_rate,
                                                                            risk_to_reward,
                                                                            n_operazioni)
        balance_finale.append(balance)
        drawdown_finale.append(max_drawdown)
        storico_balance_finale.append(storico_balance)

    for n in range(len(storico_balance_finale[0])):
        lista_simulazioni = []

        for m in range(len(storico_balance_finale)):
            lista_simulazioni.append(storico_balance_finale[m][n])

        mediana_simulazioni.append(statistics.median(lista_simulazioni))

    return balance_finale, drawdown_finale, storico_balance_finale, mediana_simulazioni


def calcola_statistiche(lista_balance, lista_drawdown, soglia_drawdown, capitale):
    """Calcola e ritorna i risultati della simulazione Monte Carlo"""
    total_balance = sum(lista_balance)
    total_drawdown = sum(lista_drawdown)
    min_balance = min(lista_balance)
    max_balance = max(lista_balance)
    min_drawdown = min(lista_drawdown)
    max_drawdown = max(lista_drawdown)
    media_balance = total_balance / len(lista_balance)
    media_drawdown = total_drawdown / len(lista_drawdown)
    mediana_balance = statistics.median(lista_balance)
    mediana_drawdown = statistics.median(lista_drawdown)
    gain_medio = ((media_balance - capitale) / capitale) * 100
    gain_mediano = ((mediana_balance - capitale) / capitale) * 100
    count_violazione_drawdown = 0

    for index in range(len(lista_balance)):
        if lista_drawdown[index] > soglia_drawdown:
            count_violazione_drawdown += 1

    perc_violazione_drawdown = (count_violazione_drawdown / len(lista_drawdown)) * 100

    return {
        "media_balance": media_balance,
        "media_drawdown": media_drawdown,
        "min_balance": min_balance,
        "max_balance": max_balance,
        "min_drawdown": min_drawdown,
        "max_drawdown": max_drawdown,
        "count_violazione_drawdown": count_violazione_drawdown,
        "perc_violazione_drawdown": perc_violazione_drawdown,
        "mediana_balance": mediana_balance,
        "mediana_drawdown": mediana_drawdown,
        "gain_medio": gain_medio,
        "gain_mediano": gain_mediano
    }


def genera_grafico(mediana_simulazioni, migliore_simulazione, peggior_simulazione, capitale):
    """Genera il grafico delle performance della strategia e capitale iniziale"""
    max_x = max(range(len(mediana_simulazioni)))
    plt.plot(range(len(mediana_simulazioni)), mediana_simulazioni, label="Mediana")
    plt.plot(range(len(migliore_simulazione)), migliore_simulazione, label="Migliore", color="green")
    plt.plot(range(len(peggior_simulazione)), peggior_simulazione, label="Peggiore", color="red")
    plt.hlines(capitale, 0, max_x, label="Capitale iniziale", color="black", linestyles="dashed")
    plt.title("Simulazione Monte Carlo")
    plt.xlabel("N° Trade")
    plt.ylabel("Balance ($)")
    plt.legend()
    plt.show()


def filtra_simulazioni(lista_balance, lista_storico_balance):
    """Filtra le simulazioni prendendo la migliore e la peggiore e ritorna l'intero storico di entrambe"""
    posizione_migliore_simulazione = lista_balance.index(max(lista_balance))
    posizione_peggiore_simulazione = lista_balance.index(min(lista_balance))

    lista_storico_migliore = lista_storico_balance[posizione_migliore_simulazione]
    lista_storico_peggiore = lista_storico_balance[posizione_peggiore_simulazione]

    return {
        "lista_storico_migliore": lista_storico_migliore,
        "lista_storico_peggiore": lista_storico_peggiore
    }


def chiedi_numero(frase, low, high=None, intero=False):
    """Cattura un numero dall'utente in input finchè è valido e lo restituisce"""
    numero_input = 0

    while True:
        try:
            numero_input = float(input(frase))
        except ValueError:
            print("Inserisci un valore valido.")
            continue

        if intero and not numero_input.is_integer():
            print("Il numero deve essere un intero.")
            continue

        if numero_input <= low:
            print(f"Inserisci un valore maggiore di {low}")
            continue
        elif high is not None and numero_input > high:
            print(f"Inserisci un valore massimo di {high}")
            continue

        break

    return numero_input


# if __name__ == "__main__" è per far eseguire il codice al suo interno solo quando viene lanciato e non importato
if __name__ == "__main__":
    win_rate = chiedi_numero("Win Rate: ", MIN_THRESHOLD, MAX_THRESHOLD)
    capitale = chiedi_numero("Capitale: ", MIN_THRESHOLD)
    rischio = chiedi_numero("Rischio su capitale: ", MIN_THRESHOLD, MAX_THRESHOLD)
    risk_to_reward = chiedi_numero("RR: ", MIN_THRESHOLD, MAX_THRESHOLD)
    n_operazioni = int(chiedi_numero("Numero di trade: ", MIN_THRESHOLD, intero=True))
    n_simulazioni = int(chiedi_numero("Numero di simulazioni: ", MIN_THRESHOLD, intero=True))
    soglia_drawdown = chiedi_numero("Limite drawdown: ", MIN_THRESHOLD, MAX_THRESHOLD)

    lista_balance, lista_drawdown, lista_storico_balance, mediana_simulazioni = run_montecarlo(capitale, rischio,
                                                                                               win_rate,
                                                                                               risk_to_reward,
                                                                                               n_operazioni,
                                                                                               n_simulazioni)

    statistiche = calcola_statistiche(lista_balance, lista_drawdown, soglia_drawdown, capitale)

    print(f"\nGain medio: {statistiche['gain_medio']:,.2f}%")
    print(f"Gain mediano: {statistiche['gain_mediano']:,.2f}%")
    print(f"\nBalance medio: {statistiche['media_balance']:,.2f}$")
    print(f"Mediana balance: {statistiche['mediana_balance']:,.2f}$")
    print(f"\nDrawdown medio: {statistiche['media_drawdown']:,.2f}%")
    print(f"Mediana Drawdown: {statistiche['mediana_drawdown']:,.2f}%")
    print(f"\nBalance minimo: {statistiche['min_balance']:,.2f}$")
    print(f"Balance massimo: {statistiche['max_balance']:,.2f}$")
    print(f"\nDrawdown minimo: {statistiche['min_drawdown']:,.2f}%")
    print(f"Drawdown massimo: {statistiche['max_drawdown']:,.2f}%")
    print(f"\nNumero di violazioni della soglia di drawdown: {statistiche['count_violazione_drawdown']}")
    print(f"Percentuale di simulazioni oltre la soglia: {statistiche['perc_violazione_drawdown']:,.2f}%")

    simulazioni = filtra_simulazioni(lista_balance, lista_storico_balance)
    genera_grafico(mediana_simulazioni, simulazioni["lista_storico_migliore"], simulazioni["lista_storico_peggiore"],
                   capitale)
