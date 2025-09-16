Le fichier ["Bat-both.csv"](https://github.com/GwenTsang/BERT_experiments/blob/main/Materials%20and%20data%20cleaning/bat-both.csv) contient des phrases dans lesquelles le mot **"bat"** doit être interprété comme "batte de baseball" ET des phrases dans lesquelles le mot "bat" doit être interprété comme "chauve-souris".
La première partie des lignes (index `df.iloc[0, 0]` à `df.iloc[64, 0]` inclus) contient des phrases où « bat » fait référence à une batte de baseball.
Les lignes restantes (index `df.iloc[65, 0]` à `df.iloc[129, 0]` inclus) contiennent des phrases où « bat » fait référence à la chauve-souris. 


Le but de ce projet est de voir les dernières couches d'attention de BERT permettent de "désambiguer" la signification du mot "bat" en fonction du contexte (les autres mots de la phrase). Les phrases dans le CSV ne sont pas ambigues : le contexte permet à un humain de deviner si "bat" a le premier sens ou le second sens.

**Résultats** : C'est globalement *très* satisfaisant. On remarque que les outliners sont souvent des phrases longues, tandis que les phrases centroïdes sont des phrases courtes. Hypothèse : plus la phrase est longue, plus le vecteur associé au mot X a de chances d’être un peu moins discriminant, ce qui produit une moins bonne désambiguation. En réalité, nous avons essayé de tester cette hypothèse en raccourcissant certaines phrases qui posaient problèmes mais *a priori* cela n'a pas eu d'impact. 
