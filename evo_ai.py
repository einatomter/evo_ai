# ruleset is an array of possible rules
# initial_values are the binary configuration of the observations
def cellular_automaton(ruleset, initial_values):
    '''
        # 000 = 0 0
        001 = 1 1
        # 010 = 0 2
        # 011 = 0 3
    '''

    # range is size of cellular automaton
    for i in range(6):
        substr = [initial_values[i-1], initial_values[i], initial_values[(i+1)%6]]
        print(substr)

        # convert substr = decimal

        # when ruleset match found:
        # x = function(3)

        # save to new grid
        # new_val.append(x)

# def ca_output(new_val):

# if more 1s, go right, else go left

cellular_automaton(1, "123456")