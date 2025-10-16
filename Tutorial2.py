# Generate every combination of truth values for n variables
def generate_combinations(n):
    combinations = []
    for i in range(2 ** n):
        combo = []
        for j in range(n):
            value = (i >> j) & 1
            combo.append(bool(value))
        combinations.append(combo)
    return combinations


# Evaluate each sentence with the given variables
def evaluate_sentences(sentences, variables, values):
    env = dict(zip(variables, values))
    results = []
    for s in sentences:
        expr = s
        # Replace variables with their truth values
        for var in variables:
            expr = expr.replace(var, str(env[var]))
        # Format sentences for python commands
        expr = expr.replace('^', ' and ')
        expr = expr.replace('v', ' or ')
        expr = expr.replace('¬', ' not ')
        expr = expr.replace('->', ' <= ')
        # Evaluate and record result
        results.append(eval(expr))
    return all(results)


# === MAIN PROGRAM ===

print("\nEnter your propositional sentences (one per line). Type 'done' when finished:")
sentences = []
while True:
    line = input("> ").strip()
    if line.lower() == "done":
        break
    if line:
        sentences.append(line)

# Input variaqble names
variables = input("\nEnter all propositional variables separated by spaces (e.g. A B C D): ").split()

# Compute all combinations of truth values
combinations = generate_combinations(len(variables))

# Print the models for each set of sentences
print("\n--- Models that satisfy the sentences ---")
found = False
for combo in combinations:
    if evaluate_sentences(sentences, variables, combo):
        print(dict(zip(variables, combo)))
        found = True

if not found:
    print("No models found.")
