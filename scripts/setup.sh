#!/usr/bin/env bash

conda create --name py36 python=3.6
conda activate py36
conda install -c conda-forge poppler
conda install -c conda-forge beautifulsoup4
conda install -c conda-forge pandas
conda install -c conda-forge openpyxl
