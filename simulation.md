# Simulation Document
## Initialization
Parameters serves as the inputs of the simulation, in JSON format. In `input/parameters.json`，parameters are adjustable for simulation set-up. Below is a brief introduction to these parameters.
- **Compulsory parameters**:
    - `round`: integer, the number of rounds for a simulation.
    - `timestep`: integer, the number of steps within a round.
    - `is_derected`: either `true` or `false`. This suggests whether the social network is a directed graph or not.
    - `is_external_dataset`: either `ture` or `false`. If the value is `true`, suggests to use external datasets after conversion. `false` uses the synthetic random network.
    - `broadcasting_prob`: a float value in the range between [0,1]. This is the broadcasting probability of each user agent to get the inital broadcasting message, and therefore functions as a seed user.
- **Optional parameters**:
    You can define ***social network*** in **one of these ways** with the optional parameters:
  1. Use synthetic network: a random network based on Erdos-Renyi model is built with self-defined values, powered by Networkx. Some parameters need to be assigned to construct this synthetic network:
     1. `node_size`: integer, the number of nodes in a graph.
     2. `connect_prob`: float in the range between [0,1]. This is the probability of the nodes connecting to each other. 
  2. Use external dataset: alternatively, we support real-world dataset to be used for the simulation, through our conversion tool provided in `dataset_conversion_tool.py`. 
     Conversion tool support input dataset in a `TXT` format. An example of the dataset is like
      ```
      30	1412
      30	3352
      3	54
      ```
      Each line suggests an edge between node i and node j. If this was a directed network, nominate it in `input/parameter.json` by setting `is_directed` equals `ture`. So that it represents a directed edge from node i to node j.
      
      Run `python tools/dataset_tool.py -d dataset_file_name` so the input TXT file will be saved in `saved/graph.G` directly.

    You can adjust ***seed set*** in **one of these ways** with the optional parameters:
  1. `seed_set_size`: integer, define the seed size of influence diffusion. Note we currently only support random selection, so the seeds can be different but with a defined seed set size. `"seed_set_size": 1` suggests there is one seed selected at the beginning of the diffusion.
  2. `seed_set`: string, define the seed set of influence diffusion. So the seed set is fixed as what it defined. Multiple seeds can be set in a list format. `"seed_set": "[1, 5]"` suggests the seed set is `[1, 5]`, so users 1 and 5 are selected as seed.
  3. Alternatively, you do not need to assign seeds when initializing a simulation, so user 1 will be set as the seed by default.
## File Structure
    ```
        | input # save input files, like external dataset (in TXT format), and parameter setting file (in JSON format).
            parameter.json
            facebook.txt
        | saved # save output files, like graph file (in G format, loaded by pickle)
            graph1.G
        | model # models
            agent.py
            environment.py
        | tool # tools
            dataset_tool.py
        | visualizer # for visualization files
            app.py
    ```
## Visualization