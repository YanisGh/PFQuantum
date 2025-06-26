from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import random
import math

import qiskit
import qiskit_aer


#---------main method-------------------
def quantum_coin_flip(bias_angle=None):

    simulator = AerSimulator()
    qreg = QuantumRegister(1, 'q')
    creg = ClassicalRegister(1, 'c')
    
    circuit = QuantumCircuit(qreg, creg)
    
    if bias_angle is None:
        # 50/50
        circuit.h(qreg[0])
    else:
        # rotation custom pr bias la proba
        circuit.ry(bias_angle, qreg[0])
    
    circuit.measure(qreg[0], creg[0])
    
    transpiled_circuit = transpile(circuit, simulator)
    job = simulator.run(transpiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    measurement = list(counts.keys())[0]
    print(f"measurement : " + measurement)    
    return int(measurement)
 
def calculate_bias_angle(probability):
    # pr angle RY
    return 2 * math.acos(math.sqrt(probability))

def choose_bias_direction():
    # == renvoie un booléen
    return quantum_coin_flip() == 0

def choose_difficulty():
    # print(qiskit.__file__)
    # print(qiskit_aer.__file__)
    print("\n Choisissez la difficulté :")
    print("1. Facile - Victoire: +20% | Défaite: -10%")
    print("2. Normal - Victoire: +10% | Défaite: -10%")
    print("3. Difficile - Victoire: +10% | Défaite: -20%")
    
    while True:
        choice = input("Entrez votre choix (1/2/3): ").strip()
        if choice == '1':
            return 0.2, 0.1
        elif choice == '2':
            return 0.1, 0.1 
        elif choice == '3':
            return 0.1, 0.2 
        else:
            print("Veuillez choisir 1, 2 ou 3.")

def play_coin_flip_game():
    print("🪙 Pile ou Face Quantique 🪙")
    print("La pièce utilise la superposition quantique pour un vrai hasard.")
    print("VICTOIRE : Atteindre 100% de biais pour un côté")
    print("DÉFAITE : Retourner à 50/50 trois fois")
    print("-" * 70)
    
    # paramètres diff
    win_increment, loss_decrement = choose_difficulty()
    
    consecutive_wins = 0
    bias_probability = 0.5  
    bias_direction = None   # aucun bias au début
    fifty_fifty_count = 3  
    
    while True:
        if bias_direction is None:
            print(f"\n Probabilités actuelles : 50/50 (Pièce équitable)")
        else:
            heads_prob = bias_probability if bias_direction == 'pile' else (1 - bias_probability)
            tails_prob = 1 - heads_prob
            print(f"\nProbabilités actuelles : Pile {heads_prob:.0%} / Face {tails_prob:.0%}")
        
        print(f"Vies épuisées : {fifty_fifty_count}/3")
        
        # gg (100% bias)
        if bias_probability >= 1.0:
            print("VICTOIRE !")
            print(f"Vous avez atteint 100% de biais vers {bias_direction}.")
            break
        
        # rip
        if fifty_fifty_count <= 0:
            print("DÉFAITE !")
            print("Vous avez perdu le contrôle de la pièce quantique trois fois.")
            break
        
        guess = input("Devinez le résultat (p pour pile, f pour face, q pour quitter) : ").lower()
        
        if guess == 'q':
            print("Merci d'avoir joué.")
            break
        
        if guess not in ['p', 'f']:
            print("Veuillez entrer 'p' pour pile, 'f' pour face, ou 'q' pour quitter.")
            continue
        
        # decide quel type de flip quantique faire
        if bias_direction is None:
            # pièce équitable avec hadamard
            print("Lancement de la pièce quantique... ")
            result = quantum_coin_flip()
        else:
            # pièce biaisée avec rotation
            if bias_direction == 'pile':
                angle = calculate_bias_angle(bias_probability)
            else:
                angle = calculate_bias_angle(1 - bias_probability)
            
            # print(f"Direction du biais : {bias_direction} ({bias_probability:.0%})")
            # print(f"Lancement de la pièce quantique biaisée... (angle = {angle:.2f} radians)")
            result = quantum_coin_flip(angle)
        
        # convert 0/1 en pile/face
        coin_result = "pile" if result == 0 else "face"
        coin_symbol = "🟡" if result == 0 else "🔴"
        
        print(f"Résultat : {coin_symbol} {coin_result.upper()}")
        
        # check si le joueur a deviné juste
        player_guess = "pile" if guess == 'p' else "face"
        if player_guess == coin_result:
            consecutive_wins += 1
            print(f"✓ Correct. Série de victoires : {consecutive_wins}")
            
            # augmente le bias après une bonne réponse
            if bias_direction is None:
                # premier righr guess
                bias_direction = "pile" if choose_bias_direction() else "face"
                bias_probability = 0.5 + win_increment  # 50% + bonus selon diff
                print(f"🎯 Les futurs lancers favoriseront {bias_direction}.")
            else:
                bias_probability = min(1.0, bias_probability + win_increment)  
                bias_direction = "pile" if choose_bias_direction() else "face"
                prob_percent = int(bias_probability * 100)
                print(f"{bias_direction} a maintenant {prob_percent}% de probabilité.")
                
        else:
            print("Choix incorrect")
            consecutive_wins = 0
            
            # réduit le bias après mauvaise réponse
            if bias_direction is not None:
                bias_probability = max(0.5, bias_probability - loss_decrement)  
                
                if bias_probability == 0.5:
                    fifty_fifty_count -= 1
                    print(f"({fifty_fifty_count}/3)")
                    bias_direction = None
                else:
                    prob_percent = int(bias_probability * 100)
                    print(f"📉 {bias_direction} a maintenant {prob_percent}% de probabilité.")

if __name__ == "__main__":
    play_coin_flip_game()