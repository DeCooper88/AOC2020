from collections import defaultdict, deque
from helpers import file_reader
from typing import Deque, Dict, List, Set, Tuple
from time import perf_counter


def compute(data: List[str]) -> str:
    food_ingredients: Dict[int, Set] = {}  # maps food IDs to it's ingredients
    allergen_foods = defaultdict(list)  # maps allergens to food IDs
    all_ingredients: Set[str] = set()  # all unique ingredients
    for food_id, line in enumerate(data):
        raw_ingredients, raw_allergens = line.strip().split(" (contains ")
        raw_allergens = raw_allergens.replace(")", "")
        allergens = raw_allergens.strip().split(", ")
        ingredients = set(raw_ingredients.split(" "))
        all_ingredients = all_ingredients | ingredients  #
        food_ingredients[food_id] = ingredients
        for al in allergens:
            allergen_foods[al].append(food_id)
    allergen_ingredients = {}
    for allergen, foods in allergen_foods.items():
        in_all = food_ingredients[foods[0]]
        for food in foods[1:]:
            in_all = in_all & food_ingredients[food]
        allergen_ingredients[allergen] = in_all
    potentials = set()
    for pot in allergen_ingredients.values():
        for x in pot:
            potentials.add(x)
    wrong_ingredients = all_ingredients - potentials
    appearances = 0
    for wrong in wrong_ingredients:
        for ingred in food_ingredients.values():
            if wrong in ingred:
                appearances += 1
    print("solution part 1:", appearances)
    # part 2:
    potential_tups = []
    frontier: Deque[Tuple] = deque()
    for al, ing in allergen_ingredients.items():
        potential_tups.append((al, ing))
        frontier.append((al, ing))
    seen: Set[str] = set()
    dangerous = []
    while frontier:
        current = frontier.popleft()
        alg, pot_set = current
        pts = pot_set - seen
        if len(pts) == 1:
            pt_name = pts.pop()
            dangerous.append((alg, pt_name))
            seen.add(pt_name)
        else:
            frontier.append(current)
    danger_list = ""
    for p in sorted(dangerous, key=lambda z: z[0]):
        danger_list = danger_list + p[1] + ","
    return danger_list[:-1]


if __name__ == "__main__":
    t0 = """
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)
    """

    start = perf_counter()
    day21 = file_reader("inputs/2020_21.txt", output="lines")
    print("solution part 2:", compute(day21))
    end = perf_counter()
    print(f"total runtime: {round((end - start) * 1000, 1)}ms")
