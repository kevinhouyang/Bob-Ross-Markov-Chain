import sys
import random

def update_value(word, value):
    """
    input: word to be searched, and value is a list of pairings
    """
    for pairings in value: #iterate through the list of pairings
        if pairings[0] == word: #check the first index for the word
            pairings[1] += 1 #increment the number stored in second index
            return

    value.append([word, 1]) #not one of the value stored, so add it to the list
    return


def replace_punctuation(text, punctuation):
    """
    given a list of punctuation marks, replace them each with the punctuation plus a space
    """
    for p in punctuation:
        new_text = text.replace(p, ' ' + p)
        text = new_text

    return text


def weighted_random(value):
    """
    goes through the list of pairings and adds each word to a list n number of times,
    where n is the value stored in the markov
    """
    weighted_list = []
    for v in value:
        weighted_list += [v[0]] * v[1]

    return random.choice(weighted_list)


def read_text(filename):
    """
    opens the file and reads its content as a string, removes any double line spaces,
    closes the file, and returns the string
    """
    with open(filename) as f:
        contents = f.read().replace('\n', ' ')
    return contents


def build_chain(text, chain = {}):
    """
    chain is a dictionary,
    """
    new_text = replace_punctuation(text, ',.;?!') # add a space before all punctuation so that they get counted as separate words

    words = new_text.split(' ') # split string
    index = 1

    for word in words[index:]:
        #print(chain)
        key = words[index - 1]
        if key in chain:
            update_value(word, chain[key]) # check if word has already followed key, increment accordingly
        else:
            chain[key] = [[word, 1]]
        index += 1

    return chain


def generate_text(chain, length):
    """
    generates number of words using weighted random choice from markov chain
    """
    word1 = random.choice(list(chain.keys()))
    print(word1)
    output = word1.capitalize()

    while length != 0:

        word2 = weighted_random(chain[word1])
        word1 = word2
        output += ' ' + word2
        length -= 1

    return output


def write_text(filename, output):
    """
    output generated text to a file
    """
    with open(filename, 'w') as f:
        f.write(output)

#TODO: build second order chain, fix formatting with spaces and punctuation

if __name__ == '__main__':
    markov = build_chain(read_text(sys.argv[1]))
    output = generate_text(markov, int(sys.argv[2]))
    write_text("bobrossoutput.txt", output)
