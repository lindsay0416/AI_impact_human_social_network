import json

def load_results_from_file():
    with open("saved/results.json", "r") as file:
        results = json.load(file)
        results = results.get("simulation")
    for simulation in results:
        round = simulation.get("round")
        result = simulation.get("result")
        for r in result:
            coverage = r.get("data")[0].get("coverage")
            print(coverage)
        print(f" ======== Round {round} ======== ")

if __name__ == "__main__":
    load_results_from_file()