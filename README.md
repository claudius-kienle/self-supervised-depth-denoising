depth-denoising
==============================

self supervised depth denoising

Structure
======
- [Installation](#installation)
  - [Setup Environment](#setup-environment)
  - [Update Environment](#update-environment)
- [Project Organization](#project-organization)

Installation
=====

Setup Environment
------------------

The major packages will be installed with the conda environment.
Due to a bug in the Zivid Python package v2.3.0.2.5.0,
a pached version of this package will be installed.

### Create Conda Environment

**This repository requires the [Zivid SDK v2.5.0](https://www.zivid.com/downloads) to be installed already.
Otherwise the following commands will fail.**

Create a new conda environment with the required packages and activate it:

    conda env create -f depth-denoising.yml 
    conda activate depth-denoising


Update Environment
------------------
Make sure you are in the correct conda environment
    conda activate depth-denoising

execute following commands to update conda and pip files
**IMPORTANT: remove the zivid requirement from pip, as it must be installed by hand**

    conda env export > depth-denoising.yml


Project Organization
======

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
        └── roadmap.md     <- Lists the general roadmap
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

