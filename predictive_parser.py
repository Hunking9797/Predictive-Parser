# Some helper functions
def print_iter(Matched, Stack, Input, Action, verbose=True):
    if verbose == True:
        print(
            ".".join(Matched).ljust(30),
            " | ",
            ".".join(Stack).ljust(25),
            " | ",
            ".".join(Input).ljust(30),
            " | ",
            Action,
        )


# The predictive parsing algorithm
def predictive_parsing(sentence, parsingtable, terminals, start_state="S", verbose=True):
    status = None
    match = []
    stack = [start_state, "$"]
    Inp = sentence.split(".")
    if verbose == True:
        print_iter(["Matched"], ["Stack"], ["Input"], "Action")
    print_iter(match, stack, Inp, "Initial", verbose)
    action = []
    while len(sentence) > 0 and status != False:
        top_of_input = Inp[0]
        pos = top_of_input
        if stack[0] == "$" and pos == "$":
            print_iter(match, stack, Inp, "Accepted", verbose)
            return "Accepted"
        if stack[0] == pos:
            print_iter(match, stack, Inp, "Pop", verbose)
            match.append(stack[0])
            del stack[0]
            del Inp[0]
            continue
        if stack[0] == "epsilon":
            print_iter(match, stack, Inp, "Poping Epsilon", verbose)
            del stack[0]
            continue
        try:
            production = parsingtable[stack[0]][pos]
            print_iter(match, stack, Inp, stack[0] + " -> " + production, verbose)
        except:
            return "error for " + str(stack[0]) + " on " + str(pos), "Not Accepted"

        new = production.split(".")
        stack = new + stack[1:]
    return "Not Accepted"


if __name__ == "__main__":
    # input for the grammar : E->TE1;E1->+TE1|epsilon;T->FT1 ...
    parsingtable = {
        "E": {"id": "T.E1", "(": "T.E1"},
        "E1": {"+": "+.T.E1", ")": "epsilon", "$": "epsilon"},
        "T": {"id": "F.T1", "(": "F.T1"},
        "T1": {"+": "epsilon", "*": "*.F.T1", ")": "epsilon", "$": "epsilon"},
        "F": {"id": "id", "(": "(.E.)"},
    }
    terminals = ["id", "(", ")", "+", "*"]
    print(
        predictive_parsing(
            sentence="(.id.+.id.).*.(.id.+.id.).$",
            parsingtable=parsingtable,
            terminals=terminals,
            start_state="E",
            verbose=True,
        )
    )
