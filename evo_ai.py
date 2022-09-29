#!/usr/bin/env python3

# TODO: Rename variables to match terminology from lectures



def cellular_automaton(ruleset, initial_values):
    '''
        performs update step

        ruleset is an array of possible rules

        initial values is binary string from observations

        TODO: add parameter for substr size (should be odd value?)
    '''

    # variable declaration
    new_values = ""


    print(f'initial values:\t{initial_values}')

    # range is size of cellular automaton
    for i in range(6):
        substr = ""
        substr = substr + initial_values[i-1] + initial_values[i] + initial_values[(i+1)%6]
        # print(substr)

        # convert substr = decimal
        substr_10 = int(substr, 2)

        # check for match in ruleset and save resulting value to new grid
        if substr_10 in ruleset:
            new_values = new_values + "1"
            # print("found match")
        else:
            new_values = new_values + "0"
    # /loop

    print(f'new values:\t{new_values}')
    
    # return new_values

# def ca_output(new_val):

# if more 1s, go right, else go left






def main():
    cellular_automaton([5], "101110")




if __name__ == "__main__":
    main()