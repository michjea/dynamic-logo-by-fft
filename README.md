# Logos dynamiques par FFT

Ce projet permet la modification en continu d'un logo grâce à la modification de sa représentation spectrale.

[Lien wiki](https://gitlab-etu.ing.he-arc.ch/isc/2022-23/niveau-3/3281.1-projet-p3-sa-il/214/logos-dynamiques-par-fft/-/wikis/home)

## Arborecense

Le dossier ´lib´ contient les fichiers nécessaires au fonctionnement du programme.

Les dossiers ´static´ et ´templates´ contiennent les fichiers nécessaires au fonctionnement de l'interface web.

Le fichier ´gif_generator.py´ permet de générer un gif à partir d'une image et d'un fichier de paramètres.

Le fichier ´app.py´ permet de lancer l'interface web.

Le fichier ´parameters.json´ contient les paramètres par défaut.

Le fichier ´requirements.txt´ contient les dépendances nécessaires au fonctionnement du programme.

## Installation

Premièrement, il faut vous assurer que Python est installé sur votre machine.

Pour ce faire, ouvrez un terminal et tapez la commande suivante :

    ``` bash
    python --version
    ```

Si Python n'est pas installé, vous pouvez le télécharger [ici](https://www.python.org/downloads/).

Deuxièmement, il faut vérifier que vous avez pip installé sur votre machine.

Pour ce faire, ouvrez un terminal et tapez la commande suivante :

    ``` bash
    pip --version
    ```

Si pip n'est pas installé, vous pouvez le télécharger [ici](https://pip.pypa.io/en/stable/installation/).

Si vous désirez installer les dépendances dans un environnement virtuel, vous pouvez suivre cette méthode :

    ``` bash
    pip install virtualenv
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

Sinon, vous pouvez installer les dépendances directement sur votre machine :

Pour installer les dépendances :

    ``` bash
    pip install -r requirements.txt
    ```

## Utilisation

Pour lancer l'interface web :

    ``` bash
    python app.py
    ```

Pour lancer le programme :

    ``` bash
    python gif_generator.py "logo.png" "parameters.json
    ```

Le programme va générer un fichier dans le dossier courant. Il est possible de modifier le nom du fichier dans le fichier ´parameters.py´. Le fichier généré est un fichier gif. Le programme utilise l'image ´logo.png´ comme image de base. Il est possible de modifier cette image dans le fichier ´Gif.py´.

## Paramètres

Les paramètres sont modifiables dans le fichier ´parameters.py´.
