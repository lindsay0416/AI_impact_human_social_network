# Simulation Document
## Initialization
Parameters serves as the inputs of the simulation, in JSON format. In `saved/parameters.json`，parameters are adjustable for simulation set-up. Below is a brief introduction to these parameters.
- **Compulsory parameters**:
    - `round`: integer, the number of rounds for a simulation.
    - `timestep`: integer, the number of steps within a round.
    - `is_derected`: either `true` or `false`. This suggests whether the social network is a directed graph or not.
- **Optional parameters**:

    You can define ***social network*** in **one of these ways** with the optional parameters:
  1. Use synthetic network: a random network based on Erdos-Renyi model is built with self-defined values, powered by Networkx. Some parameters need to be assigned to construct this synthetic network:
     1. `node_size`: integer, the number of nodes in a graph.
     2. `connect_prob`: float in the range between [0,1]. This is the probability of the nodes connecting to each other. 
  2. Use external dataset: alternatively, we support real-world dataset to be used for the simulation, through our conversion tool with `dataset_conversion_tool.py`. 

You can adjust ***seed set*** in **one of these ways** with the optional parameters:
  1. `seed_set_size`: integer, define the seed size of influence diffusion. Note we currently only support random selection, so the seeds can be different but with a defined seed set size. `"seed_set_size": 1` suggests there is one seed selected at the beginning of the diffusion.
  2. `seed_set`: string, define the seed set of influence diffusion. So the seed set is fixed as what it defined. Multiple seeds can be set in a list format. `"seed_set": "[1, 5]"` suggests the seed set is `[1, 5]`, so users 1 and 5 are selected as seed.
  3. Alternatively, you do not need to assign seeds when initializing a simulation, so user 1 will be set as the seed by default.
  