import re

def loadPlayerGlobalVars():
   mute()
   me.setGlobalVariable("toggleAutoAT", "True")
   me.setGlobalVariable("deckLoadedAndSet", "False") #For nextPhase function to check if a deck is loaded and set before continuing
   me.setGlobalVariable("noDrawFirstTurn", "False")

def chkMultiplayer(args):
    mute()
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False":
        #Prevent red errors from showing up if item is not found in the lists below
        try:
            card = args.cards[0]
            toName = args.toGroups[0].name
            fromName = args.fromGroups[0].name
        except IndexError:
            return
        
        if args.player._id == 2:
            if card.controller == me and card.owner == me:
                if toName != 'Table': #Any group not a Table, reset card to normal
                    card.orientation = Rot0
                elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                    card.orientation = Rot90
        elif args.player._id == 3:
            if card.controller == me and card.owner == me:
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot180
        elif args.player._id == 4:
            if card.controller == me and card.owner == me:
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot270
    
def autoAT(args):
    mute()
    if me.getGlobalVariable("toggleAutoAT") == "True":
        #Prevent red errors from showing up if item is not found in the lists below
        try:
            toName = args.toGroups[0].name
            fromName = args.fromGroups[0].name
            card = args.cards[0]
        except IndexError:
            return
        
        #Just for debugging pos
        #whisper("Card Pos: {}".format(card.position))
        
        type = card.properties["Type"]
        #cardNo = card.properties["Number"] #Only to find cards with special conditions Eg. The Fire of Friendship
        cardCost = card.properties["Cost"]
        cardReqPower = card.properties["PlayRequiredPower"]
        cardReqElement = card.properties["PlayRequiredElement"]
        cardSecondaryReqElement = card.properties["SecondaryPlayRequiredElement"]
        cardTriReqElement = card.properties["TertiaryPlayRequiredElement"]
        cardPower = 0
        priColorReqFailed = False
        secColorReqFailed = False
        triColorReqFailed = False
        playerCounters = me.counters['Actions'].value
        transformCard = False #A check for transformCard
        
        #GUID for Action and Colour Counters
        Action = ("Action", "ec99fdcb-ffea-4658-8e8f-5dc06e93f6fd")
        LoyaltyCounter = ("Loyalty", "a875a876-5ce3-4879-9590-09fc5835b5f3")
        HonestyCounter = ("Honesty", "b5ba06aa-b52f-4b17-b2e1-92302c38c5d7")
        LaughterCounter = ("Laughter", "6b46c706-08e9-44ed-8d0f-c2e478f68cd1")
        MagicCounter = ("Magic", "d970ca6c-0a3d-4def-b0e1-b1e385902a34")
        GenerosityCounter = ("Generosity", "10d7e739-bed0-4cab-93dd-24215bb13948")
        KindnessCounter = ("Kindness", "f04f63b2-52e8-439f-86a2-bff887fab0cd")
        
        Loyalty = 0
        Kindness = 0
        Honesty = 0
        Laughter = 0
        Magic = 0
        Generosity = 0
        
        if type == 'Troublemaker': #setting cost for TMs
            intCardCost = 1
        elif cardCost == '': #For Manes, do not continue with this function
            return
        elif re.search(r'Transform 2', card.Keywords) or re.search(r'Transform 2', card.Text):
            transformCard = True
        else:
            intCardCost = int(card.properties["Cost"])
            
        if card.properties["Element"] != '': #Check if card is a friend
            cardPower = int(card.properties["Power"])
        
        
        if toName == 'Table' and fromName == 'Hand':
            if card.controller == me and card.owner == me:
            
                if cardReqElement != '':
                    #Capturing all face up friend cards on table for comparison
                    allCards = (card for card in table if card.isFaceUp == True and (card.properties["Type"] == 'Friend' or card.properties["Type"] == 'Mane Character' or card.properties["Type"] == 'Mane Character Boosted' or card.properties["Number"] == 'FF115'))
                    for cards in allCards:
                        elementPower =  int(cards.properties["Power"]) + cards.markers[Action]
                        
                        #For Cards with special conditions
                        if cards.properties["Number"] == 'FF115':
                            if cards.markers[LoyaltyCounter] > 0:
                                Loyalty += 2
                            if cards.markers[KindnessCounter] > 0:
                                Kindness += 2
                            if cards.markers[HonestyCounter] > 0:
                                Honesty += 2
                            if cards.markers[LaughterCounter] > 0:
                                Laughter += 2
                            if cards.markers[MagicCounter] > 0:
                                Magic += 2
                            if cards.markers[GenerosityCounter] > 0:
                                Generosity += 2
                        else:
                            #Capture all colours for single, multicolored or tri-colored friend cards and add their powers
                            if cards.properties["Element"] != 'Multicolor':
                                if cards.properties["Element"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                    Loyalty += elementPower
                                if cards.properties["Element"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                    Kindness += elementPower
                                if cards.properties["Element"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                    Honesty += elementPower
                                if cards.properties["Element"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                    Laughter += elementPower
                                if cards.properties["Element"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                    Magic += elementPower
                                if cards.properties["Element"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                    Generosity += elementPower
                            elif cards.properties["TriElement"] == '':
                                if cards.properties["MultiPrimaryElement"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                    Loyalty += elementPower
                                if cards.properties["MultiPrimaryElement"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                    Kindness += elementPower
                                if cards.properties["MultiPrimaryElement"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                    Honesty += elementPower
                                if cards.properties["MultiPrimaryElement"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                    Laughter += elementPower
                                if cards.properties["MultiPrimaryElement"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                    Magic += elementPower
                                if cards.properties["MultiPrimaryElement"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                    Generosity += elementPower
                                
                                if cards.properties["MultiSecondaryElement"] == 'Loyalty':
                                    Loyalty += elementPower
                                if cards.properties["MultiSecondaryElement"] == 'Kindness':
                                    Kindness += elementPower
                                if cards.properties["MultiSecondaryElement"] == 'Honesty':
                                    Honesty += elementPower
                                if cards.properties["MultiSecondaryElement"] == 'Laughter':
                                    Laughter += elementPower
                                if cards.properties["MultiSecondaryElement"] == 'Magic':
                                    Magic += elementPower
                                if cards.properties["MultiSecondaryElement"] == 'Generosity':
                                    Generosity += elementPower
                            else:
                                if cards.properties["TriPrimaryElement"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                    Loyalty += elementPower
                                if cards.properties["TriPrimaryElement"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                    Kindness += elementPower
                                if cards.properties["TriPrimaryElement"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                    Honesty += elementPower
                                if cards.properties["TriPrimaryElement"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                    Laughter += elementPower
                                if cards.properties["TriPrimaryElement"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                    Magic += elementPower
                                if cards.properties["TriPrimaryElement"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                    Generosity += elementPower
                                
                                if cards.properties["TriSecondaryElement"] == 'Loyalty':
                                    Loyalty += elementPower
                                if cards.properties["TriSecondaryElement"] == 'Kindness':
                                    Kindness += elementPower
                                if cards.properties["TriSecondaryElement"] == 'Honesty':
                                    Honesty += elementPower
                                if cards.properties["TriSecondaryElement"] == 'Laughter':
                                    Laughter += elementPower
                                if cards.properties["TriSecondaryElement"] == 'Magic':
                                    Magic += elementPower
                                if cards.properties["TriSecondaryElement"] == 'Generosity':
                                    Generosity += elementPower
                                    
                                if cards.properties["TriElement"] == 'Loyalty':
                                    Loyalty += elementPower
                                if cards.properties["TriElement"] == 'Kindness':
                                    Kindness += elementPower
                                if cards.properties["TriElement"] == 'Honesty':
                                    Honesty += elementPower
                                if cards.properties["TriElement"] == 'Laughter':
                                    Laughter += elementPower
                                if cards.properties["TriElement"] == 'Magic':
                                    Magic += elementPower
                                if cards.properties["TriElement"] == 'Generosity':
                                    Generosity += elementPower
                                
                    #Comparing card to see if it meet color req
                    intCardReqPower = int(card.properties["PlayRequiredPower"])
                    
                    #For primary color req
                    if cardReqElement == 'Loyalty':
                        Loyalty -= cardPower #Remove the newly placed card on Table from the calculation
                        if Loyalty < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Kindness':
                        Kindness -= cardPower
                        if Kindness < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Honesty':
                        Honesty -= cardPower
                        if Honesty < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Laughter':
                        Laughter -= cardPower
                        if Laughter < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Magic':
                        Magic -= cardPower
                        if Magic < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Generosity':
                        Generosity -= cardPower
                        if Generosity < intCardReqPower:
                            priColorReqFailed = True
                    
                    #For secondary color req
                    if cardSecondaryReqElement != '':
                        if cardSecondaryReqElement == 'Loyalty':
                            Loyalty -= cardPower
                            if Loyalty < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Kindness':
                            Kindness -= cardPower
                            if Kindness < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Honesty':
                            Honesty -= cardPower
                            if Honesty < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Laughter':
                            Laughter -= cardPower
                            if Laughter < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Magic':
                            Magic -= cardPower
                            if Magic < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Generosity':
                            Generosity -= cardPower
                            if Generosity < intCardReqPower:
                                secColorReqFailed = True
                                
                    #For tri color req
                    if cardTriReqElement != '':
                        if cardTriReqElement == 'Loyalty':
                            Loyalty -= cardPower
                            if Loyalty < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Kindness':
                            Kindness -= cardPower
                            if Kindness < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Honesty':
                            Honesty -= cardPower
                            if Honesty < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Laughter':
                            Laughter -= cardPower
                            if Laughter < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Magic':
                            Magic -= cardPower
                            if Magic < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Generosity':
                            Generosity -= cardPower
                            if Generosity < intCardReqPower:
                                triColorReqFailed = True
                    
                    #For debugging color req
                    #notify("Honesty: {}, Loyalty: {}, Generosity: {}, Magic: {}, Laughter: {}, Kindness: {}".format(Honesty, Loyalty, Generosity, Magic, Laughter, Kindness))
                    #notify("PriReqFailed: {}, SecReqFailed: {} triColorReqFailed: {}".format(priColorReqFailed, secColorReqFailed, triColorReqFailed))
                    if priColorReqFailed == True or secColorReqFailed == True or triColorReqFailed == True:
                        mute()
                        card.moveTo(me.hand)
                        choice = confirm("You do not have the Color Requirement to play {}. Do you want to continue?".format(card.name))
                        if choice == True:
                            if me.isInverted:
                                card.moveToTable(-28, -120)
                            else:
                                card.moveToTable(-33, 30)
                        else:
                            return
                
                #Check if the card is a Transform card which can reduce a card cost
                if transformCard == True:
                    transformChoice = confirm("Are you using Transform 2 to pay for the card?")
                    
                    if transformChoice == True:
                        intCardCost = 2 #Change the card cost to 2
                    else:
                        intCardCost = int(card.properties["Cost"])

                #Calculate if player has enough AT to pay for the card cost
                checkPayable = playerCounters - intCardCost
                                
                if checkPayable < 0:
                    mute()
                    card.moveTo(me.hand)
                    choice2 = confirm("You do not have enough Action Token(s) to play {}. Do you want to continue?".format(card.name))
                    if choice2 == True:
                        if me.isInverted:
                            card.moveToTable(-28, -120)
                        else:
                            card.moveToTable(-33, 30)
                else:
                    me.counters['Actions'].value = me.counters['Actions'].value - intCardCost
            
def autoRotateDilemma(args):
    mute()
    try:
        toName = args.toGroups[0].name
        fromName = args.fromGroups[0].name
        card = args.cards[0]
    except IndexError:
        return
        
    traits = card.properties["Traits"]
    cardID = card._id
    if getGlobalVariable("PermExhausted") != "Start": #Get a list of cards that is perm exhausted
            permExhaustedList = eval(getGlobalVariable("PermExhausted"))
    else:
        permExhaustedList = []
    
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False":
        if args.player._id == 1:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table': #Any group not a Table, reset card to normal
                    card.orientation = Rot0
                elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                    card.orientation = Rot90
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
        elif args.player._id == 4:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot180
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
        elif args.player._id == 3:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot270
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
    else:
        if card.controller == me and card.owner == me and traits == "Dilemma":
            if toName != 'Table': #Any group not a Table, reset card to normal
                card.orientation = Rot0
            elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                card.orientation = Rot90
                card.filter = "#44ff0000"
                permExhaustedList.append(cardID) #Adds to perm exhausted list
                setGlobalVariable("PermExhausted", str(permExhaustedList))
                
def specialActionsEnterPlay(args):
    mute()
    #Prevent red errors from showing up if item is not found in the lists below
    try:
        toName = args.toGroups[0].name
        fromName = args.fromGroups[0].name
        card = args.cards[0]
    except IndexError:
        return
    
    #Information to retrieve from cards
    cardNo = card.properties["Number"] #To find cards with special conditions

    if toName == 'Table' and fromName == 'Hand' and card.controller == me and card.owner == me:
        #For Zecora, Curative Cache
        if cardNo == "LL41":
            count = 4
            
            #Loop up to 4 times for player to choose up to 4 cards to banish
            while not count <= 0:
                #Placed here to prevent the loop from repeatedly appending cards from hand
                handCardPower, handCardType, handCardName, handCardSubname, cardData, cardChoices = [], [], [], [], [], []
                
                #Get details of all cards in player hand
                for cards in me.hand:
                    handCardPower.append(cards.power)
                    handCardType.append(cards.type)
                    handCardName.append(cards.name)
                    handCardSubname.append(cards.subname)
                    cardData.append(cards)
                
                #Query player and display all cards in hand
                desc = "{}/{} cards left!\n\nChoose up to 4 cards to be banished:".format(count, 4)
                for i in range(0, len(handCardPower)):
                    desc = desc + "\n\n({}) {}: {} - {}".format(handCardPower[i], handCardType[i], handCardName[i], handCardSubname[i])
                    cardChoices.append("{} - {}".format( handCardName[i], handCardSubname[i]))
                cardChoices.append("Cancel")
                choiceNum = askChoice(desc, cardChoices)
                
                # Move card to table and add it to banish list
                if choiceNum != len(cardChoices) and choiceNum != 0:
                    cardToMove = cardData[choiceNum-1]
                    if me.isInverted:
                        cardToMove.moveToTable(-453, -241, True)
                    else:
                        cardToMove.moveToTable(392, 151, True)
                    cardToMove.peek()
                    cardToMove.highlight = "#990000"
                    notify("{} moved a card to the Banish Pile on the table.".format(me))
                elif choiceNum == len(cardChoices): #Checks if the player want to stop
                    if confirm("Are you sure you do not want to banish any more cards?"):
                        break
                    else:
                        count += 1
                else: #Loop again if player tries to close the dialog box
                    count += 1
                
                count -= 1 #End of Loop
            
            notify("{} has finished picking cards to banish.".format(me))
            #Draw cards depending on how many cards were banished
            cardsToDraw = me.deck.top(4 - count)
            for c in cardsToDraw:
                c.moveTo(me.hand)
            notify("{} draw(s) {} cards.".format(me, 4 - count))
            
        else:
            return

def triggerPhaseStop(args):
    #Note for Improvement: Make it track the pause list for each player so the pause list will not clash between players
    #Also there is a visual bug as setStop only removes the yellow square if the active player set the stop, the non active player will still have that square
    mute()
    currentPhaseName, currentPhaseID = currentPhase()
    phaseClickedID = args.id
    phaseClickedName = args.name
    phaseStops = eval(getGlobalVariable("phaseStops"))
    removeStop = False
    activeStops = []
    
    #Prevent pause during phase 0
    if currentPhaseID != 0:
        for stops in phaseStops:
            #Ensures the any "Del" in the list will not be counted
            if "Del" not in stops:
                activeStopsInPhase = re.match(r"{}\.".format(phaseClickedID), stops)
                
                #If re finds any stops matching the clicked phase
                if activeStopsInPhase:
                    activeStops.append(stops) #Create a list of active stops
                    
                    #Only remove all stops if there is 2 stops in the phase
                    if len(activeStops) == 2:
                        removeStop = True
        
        if removeStop == True:
            #Removes all stops in that phase to make it easier to code, might be changed in the future
            num = askChoice("Are you sure you want to remove all pauses for this phase?", ["Yes","No"])
            if num != 1:
                return
            else:
                for stops in activeStops:
                    phaseStops.remove(stops)
                whisper("All pause(s) for {} has been removed!".format(phaseClickedName))
                setStop(phaseClickedID, False)
                setGlobalVariable("phaseStops", str(phaseStops))
        else:
            #Adds stop depending on what phase was clicked
            #Ready Phase
            if phaseClickedID == 1:
                phaseStopList = ["Before player draws card", "After player draws card", "Cancel"]
                choice = askChoice("Which part of the phase do you want to pause?", phaseStopList)
                
                if choice == 1:
                    phaseStops.append("1.1")
                    setGlobalVariable("phaseStops", str(phaseStops))
                elif choice == 2:
                    phaseStops.append("1.2")
                    setGlobalVariable("phaseStops", str(phaseStops))
                else:
                    return
                
                setStop(1, True)
            #Troublemaker Phase
            elif phaseClickedID == 2:
                phaseStopList = ["Before uncovering Troublemaker", "Before ending the phase", "Cancel"]
                choice = askChoice("Which part of the phase do you want to pause?", phaseStopList)
                
                if choice == 1:
                    phaseStops.append("2.1")
                    setGlobalVariable("phaseStops", str(phaseStops))
                elif choice == 2:
                    phaseStops.append("2.2")
                    setGlobalVariable("phaseStops", str(phaseStops))
                else:
                    return
                
                setStop(2, True)
            #Main Phase
            elif phaseClickedID == 3:
                phaseStopList = ["Before any Main Phase Action", "Before ending the phase", "Cancel"]
                choice = askChoice("Which part of the phase do you want to pause?", phaseStopList)
                
                if choice == 1:
                    phaseStops.append("3.1")
                    setGlobalVariable("phaseStops", str(phaseStops))
                elif choice == 2:
                    phaseStops.append("3.2")
                    setGlobalVariable("phaseStops", str(phaseStops))
                else:
                    return
                
                setStop(3, True)
            #Score Phase
            elif phaseClickedID == 4:
                phaseStopList = ["Before confronting problems", "Before ending the phase", "Cancel"]
                choice = askChoice("Which part of the phase do you want to pause?", phaseStopList)
                
                if choice == 1:
                    phaseStops.append("4.1")
                    setGlobalVariable("phaseStops", str(phaseStops))
                elif choice == 2:
                    phaseStops.append("4.2")
                    setGlobalVariable("phaseStops", str(phaseStops))
                else:
                    return
                
                setStop(4, True)
            elif phaseClickedID == 5:
                phaseStopList = ["Before end phase actions", "Cancel"]
                choice = askChoice("Which part of the phase do you want to pause?", phaseStopList)
                
                if choice == 1:
                    phaseStops.append("5.1")
                    setGlobalVariable("phaseStops", str(phaseStops))
                else:
                    return
                
                setStop(5, True)
            else:
                return
            
            whisper("Your pause is now active!")
    else:
        whisper("You cannot set a pause when the game has not started!")