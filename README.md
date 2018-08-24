# PDBe API Training Notebooks

This repository contains Jupyter Notebooks that can be used as training materials for understanding how the PDBe REST API works, and provides a number of examples of answering specific questions about PDB entries using the API.

## Getting Started

You will need to have Jupyter installed on your machine. For Linux/OSX machines, simply type:

```
pip3 install --upgrade pip
pip3 install jupyter
```

For Windows machines (optionally also for Linux/OSX) you can install Jupyter with Anaconda:
https://www.anaconda.com/download/

### Prerequisites

If installing using Anaconda, there is no additional prerequisites. If installing using pip3, you will need to have Python3 on your machine, and of course pip3

### Installing

From command line on Unix machine these would be the steps setting up everyone:

```
mkdir pdbe_jupyter
cd pdbe_jupyter
git clone https://github.com/PDBeurope/pdbe-api-training .
jupyter notebook
```

Jupyter Notebook will open a window in your browser, and you can select the specific notebooks you would like to view.

## Authors

* **Mihaly Varadi** - *Initial work* - [mvaradi](https://github.com/mvaradi)

## License

This project is licensed under the EMBL-EBI License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to the PDBe team for suggestions during creating these materials
