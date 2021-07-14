# NEAT data preprocessing service

## Project description

This project is designed to predict the data of the presented regression model. The neuroevolutionary algorithm ["Neuroevolution of augmenting topologies"(PDF)](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf) is used for forecasting.
The project is presented in a microservice architecture and includes the following components: 

1. [User's requests processing service](https://github.com/SkaaRJik/neatvue) 
2. [Data preprocessing service](https://github.com/SkaaRJik/neat-data-preprocessing) <- You are here
3. [Prediction service](https://github.com/SkaaRJik/neat-executor)
4. [Graphical user interface](https://github.com/SkaaRJik/neatvue)
5. PostgresSQL 11
6. SMB protocol (Linux: Samba)
7. RabbitMQ 

## Service description

This service is responsible for validation, normalization, denormalization of datasets and generating reports with predicted results.

## Minimal system requirements

<ol>
<li>CPU: 2core 2 Ghz </li>
<li>RAM: 8Gb</li>
<li>Free disk space: 10GB</li>
</ol>

## Requirements

<ol>
<li>Python 3.9</li>
<li>RabbitMQ</li>
<li>Samba</li>
</ol>

## Running

<ol>
<li>Activate python virtual environment</li>

`/venv/activate`

<li>Install dependencies</li>

`pip3 install -r ./requirements.txt`

<li>Run RabbitMQ if it is not active</li>
<li>Run Samba if it is not active</li>

<li>Run service</li>

`python ../main.py` 

</ol> 