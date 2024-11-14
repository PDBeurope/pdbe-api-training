# PDBe API Training Notebooks

This repository contains Jupyter Notebooks that can be used as training materials for understanding how the PDBe REST API works, and provides a number of examples of answering specific questions about PDB entries using the API.


## Getting started with Docker (recommended)

This option launches the summer school notebooks in a Docker container. This is the recommended way to run the notebooks as it ensures that all dependencies are correctly installed and that the notebooks will run as expected.

Make sure your [Docker](https://docs.docker.com/engine/install/) is running on your machine before executing the following commands:

### Clone the repository
```console
git clone https://github.com/PDBeurope/pdbe-api-training .
cd /path/to/your/pdbe-api-training/
```

### Build the Docker container (you only need to do this once)
```console
docker build -t pdbe-api-training .
```

### Run the Docker container
```console
docker run -p 8888:8888 -v /path/to/your/pdbe-api-training/pdbe_tutorial_2024/:/pdbe_api_tutorial/pdbe_tutorial_2024 pdbe-api-training
```

Now open your browser and go to `http://localhost:8888/` and you should see the Jupyter Notebook interface. The `-v` flag ensures changes you make to the notebooks will be saved in the `pdbe_tutorial_2024` directory in the repository cloned to your local machine.

## Getting started with Binder

Notebooks can also be run on cloud via Binder. Click on the badge below to launch the notebooks in Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PDBeurope/pdbe-api-training/master)


## Getting started with Python and Jupyter

You will need to have Python3.10, pip3 and Jupyter installed on your machine.

### Upgrade pip3
```console
pip3 install --upgrade pip
```

For Windows machines (optionally also for Linux/OSX) you can install Jupyter with conda-forge:
https://conda-forge.org/

### Clone the repository

```console
mkdir pdbe_jupyter
cd pdbe_jupyter
git clone https://github.com/PDBeurope/pdbe-api-training .
```

### Install the dependencies and start Jupyter
```console
cd pdbe-api-training
pip3 install -r requirements.txt
jupyter ./pdbe_tutorial_2024
```

Jupyter Notebook will open a window in your browser, and you can select the specific notebooks you would like to view.


## Authors

* **Mihaly Varadi** - *Initial work* - [github](https://github.com/mvaradi)
* **John Berrisford** - *Additional notebooks* - [github](https://github.com/berrisfordjohn)
* **David Armstrong** - *PDBe statistics notebooks and other maintenance* - [github](https://github.com/drarmstrong)
* **Preeti Choudhary** - *Ligand interactions and predicted models notebooks* - [github](https://github.com/cypreeti)
* **Joseph Ellaway** - *Protein superposing notebooks* - [github](https://github.com/Joseph-Ellaway)
* **Marcus Bage** - *Complexes notebook and other maintenance* - [github](https://github.com/mbage)

## License

This project is licensed under the EMBL-EBI License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to the PDBe team for suggestions during creating these materials
