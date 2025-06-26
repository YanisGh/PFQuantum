Jeu de pile ou face simulé avec un circuit quantique via Qiskit.

Le jeu repose sur un qubit simulé avec Qiskit. La pièce est initialement équitable (50/50), mais devient biaisée selon les performances du joueur :

Une bonne réponse augmente la probabilité que le côté deviné réapparaisse.

Une mauvaise réponse réduit ce biais.

L'objectif est d'atteindre 100 % de probabilité sur un côté.

Le joueur perd s'il revient trois fois à une pièce équitable (50/50).

Le biais est simulé à l'aide de la porte quantique RY avec un angle calculé en fonction de la probabilité.

Fonctionnalités : 
Choix du niveau de difficulté (facile, normal, difficile) influençant les gains/pertes de biais.

Affichage dynamique des probabilités.

Système de série de victoires.

Simulation basée sur AerSimulator de Qiskit.

Comportement aléatoire contrôlé via qubit (porte Hadamard pour 50/50, porte RY pour le biais).
