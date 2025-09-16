En principe, le CSV "Bat-baseball.csv" contient des phrases dans lesquelles le mot "bat" doit être interprété comme "batte de baseball". En revanche le fichier "Bat-animal.csv" contient des phrases dans lesquelles le mot "bat" doit être interprété comme "chauve-souris".
Le fichier "Bat.csv" résulte de la concaténation des deux fichiers précédents.

Le but de ce projet est de voir les dernières couches d'attention de BERT permettent de "désambiguer" la signification du mot "bat" en fonction du contexte.

En principe, en l'état, les phrases dans les CSV ne sont pas ambigues (le contexte permet de deviner si "bat" a le premier sens ou le second sens).
