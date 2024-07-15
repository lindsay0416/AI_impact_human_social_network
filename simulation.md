# Simulation Document
## File Structure
    ```
        | input # save input files, like external dataset (in TXT format), parameter setting file (in JSON format), and user profile file (in JSON format)
            ego-Facebook.txt
            parameter.json
            user_profile.json
        | saved # save output files, like graph files (one in G format, loaded by pickle; another is in JSON format, save nodes (such as id and profile data, and edges information)) and results (saved in JSON format)
            graph.G
            results.json
            graph.json
        | model # object models. This includes Agent object, Environment object, and Message object.
            agent.py
            environment.py
            message.py
        | tool # tools for connect Elastic Search, openAI, and for dataset usage.
            dataset_tool.py
            config_manager.py # open AI API configration
            elastic_search.py
            es_manager.py
        | visualizer # for visualization files
            app.py
        simulation.py # the entry of the simulation
    ```
## Initialization
Parameters serves as the inputs of the simulation, in JSON format. In `input/parameters.json`，parameters are adjustable for simulation set-up. Below is a brief introduction to these parameters.
- **Compulsory parameters**:
    - `round`: integer, the number of rounds for a simulation.
    - `timestep`: integer, the number of steps within a round.
    - `is_directed`: either `true` or `false`. This suggests whether the social network is a directed graph or not.
    - `is_external_dataset`: either `ture` or `false`. If the value is `true`, suggests to use external datasets after conversion. `false` uses the synthetic random network.
    - `influence_prob`: a float value in the range between [0,1]. This indicates the probability of a user agent to be influenced by one of its in-neighbours.
    - `broadcasting_prob`: a float value in the range between [0,1]. This is the broadcasting probability of each user agent to get the inital broadcasting message, and therefore functions as a seed user.
- **LLM-related parameters**:
    Some parameters are used for LLM module to generate textual messages. These includes: user profile and initial message.

    The initial message `initial_message` is a piece of textual information, such as news, a released policy, or a public event, that is proposed to be propagated through the network to simulate public responses to this message.

    `generate_user_profile`: either true or false. If this parameter is set to true, user profiles will be (re-)generated at the beginning of the simulation. Otherwise, user profiles will be based on pre-defined profiles. A user profile is a dictionary, as shown below:
    ```
    "N1": {
        "name": "Ethan",
        "age": 27,
        "gender": "male",
        "description": "an adventurous traveler who enjoys exploring new cultures and cuisines. He documents his journeys through photography and shares tips on budget-friendly travel."
    }
    ```
    All user profiles are stored in an input JSON file, located at `input/user_profile.json`.

    `user_profile_prompt`: string, the prompt used for LLM to generate user profile.
- **Optional parameters**:
    You can define ***social network*** in **one of these ways** with the optional parameters:
  1. Use synthetic network: a random network based on the Holme and Kim algorithm is built with self-defined values, powered by [Networkx](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.powerlaw_cluster_graph.html). Some parameters need to be assigned to construct this synthetic network:
     1. `node_size`: integer, the number of nodes in a graph.
     2. `random_edges`: integer in the range between [1,node_size]. The number of random edges to add for each new node.
     3. `connect_prob`: float in the range between [0,1]. Probability of adding a triangle after adding a random edge. 
  2. Use external dataset: alternatively, we support real-world dataset to be used for the simulation, through our conversion tool provided in `dataset_conversion_tool.py`. 
     Conversion tool support input dataset in a `TXT` format. An example of the dataset is like
      ```
      30	1412
      30	3352
      3	54
      ```
      Each line suggests an edge between node i and node j. If this was a directed network, nominate it in `input/parameter.json` by setting `is_directed` equals `ture`. So that it represents a directed edge from node i to node j.
      
      Run `python tools/dataset_tool.py -d dataset_file_name` so the input TXT file will be saved in `saved/graph.G` directly.

Below table shows a summary of these parameters:
| parameter  | type  | compulsary  | range  |
|---|---|---|---|
|  round | int  |  :heavy_check_mark: |   |
| timestep | int  |  :heavy_check_mark: |   |
| influence_prob |  float |  :heavy_check_mark: | `[0,1]`  |
| is_directed |  boolean |  :heavy_check_mark: | `{true, false}`  |
| is_external_dataset |  boolean |  :heavy_check_mark: | `{true, false}` |
| node_size |  int |  depends on `is_external_dataset` is `false` |  |
| random_edges |  int | depends on `is_external_dataset` is `false` | `[1,node_size]`  |
| connect_prob | float  |  depends on `is_external_dataset` is `false`  | `[0,1]`  |
| generate_user_profile | boolean  |  :heavy_check_mark: | `{true, false}` |
| user_profile_prompt | str  |  :heavy_check_mark: |   |
| broadcasting_prob | float  |  :heavy_check_mark: |  `[0,1]`  |
| initial_message | str  |  :heavy_check_mark: |  |

## Information Propagation
When a piece of news is released to the public via platforms like newspapers or websites, every member (or agent) of a social network has an equal opportunity to access this news. Once an agent reads the news, they begin sharing it with their neighbors within the network.

As the news spreads, the propagation is not just a simple relay of information. Instead of merely passing along the news as is, agents engage interactively. This means when an agent shares the news with a neighbor, they also express their thoughts, opinions, or reactions to the news. Meanwhile, once a neighbor is influenced by the spreading information, it is respond with its own opinions and reactions.

The information propagation ends if there is no user agents can be influenced.