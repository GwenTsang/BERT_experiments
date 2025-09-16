Le fichier "Bat.csv" contient des phrases dans lesquelles le mot **"bat"** doit être interprété comme "batte de baseball" ET des phrases dans lesquelles le mot "bat" doit être interprété comme "chauve-souris".
La première partie des lignes (index `df.iloc[0, 0]` à `df.iloc[64, 0]` inclus) contient des phrases où « bat » fait référence à une batte de baseball.
Les lignes restantes (index `df.iloc[65, 0]` à `df.iloc[129, 0]` inclus) contiennent des phrases où « bat » fait référence à la chauve-souris. 


Le but de ce projet est de voir les dernières couches d'attention de BERT permettent de "désambiguer" la signification du mot "bat" en fonction du contexte. En principe, dans le CSV, les phrases ne sont pas ambigues (le contexte permet à un humain de deviner si "bat" a le premier sens ou le second sens).

**Résultats** : C'est globalement *très* satisfaisant. On remarque que les outliners sont souvent des phrases longues, tandis que les phrases centroïdes sont des phrases courtes. Moralité : la désambiguation marche particulièrement bien dans les phrases courtes toutes choses égales par ailleurs.
