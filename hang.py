#!/usr/bin/python
import requests, string, time, random

#Hangman AI
def main():
    playing = True
    while playing:
        #initialize badguesses storage and dictionary used for guessing
        badguess = []
        guessed = []
        
        wordfile = open("words.txt", 'r')

        #initialize dictionary list
    
        words = wordfile.readlines()

        # remove all newline characters in each word in the dictionary
        w = 0
        while w < len(words):
            words[w] = words[w].replace("\n", "")
            w += 1

        # initialize list of potential words each word in the phrase can
        #be
        potentialwords = []

        #all vowels
        #used for initial guesses
        commonletters = ['e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'l', 'c', 'u', 'd', 'p', 'm', 'h', 'g', 'b', 'f', 'y', 'w', 'k', 'v', 'x', 'z', 'j', 'q']
        gletter=0

        #get the initial state of the game and sleep for 1 second afterwards
        r = requests.get("http://upe.42069.fun/zt62p")
        print ("Got request")
        j = r.json()
        time.sleep(1)

        #split each word in the phrase into individual words (will be unknown)
        tempstring = j["state"]
        t = 0
        while t < len(tempstring):
            if (not tempstring[t].isalpha()) and (tempstring[t] != '_') and (tempstring[t] != '\''):
                tempstring = tempstring.replace(tempstring[t], ' ')
            t += 1
        strings = tempstring.split()

        # place all words with same length as string in strings into the potential word list
        #Only consider lower case words
        for pot in strings:
            subwords = []
            for word in words:
                if len(pot) == len(word):
                    subwords.append(word.lower())
            potentialwords.append(subwords)

        #remove contractions from potential word list that definetely don't
        #work as the apostrophe is in the wrong location
        p1 = 0
        while p1 < len(potentialwords):
            p2 = 0
            numwords = len(potentialwords[p1])
            while p2 < numwords:
                badcontraction = False
                p3 = 0
                while p3 < len(potentialwords[p1][p2]):
                    if ((potentialwords[p1][p2][p3] == '\'') or (strings[p1][p3] == '\'')) and (potentialwords[p1][p2][p3] != strings[p1][p3]):
                        badcontraction = True
                        break
                    p3 += 1
                if badcontraction:
                    potentialwords[p1].remove(potentialwords[p1][p2])
                    numwords -= 1
                else:
                    p2 += 1
            p1 += 1

        
        while j["status"] == "ALIVE":
            
            # if too many possible words, guess most common letters in English
            wordlistsize = []  #check for minimum potential words
            wordlistind = []

            #varibales to check potential word
            possible = False
            pindex = 0
            pwordind = 0
            guesscheck = j["remaining_guesses"]

            #checks if a word is potentially known
            for pwords in potentialwords:
                if(len(pwords) > 0 and len(pwords) <= 10):
                    possible=True
                    wordlistsize.append(len(pwords))
                    wordlistind.append(pindex)
                pindex += 1

            #guesses common letter if potential word not known
            if not possible:
                while(guessed.count(commonletters[gletter]) != 0):
                      gletter += 1
                r = requests.post("http://upe.42069.fun/zt62p", {'guess':commonletters[gletter]})
                print ("Guessed " + commonletters[gletter])
                guessed.append(commonletters[gletter])
                j = r.json()
                if j["remaining_guesses"] < guesscheck:
                    badguess.append(commonletters[gletter])
                gletter += 1;

            #otherwise guess letters from possible words
            
            else:
                #find word in phrase most likely known
                minval = min(wordlistsize)
                tempind = wordlistsize.index(minval)
                pindex = wordlistind[tempind]

                #pick a random word in your potential wordlist for the most
                #likely known word, and guess a letter not already guessed
                q = 0
                potwordr = random.randint(0, len(potentialwords[pindex])-1)
                while q < len(potentialwords[pindex][potwordr]):
                    if(guessed.count(potentialwords[pindex][potwordr][q]) == 0) and (potentialwords[pindex][potwordr][q] != '\''):
                        r = requests.post("http://upe.42069.fun/zt62p", {'guess':potentialwords[pindex][potwordr][q]})
                        print("Guessed " + potentialwords[pindex][potwordr][q])
                        j = r.json()
                        guessed.append(potentialwords[pindex][potwordr][q])
                        if j["remaining_guesses"] < guesscheck:
                            badguess.append(potentialwords[pindex][potwordr][q])
                        break
                    q += 1
            #update state of words
            tempstring = j["state"]
            print (tempstring)
            
            t = 0
            while t < len(tempstring):
                if (not tempstring[t].isalpha()) and (tempstring[t] != '_') and (tempstring[t] != '\''):
                    tempstring = tempstring.replace(tempstring[t], ' ')
                t += 1
            strings = tempstring.split()
            
            #update potential words list after guess is given 
            gy = 0
            while gy < len(potentialwords):
                xe = 0
                lengthlist = len(potentialwords[gy])
                while xe < lengthlist:
                    #no need to guess word if already solved
                    if potentialwords[gy][xe] == strings[gy]:
                        potentialwords[gy].clear()
                        break
                    le = 0
                    stilllegal = True
                    while le < len(potentialwords[gy][xe]):
                        # remove words that failed in the guess or who have
                        # letters in incorrect positiions
                        if (strings[gy][le].isalpha() and strings[gy][le] != potentialwords[gy][xe][le]) or (badguess.count(potentialwords[gy][xe][le]) != 0) or (strings[gy][le] == '_' and guessed.count(potentialwords[gy][xe][le]) != 0):
                            stilllegal = False
                            break
                        le += 1
                    if not stilllegal:
                        potentialwords[gy].remove(potentialwords[gy][xe])
                        lengthlist -= 1
                        continue
                    xe += 1
                gy += 1
            #sleep between requests
            time.sleep(1)
        #output final values and success or failure, along with number of games
        #and win rate
        print (j["lyrics"])
        if j["status"] == "DEAD":
            print ("LOST")
        else:
            print("WON")
        print (j["win_rate"])
        print (j["games"])
        print ("Playing again")

if __name__ == "__main__":
    main()
