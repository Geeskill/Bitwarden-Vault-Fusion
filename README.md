# 🔐 Bitwarden Vault Fusion

Un outil en ligne de commande (CLI) écrit en Python pour fusionner intelligemment deux exports non chiffrés (`.json`) provenant de **Bitwarden** ou **Vaultwarden**.

Ce script résout le problème classique lors de la fusion de deux comptes : **l'avalanche de doublons**.

## ✨ Fonctionnalités

*   **Fusion Intelligente** : Compare les entrées sur la base de 4 critères essentiels :
    1.  Nom de l'entrée
    2.  Nom d'utilisateur
    3.  Mot de passe
    4.  URL
*   **Détection de Doublons** : Si ces 4 critères sont identiques, l'entrée est considérée comme un doublon et est ignorée (même si la date de modification ou le dossier diffère).
*   **Sécurité des Conflits** : Si deux entrées ont le même nom mais un mot de passe différent, **les deux sont conservées** pour éviter toute perte de données.
*   **Interface Visuelle** : Affichage coloré dans le terminal pour suivre ce qui est supprimé, ajouté ou en conflit.
*   **Aucune dépendance** : Fonctionne avec Python 3 standard (pas besoin de `pip install`).

## 🚀 Prérequis

*   Python 3.x installé.
*   Deux exports au format **JSON (non chiffré)** depuis votre coffre-fort.

## 🛠️ Installation

1.  Clonez ce dépôt ou téléchargez le fichier `Bitwarden_Vault_Fusion.py`.
2.  Assurez-vous d'avoir vos deux fichiers `.json` d'export dans le même dossier.

## 💻 Utilisation

Ouvrez un terminal et lancez la commande suivante :

```bash
python3 Bitwarden_Vault_Fusion.py fichier_base.json fichier_apport.json
```

*   **fichier_base.json** : Le fichier principal (sa structure de dossiers sera conservée).
*   **fichier_apport.json** : Le fichier secondaire dont vous voulez récupérer les éléments manquants.

### Résultat
Le script générera un nouveau fichier nommé :
👉 **`fusion_finale.json`**

## 📖 Comprendre la sortie (Légende)

Le script utilise des codes couleurs et des icônes pour faciliter la lecture :

| Icône | Couleur | Signification |
| :--- | :--- | :--- |
| 🗑️ | **Jaune** | **Doublon ignoré**. L'entrée existe déjà à l'identique dans le fichier de base. |
| ➕ | **Vert** | **Ajout**. L'entrée n'existait pas, elle a été ajoutée. |
| ⚔️ | **Rouge** | **Conflit potentiel**. Le nom est identique mais le mot de passe diffère. L'entrée a été **AJOUTÉE** (doublon visuel dans le coffre) pour que vous puissiez vérifier manuellement laquelle garder. |

## 🔄 Workflow recommandé

1.  Exportez vos coffres au format `.json` (Non chiffré).
2.  Exécutez `Bitwarden_Vault_Fusion.py`.
3.  Vérifiez le résumé final dans le terminal.
4.  Importez `fusion_finale.json` dans votre Vaultwarden/Bitwarden.
5.  **Important** : Recherchez ensuite manuellement les éventuels conflits (les lignes marquées ⚔️) dans votre coffre pour supprimer l'ancienne version obsolète.
6.  Supprimez les fichiers `.json` de votre ordinateur.

## ⚠️ Avertissement de Sécurité

Les fichiers `.json` manipulés contiennent **tous vos mots de passe en clair**.

*   Ne lancez jamais ce script sur une machine partagée ou compromise.
*   Supprimez les fichiers `.json` (entrée et sortie) immédiatement après l'importation.
*   Sur Linux, utilisez la commande `shred` ou `rm` de manière sécurisée si possible.

Licence : MIT (Open Source).
