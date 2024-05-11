# Simulation Document
## Initialization
In `saved/parameters.json`，parameters are adjustable for simulation set-up. Below is a brief introduction to these parameters.
- **Compulsory parameters**:
    - `round`: integer, the number of rounds for a simulation.
    - `timestep`: integer, the number of steps within a round.
- **Optional parameters**:
    - You can adjust ***seed set*** in **one of these ways** with the optional parameters:
      1. `seed_set_size`: integer, define the seed size of influence diffusion. Note we currently only support random selection, so the seeds can be different but with a defined seed set size. `"seed_set_size": 1` suggests there is one seed selected at the beginning of the diffusion.
      2. `"seed_set"`: string, define the seed set of influence diffusion. So the seed set is fixed as what it defined. Multiple seeds can be set in a list format. `"seed_set": "[1, 5]"` suggests the seed set is `[1, 5]`, so users 1 and 5 are selected as seed.
      3. Alternatively, you do not need to assign seeds when initializing a simulation, so user 1 will be set as the seed by default.
  