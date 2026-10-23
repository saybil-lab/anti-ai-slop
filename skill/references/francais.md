# Tics IA en français

À charger dès que le texte est en français. Les listes anglaises ne s'appliquent
pas telles quelles : beaucoup de mots (« crucial », « robuste », « dynamique »)
existent dans les deux langues mais ne trahissent pas l'IA de la même façon.

Le dictionnaire complet (≈ 260 entrées) est dans
`scripts/anti_ai_slop/patterns_fr.json`. Scan déterministe :

```bash
slop words texte.md --lang fr
slop replace texte.md --lang fr --dry-run
```

## Mots et expressions à bannir (les plus fréquents)

| Tic | Pourquoi ça sonne IA | Remplacer par |
|---|---|---|
| il est crucial / essentiel / primordial de | emphase creuse | « il faut », ou dire pourquoi |
| il est important de noter que / il convient de noter que | annonce au lieu de dire | supprimer, dire la chose |
| dans un monde en constante évolution / à l'ère du numérique | ouverture générique | entrer direct dans le sujet |
| plongeons dans / découvrons ensemble / sans plus attendre | animation de blog | supprimer |
| tirer parti de / libérer le potentiel | calque de « leverage / unlock » | utiliser, servir à |
| un véritable levier / atout / game changer | superlatif vide | dire l'effet concret, avec un chiffre |
| joue un rôle clé / crucial / central | calque de « plays a key role » | dire ce que ça fait |
| changer la donne / repousser les limites / ouvrir la voie | cliché | dire ce qui change |
| une myriade / pléthore / multitude de | registre gonflé | beaucoup de, ou le nombre |
| holistique, synergie, paradigme, écosystème, actionnable | jargon conseil | mot simple |
| tapisserie, symphonie, odyssée, kaléidoscope, quintessence | métaphore pompeuse | supprimer |
| méticuleux, indéniablement, résolument, véritablement | adverbe/adjectif de remplissage | supprimer |
| témoigne de / s'inscrit dans / se positionne comme | « serves as / stands as » en français | « montre », « est » |
| en somme / en définitive / en conclusion | conclusion scolaire | supprimer, finir sur le fait |
| par ailleurs / de surcroît / en outre (en série) | transitions empilées | une seule, ou aucune |
| n'hésitez pas à | formule d'email IA | « écrivez-moi si… », ou rien |
| j'espère que ce message vous trouve en bonne santé | calque direct de l'anglais | supprimer |

## Structures à bannir

- **Parallélisme négatif** : « Ce n'est pas seulement X, c'est Y », « Il ne s'agit
  pas simplement de X, mais de Y », « Bien plus qu'un simple X ». Dire Y directement.
- **Règle de trois** : trois adjectifs ou trois bénéfices d'affilée
  (« simple, rapide et efficace »). En garder un, le plus vrai.
- **Question-réponse théâtrale** : « Le résultat ? Une hausse de 30 %. »,
  « Le secret ? La régularité. » Écrire la phrase normalement.
- **« Et c'est là que X entre en jeu »** : transition de pitch. Supprimer.
- **Tiret cadratin (—)** pour les incises : utiliser des virgules, des
  parenthèses ou deux phrases. Le tiret de dialogue reste autorisé.
- **Majuscules à chaque mot dans les titres** (« Comment Booster Vos Ventes ») :
  calque anglais. En français, seule la première lettre prend la majuscule.
- **Puces avec étiquette en gras** : `• **Gain de temps :** vous gagnez…`.
- **Emoji en tête de titre ou de puce** (🚀 ✅ 💡).
- **Guillemets anglais "…"** dans un texte français : utiliser « … ».
- **Ponctuation double sans espace** (« Pourquoi? ») : en français on met une
  espace (insécable) avant `; : ! ?`.
- **« Que vous soyez X ou Y »** en ouverture : formule passe-partout.
- **Anglicismes de marketing** : impacter, booster, disruptif, next level,
  délivrer de la valeur. Préférer le mot français courant.

## Ce qui reste correct

Ne pas sur-corriger. « Essentiel », « notamment », « désormais », « optimiser »,
« par ailleurs » sont du français normal : ils ne posent problème que s'ils
s'empilent ou servent de remplissage. Le scan les classe en `low` ; utiliser
`--min-severity medium` pour ne voir que les vrais tics.
