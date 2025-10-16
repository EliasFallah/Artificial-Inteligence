def make_truth_combinations(number_of_variables):
    combinations = []
    total_combinations = 2 ** number_of_variables

    for i in range(total_combinations):
        single_combination = []
        for bit_position in range(number_of_variables):
            bit_value = (i >> bit_position) & 1
            single_combination.append(bool(bit_value))
        combinations.append(single_combination)

    return combinations


def check_sentences_are_true(sentences, variables, truth_values):
    environment = dict(zip(variables, truth_values))
    results = []

    for sentence in sentences:
        expression = sentence

        # Replace each variable with its truth value
        for var in variables:
            expression = expression.replace(var, str(environment[var]))

        # Convert logical symbols to Python operators
        expression = expression.replace('^', ' and ')
        expression = expression.replace('v', ' or ')
        expression = expression.replace('¬', ' not ')
        expression = expression.replace('->', ' <= ')

        # Evaluate the expression
        results.append(eval(expression))

    # Return True only if all sentences are True for this combination
    return all(results)


# ---------- Main Function ----------
print("Enter your propositional sentences (one per line).")
print("Type 'done' when finished.\n")

sentences = []
while True:
    line = input("> ").strip()
    if line.lower() == "done":
        break
    if line:
        sentences.append(line)

print("\nEnter all propositional variables separated by spaces (e.g., A B C D):")
variables = input("> ").split()

combinations = make_truth_combinations(len(variables))

print("\n--- Models that satisfy all sentences ---")
found_model = False

for combination in combinations:
    if check_sentences_are_true(sentences, variables, combination):
        model = dict(zip(variables, combination))
        print(model)
        found_model = True

if not found_model:
    print("No models found.")
