import random


def simula_esito(win_rate):
    """Simula l'esito di un trade (win/loss) in base al tasso di win rate"""
    result = random.random() <= (win_rate / 100)

    return result


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


def run_simulation(capitale, rischio_perc, win_rate, risk_to_reward, n_operazioni):
    """Avvia la simulazione dei trade eseguendone tante quante previste dall'utente"""
    win_count = 0
    new_balance = capitale

    for _ in range(n_operazioni):
        new_balance, trade_vinto = simula_operazione(new_balance, rischio_perc, win_rate, risk_to_reward)

        if trade_vinto:
            win_count += 1

    return new_balance, win_count


def chiedi_numero(frase, min, max=None):
    """Prende in input i valori dall'utente catturando errori e ritorna quei valori"""
    numero_input = 0

    while True:
        try:
            numero_input = float(input(frase))
        except ValueError as err:
            print("Inserisci un valore valido.")
            continue
        if max is not None:
            if numero_input <= min or numero_input > max:
                print(f"Inserisci un valore tra {min + 1} e {max}")
                continue
        else:
            if numero_input <= min:
                print(f"Inserisci un valore minimo di {min + 1}")
                continue
        break

    return numero_input


# if __name__ == "__main__" è per far eseguire il codice al suo interno solo da main
if __name__ == "__main__":
    win_rate = chiedi_numero("Win Rate: ", 0, 100)
    capitale = chiedi_numero("Capitale: ", 0)
    rischio = chiedi_numero("Rischio su capitale: ", 0, 100)
    risk_to_reward = chiedi_numero("RR: ", 0, 100)
    n_operazioni = int(chiedi_numero("Numero di simulazioni: ", 0))

    new_balance, trade_vinti = run_simulation(capitale, rischio, win_rate, risk_to_reward, n_operazioni)

    # ,.2f per formattazione numeri con migliaia e decimale. .2f sta per due decimali
    print(f"Capitale finale: {new_balance:,.2f})")
    print(f"Trade vinti: {trade_vinti})")
    print(f"Total gain: {((new_balance / capitale) - 1) * 100:,.2f}%")
