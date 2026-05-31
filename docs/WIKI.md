# HardSurface Pro - Documentation Complète

## Table des matières
1. [Installation](#installation)
2. [Interface générale](#interface-générale)
3. [Random Panels](#random-panels)
4. [Random Extrude](#random-extrude)
5. [Random Scatter](#random-scatter)
6. [Random Tubes](#random-tubes)
7. [Loop Extrude (Greeble Stacks)](#loop-extrude)
8. [Panel Screws](#panel-screws)
9. [Axis Extrude](#axis-extrude)
10. [Random Cells](#random-cells)
11. [Random Cables](#random-cables)
12. [Flanges / Couplings](#flanges--couplings)
13. [Presets](#presets)
14. [Utilitaires](#utilitaires)
15. [Conseils et bonnes pratiques](#conseils)

---

## <a name="installation"></a>1. Installation

1. **Télécharger** le fichier `hardsurface_addon_v1.0.0.zip`
2. Dans Blender : `Edit > Preferences > Add-ons > Install...`
3. Sélectionner le fichier zip
4. Cocher la case pour activer l'addon
5. Le panneau apparaît dans le N-Panel (touche `N`) sous l'onglet **HardSurface**

---

## <a name="interface-générale"></a>2. Interface Générale

Le panneau est organisé en sections pliables :

- **Procedural Face Generation** - Outils principaux
- **Presets** - Sauvegarde/chargement de configurations
- **Utilities** - Actions globales (Reset, Randomize Seed, Rebuild)

**Boutons communs à tous les outils :**
- **Seed** - Valeur de randomisation (0 = aléatoire)
- **Randomize** - Génère une nouvelle seed aléatoire
- **Execute** - Lance l'opération

---

## <a name="random-panels"></a>3. Random Panels

**Usage :** Crée des panneaux aléatoires sur les faces sélectionnées d'un mesh.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces où créer des panneaux
3. Régler les paramètres
4. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Probability** | Probabilité qu'une face soit subdivisée | 0.0-1.0 |
| **Inset Min/Max** | Taille minimale/maximale de l'inset | 0.0-1.0 |
| **Depth Min/Max** | Profondeur minimale/maximale d'extrusion | -1.0-1.0 |
| **Safety Margin** | Marge de sécurité pour éviter les overlaps | 0.0-0.1 |
| **Use Materials** | Applique des matériaux aux vallées | Booléen |
| **Bevel Amount** | Chanfrein des arêtes | 0.0-1.0 |

### Conseils
- Commencer avec **Probability = 0.3-0.5** (0.85 = TROP de subdivisions !)
- **Safety Margin = 0.01** est un bon départ (0.50 = insets minuscules)
- Pour un look industriel : **Depth Min = -0.05**, **Depth Max = 0.02**
- **Inset Max = 0.1** pour des panneaux visibles

### ⚠️ Attention
- Probability > 0.7 crée beaucoup de faces (lent)
- Safety Margin > 0.1 réduit l'inset à presque 0
- Inset Max > 0.5 peut créer des overlaps

---

## <a name="random-extrude"></a>4. Random Extrude

**Usage :** Extrusions aléatoires avec variation de hauteur et de taper.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces à extruder
3. Régler les paramètres
4. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Extrude Rate** | Taux d'extrusion (faces sélectionnées) | 0.0-1.0 |
| **Height Min/Max** | Hauteur minimale/maximale | 0.0-10.0 |
| **Taper Min/Max** | Conicité de l'extrusion | 0.0-1.0 |
| **Max Faces** | Nombre max de faces affectées | 1-1000 |

### Conseils
- **Extrude Rate = 0.5** = 50% des faces sélectionnées seront extrudées
- **Height Max = 0.5** pour un cube standard (pas 10 !)
- **Taper Max = 0.3** pour un look subtil (1.0 = extrusion invisible !)

### ⚠️ Attention
- **Taper = 1.0** fait converger l'extrusion vers un point (disparaît)
- **Height > 2** sur un cube standard déforme tout
- Seules les faces sélectionnées ET choisies aléatoirement sont extrudées

---

## <a name="random-scatter"></a>5. Random Scatter

**Usage :** Disperser des objets ou des collections sur les faces d'un mesh.

### Workflow
1. Créer une collection avec les objets à disperser
2. Sélectionner l'objet cible en **Edit Mode**
3. Choisir la collection dans les paramètres
4. Régler la densité et les rotations
5. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Collection** | Collection à disperser | Nom |
| **Density** | Nombre d'objets par unité | 0.0-100.0 |
| **Rotation Min/Max** | Rotation aléatoire | 0-360° |
| **Scale Min/Max** | Échelle aléatoire | 0.0-10.0 |
| **Align to Normal** | Aligner avec la normale de la face | Booléen |
| **Surface Offset** | Distance depuis la surface | -10.0-10.0 |

### Conseils
- Utiliser des objets légers (low-poly) pour de grandes surfaces
- **Align to Normal = True** pour un placement réaliste

---

## <a name="random-tubes"></a>6. Random Tubes

**Usage :** Crée des tubes/pipes le long des edges sélectionnés.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les edges (pas les faces !)
3. Régler le rayon et les segments
4. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Radius** | Rayon des tubes | 0.001-1.0 |
| **Radius Variation** | Variation aléatoire du rayon | 0.0-1.0 |
| **Segments** | Segments de la section circulaire | 4-64 |
| **Smooth** | Lissage des tubes | Booléen |

### Conseils
- **Segments = 16** pour un bon compromis qualité/performance
- **Radius Variation = 0.3** pour des tubes organiques
- Les tubes sont créés comme des objets séparés (Curve → Mesh)

---

## <a name="loop-extrude"></a>7. Loop Extrude (Greeble Stacks)

**Usage :** Crée des empilements récursifs de panneaux (greebles) avec insets et extrusions successives.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces
3. Régler les itérations et la probabilité
4. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Iterations** | Nombre de niveaux récursifs | 1-10 |
| **Probability** | Probabilité d'inset par niveau | 0.0-1.0 |
| **Height Min/Max** | Hauteur d'extrusion | 0.0-1.0 |
| **Height Decay** | Réduction de hauteur par itération | 0.0-1.0 |
| **Inset Min/Max** | Taille d'inset | 0.0-1.0 |
| **Taper** | Conicité | 0.0-1.0 |

### Conseils
- **Iterations = 3** pour un look complexe
- **Height Decay = 0.7** pour des empilements naturels
- Commencer avec **Probability = 0.7**

---

## <a name="panel-screws"></a>8. Panel Screws

**Usage :** Place des vis/boulons aux coins des faces sélectionnées.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces
3. Choisir le type de vis
4. Régler la taille et la probabilité
5. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Screw Size** | Taille des vis | 0.001-0.1 |
| **Screw Depth** | Profondeur d'insertion | 0.001-0.1 |
| **Probability** | Probabilité par coin | 0.0-1.0 |
| **Screw Type** | Type de vis (0=standard, 1=hex, 2=allen) | 0-2 |

---

## <a name="axis-extrude"></a>9. Axis Extrude

**Usage :** Extrusions branchées aléatoires sur les axes X, Y, Z.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces
3. Régler les probabilités par axe
4. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Iterations** | Niveaux de récursion | 1-10 |
| **Prob. X/Y/Z** | Probabilité d'extrusion par axe | 0.0-1.0 |
| **Length Min/Max** | Longueur d'extrusion | 0.0-10.0 |
| **Scale Decay** | Réduction d'échelle | 0.0-1.0 |
| **Use Copy** | Crée un nouvel objet | Booléen |

---

## <a name="random-cells"></a>10. Random Cells

**Usage :** Place des cellules (plans, antennes, boîtes) sur les faces sélectionnées.

### Workflow
1. Sélectionner un objet en **Edit Mode**
2. Sélectionner les faces
3. Choisir le type de cellule
4. Régler la densité et la taille
5. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Cell Type** | Plane / Antenna / Box | Enum |
| **Density** | Densité de placement | 0.0-1.0 |
| **Size Min/Max** | Taille des cellules | 0.0-1.0 |
| **Height Min/Max** | Hauteur (pour antennes/boxes) | 0.0-10.0 |
| **Align to Normal** | Aligner avec la normale | Booléen |

### Types de cellules
- **Plane** : Plan plat d'émission
- **Antenna** : Tige fine extrudée
- **Box** : Petite boîte 3D

---

## <a name="random-cables"></a>11. Random Cables

**Usage :** Crée des câbles (caténaires, courbes de Bézier, droites) entre des points.

### Workflow
1. Sélectionner des edges ou des vertices en **Edit Mode**
2. Ou utiliser le mode automatique
3. Choisir le type de câble
4. Régler le rayon et la résolution
5. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Cable Type** | Catenary / Bezier / Straight | Enum |
| **Count** | Nombre de câbles | 1-100 |
| **Radius** | Rayon du câble | 0.001-0.1 |
| **Slack** | Mou (pour caténaire) | 0.0-1.0 |
| **Resolution** | Points de contrôle | 4-64 |
| **Length Min/Max** | Longueur minimale/maximale | 0.0-100.0 |

---

## <a name="flanges--couplings"></a>12. Flanges / Couplings

**Usage :** Place des brides/raccords sur des courbes existantes.

### Workflow
1. Créer ou sélectionner une **Curve** (câble/tube)
2. Régler la taille et l'espacement des flanges
3. Cliquer **Execute**

### Paramètres
| Paramètre | Description | Plage |
|-----------|-------------|-------|
| **Seed** | Seed de randomisation | 0-∞ |
| **Flange Size** | Rayon de la bride | 0.001-0.5 |
| **Flange Depth** | Épaisseur | 0.001-0.1 |
| **Spacing** | Distance entre brides | 0.01-10.0 |
| **Probability** | Probabilité de placement | 0.0-1.0 |
| **Use Existing Curve** | Utiliser la courbe sélectionnée | Booléen |

### Conseils
- Fonctionne avec les courbes créées par **Random Cables**
- **Spacing = 0.5** pour des brides régulières

---

## <a name="presets"></a>13. Presets

**Usage :** Sauvegarder et charger des configurations de paramètres.

### Workflow
1. Régler tous les paramètres souhaités
2. Donner un nom au preset
3. Cliquer **Save Preset**
4. Pour charger : sélectionner le preset et cliquer **Load**

---

## <a name="utilitaires"></a>14. Utilitaires

### Randomize Seed
Génère une nouvelle seed aléatoire pour tous les outils.

### Reset Settings
Réinitialise tous les paramètres à leurs valeurs par défaut.

### Rebuild
Réexécute le dernier opérateur avec les mêmes paramètres.

---

## <a name="conseils"></a>15. Conseils et Bonnes Pratiques

### Général
- **Toujours travailler en Edit Mode** avec une sélection active
- **Sauvegarder avant** d'appliquer des opérations complexes
- Utiliser **Undo (Ctrl+Z)** si le résultat ne convient pas
- Le **Rebuild** est utile pour itérer rapidement

### Performance
- Éviter les **Iterations > 5** sur des meshes denses
- Pour le **Scatter**, limiter la densité sur de grandes surfaces
- Les **Tubes** et **Cables** créent des objets séparés : nettoyer si nécessaire

### Workflow recommandé
1. **Random Panels** pour la base structurelle
2. **Loop Extrude** pour ajouter du détail
3. **Panel Screws** pour les rivets/vis
4. **Random Tubes** ou **Cables** pour les tuyaux
5. **Flanges** sur les courbes pour les raccords

### Dépannage
| Problème | Solution |
|----------|----------|
| Aucun résultat | Vérifier qu'on est en Edit Mode avec une sélection |
| Mesh corrompu | Augmenter le **Safety Margin** |
| Trop de faces | Réduire **Probability** ou **Density** |
| Objets non alignés | Activer **Align to Normal** |

---

## Mises à jour

**v1.0.0**
- 10 outils de génération procédurale
- Système de presets
- Tests unitaires (21 tests)
- Support complet de la seed pour la reproductibilité
