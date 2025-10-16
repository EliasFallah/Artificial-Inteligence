

# Global variables
rules = []
facts = set()

# ---------- Parsing the Knowledge Base ----------

def clean(text):
    return text.strip().rstrip('.').strip()

def parse_sentence(sentence):
    sentence = sentence.strip()
    if not sentence:
        return None

    # Split rules by => or -> (both supported)
    if '->' in sentence:
        rule, outcome = sentence.split('->', 1)
    else:
        # Fact (no implication)
        atom = clean(sentence)
        return {'type': 'FACT', 'consequent': atom, 'antecedents': []}

    atom = clean(outcome)
    rule = rule.strip()

    # Check if AND rule
    if '^' in rule:
        antecedents = [clean(x) for x in rule.split('^')]
        rule_type = 'AND'

    # Check if OR rule
    elif 'v' in rule:
        antecedents = [clean(x) for x in rule.split('v')]
        rule_type = 'OR'

    # Empty left side means fact
    elif rule == '':
        return {'type': 'FACT', 'consequent': atom, 'antecedents': []}

    # Single antecedent rule
    else:
        antecedents = [clean(rule)]
        rule_type = 'AND'

    return {'type': rule_type, 'consequent': atom, 'antecedents': antecedents}


def load_kb_from_lines(lines):
    global rules, facts
    rules = []
    facts = set()

    for line in lines:
        parsed = parse_sentence(line)
        if not parsed:
            continue
        if parsed['type'] == 'FACT':
            facts.add(parsed['consequent'])
        else:
            rules.append(parsed)


# ---------- Backward Chaining Reasoning ----------

def build_rule_index():
    index = {}
    for rule in rules:
        c = rule['consequent']
        if c not in index:
            index[c] = []
        index[c].append(rule)
    return index


def prove(goal, seen, rule_index):
    goal = clean(goal)

    # If already known fact
    if goal in facts:
        return True

    # Prevent infinite loops
    if goal in seen:
        return False

    seen.add(goal)

    # If goal can be produced by rules
    if goal in rule_index:
        for rule in rule_index[goal]:
            if rule['type'] == 'AND':
                all_true = True
                for ant in rule['antecedents']:
                    if not prove(ant, seen, rule_index):
                        all_true = False
                        break
                if all_true:
                    return True

            elif rule['type'] == 'OR':
                for ant in rule['antecedents']:
                    if prove(ant, seen, rule_index):
                        return True

    # If no rule proves the goal
    return False

# ---------- Main Function ----------

def main():
    print("Extended Propositional Backward Chaining System")
    print("Enter rules and facts (e.g., 'A^B=>C' or 'A').")
    print("Type 'nil' to finish entering the knowledge base.\n")

    lines = []
    while True:
        line = input().strip()
        if line.lower() == 'nil':
            break
        if line:
            lines.append(line)

    load_kb_from_lines(lines)
    
    print("\nKnowledge base loaded.")
    print("Ask questions like 'P?' or type 'quit' to exit.\n")

    rule_index = build_rule_index()

    while True:
        query = input("reasoning>> ").strip()
        if query.lower() == 'quit':
            break
        if not query.endswith('?'):
            print("Use '?' at the end of your query.")
            continue

        goal = query[:-1].strip()
        proven = prove(goal, set(), rule_index)
        print("yes" if proven else "no")


if __name__ == "__main__":
    main()
