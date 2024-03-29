# Quantum Energy Trading
This project, developed within the [Quantum Open Source Foundation Mentorship Program](https://qosf.org/qc_mentorship/), aims to shed light to the practical uses of Variational Quantum Algorithms (VQAs) in the energy sector. In particular, we tackle the problem of energy trading between prosumers in decentralized energy networks under the [Transactive Energy (TE) framework](https://www.nist.gov/el/smart-grid-menu/hot-topics/transactive-energy-overview). In this scenario, the individual users act as both consumers and producers in the network, and the problem lies in finding optimal peer-to-peer trading strategies to maximize their benefits.

## Approach
Peer-to-peer energy trading under the TE framework poses a considerable computational challenge, and classical approaches like the [ADMM](https://ieeexplore.ieee.org/ielaam/5165411/9460803/9369412-aam.pdf) algorithm become slow or innacurate for larger networks. VQAs have emerged recently as a NISQ-friendly approach to this type of combinatorial optimization problems, and [hybrid versions of classical approaches](https://qiskit.org/ecosystem/optimization/tutorials/05_admm_optimizer.html) have been proposed. Although there are [existing studies](https://www.researchgate.net/publication/369550169_Quantum_Software_Architecture_Blueprints_for_the_Cloud_Overview_and_Application_to_Peer-2-Peer_Energy_Trading) applying quantum annealing technologies to this problem, our work uses a [QAOA](https://arxiv.org/pdf/1411.4028.pdf) as a gate-based approach to try to find more suitable formulations.

## Data
Similarly to [this](https://www.researchgate.net/publication/369550169_Quantum_Software_Architecture_Blueprints_for_the_Cloud_Overview_and_Application_to_Peer-2-Peer_Energy_Trading) previous study, we will generate a sythetic dataset to simplify the handling of data protection requirements. The code for the creation of this dataset is included within the project.

## Usage
To create the Docker image and run this repository in a container, open a terminal and run:
```
docker build . -t quantum-energy-trading
```
To run the image:
```
docker run quantum-energy-trading
```
You should see the following:
```
Transactive Energy Market Summary

--------------------------------------

Number of samples: 15000

Hourly Transactions Range: [10, 123]

Price Range (cents/KWh): [8, 32]

Bid Range (KWh): [1, 5]
Ask Range (KWh): [5, 10]
```
