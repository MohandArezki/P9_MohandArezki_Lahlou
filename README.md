# Projet 09 : Développez une application Web en utilisant Django

<center>
    <img src="assets/logo-black.png" alt="Logo" />
</center>

## Table des matiéres
- [A - Présentation du projet](#a---présentation-du-projet)
- [B - Fonctionnalités mises en place](#b---fonctionnalités-mises-en-place)
- [C - Obtenir le code source](#c---obtenir-le-code-source)
- [D - Environnement virtuel](#d---environnement-virtuel)
  - [1 - Activer l'environnement virtuel](#1---activer-lenvironnement-virtuel)
  - [2 - Installer les prérequis](#2---installer-les-prérequis)
- [E - Utilisation](#e---utilisation)

## A - Présentation du projet

Réalisation d'un MVP de LITReview, site communautaire de partage de critiques de livres.

## B - Fonctionnalités mises en place

Un utilisateur peut :
- s’inscrire : créer un compte;
- se connecter  – le site n'est pas accessible à un utilisateur non connecté;
- consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'il suit, classés par ordre chronologique, les plus récents en premier;
- créer de nouveaux tickets pour demander une critique sur un livre/article ;
- créer des critiques en réponse à des tickets ;
- créer des critiques qui ne sont pas en réponse à un ticket. Dans le cadre d'un processus en une étape, l'utilisateur créera un ticket puis un commentaire en réponse à son propre ticket ;
- voir, modifier et supprimer ses propres tickets et commentaires ;
- suivre les autres utilisateurs en entrant leur nom d'utilisateur ;
- voir qui il suit et suivre qui il veut ;
- cesser de suivre un utilisateur.

## C - Obtenir le code source

Vous pouvez obtenir le code source en téléchargeant ce [lien](https://github.com/MohandArezki/P9_MohandArezki_Lahlou.git) ou en clonant le référentiel avec la commande suivante:
```
git clone git@github.com:MohandArezki/P9_MohandArezki_Lahlou.git
```

## D - Environnement virtuel

Pour créer l'environnement virtuel, exécutez:
```bash
python3 -m venv env
```

### 1 - Activer l'environnement virtuel
```bash
source env/bin/activate
```

### 2 - Installer les prérequis
```bash
pip install -r requirements.txt
```

## E - Utilisation
1. Lancer le serveur Django:
```bash
python manage.py runserver
```

2. Pour tester l'application, accédez à l'URL http://127.0.0.1:8000/ dans le navigateur.
   Pour l'administration : http://127.0.0.1:8000/admin/

### Coordonnées d'accès

| Utilisateur     | Mot de passe   |
|-----------------|----------------|
| Administrateur  | P@ssword123    | 
| ethan           | P@ssword123    |
| ava             | P@ssword123    |
| isabella        | P@ssword123    |
| liam            | P@ssword123    |
| lucas           | P@ssword123    |

```