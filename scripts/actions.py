import re
import time

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
#The GUID from markers.o8g
Action = ("Action", "ec99fdcb-ffea-4658-8e8f-5dc06e93f6fd")
Loyalty = ("Loyalty", "a875a876-5ce3-4879-9590-09fc5835b5f3")
Honesty = ("Honesty", "b5ba06aa-b52f-4b17-b2e1-92302c38c5d7")
Laughter = ("Laughter", "6b46c706-08e9-44ed-8d0f-c2e478f68cd1")
Magic = ("Magic", "d970ca6c-0a3d-4def-b0e1-b1e385902a34")
Generosity = ("Generosity", "10d7e739-bed0-4cab-93dd-24215bb13948")
Kindness = ("Kindness", "f04f63b2-52e8-439f-86a2-bff887fab0cd")

GameURL = "http://tinyurl.com/ne3sb8t"
FaceoffColor1 = "#ff0000"
FaceoffColor2 = "#0000ff"
FaceoffColor3 = "#008000"
FaceoffColor4 = "#ffa500"
PumpedColor = "#999999"
ChaosColor = "#fc8eac"
CutieMarkColor = "#ffccff"

#---------------------------------------------------------------------------
# Globals
#---------------------------------------------------------------------------
FaceoffPosition = 0
FaceoffOffset = 0

#---------------------------------------------------------------------------
# Game Setup
#---------------------------------------------------------------------------
def setup(group, x = 0, y = 0):
    mute()
    #Variables
    ManeCheck = 0
    PlayerNo = me._id #Get current player ID
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))

    if not confirm("Setup your side of the table?"): return

    #Table Setup for Villain Challenge
    if getGlobalVariable("VillainChallengeActive") == "True":
        mute()
        for card in me.hand:
            if card.Type != 'Mane Character' and card.Type != 'Mane Character Boosted': 
                card.moveTo(me.Deck)
        
        for card in me.piles['Discard Pile']:
            if card.Type == 'Mane Character': 
                card.moveTo(me.hand)
            elif card.Type == 'Mane Character Boosted': 
                card.moveTo(me.hand)
            else: 
                card.moveTo(me.Deck)
        
        for card in me.piles['Problem Deck']:
            if card.Type == 'Mane Character': 
                card.moveTo(me.hand)
            elif card.Type == 'Mane Character Boosted': 
                card.moveTo(me.hand)
            elif re.search(r'NM', card.Number) or re.search(r'KS', card.Number) or re.search(r'QC', card.Number):
                pass
            else:
                card.moveTo(me.piles['Discard Pile'])
                card.delete()
        
        for card in me.hand: 
            if card.Type == 'Mane Character' or card.Type == 'Mane Character Boosted':
                if me.isInverted:
                    card.moveTo(me.piles['Discard Pile'])
                    card.delete()
                elif villainPlayerId == 1: 
                    if PlayerNo == 2:               
                        card.moveToTable(-33,177)
                    elif PlayerNo == 3:
                        card.moveToTable(-336,177)
                    elif PlayerNo == 4:
                        card.moveToTable(277,177)
                elif villainPlayerId == 2: 
                    if PlayerNo == 1:               
                        card.moveToTable(-33,177)
                    elif PlayerNo == 3:
                        card.moveToTable(-336,177)
                    elif PlayerNo == 4:
                        card.moveToTable(277,177)
                elif villainPlayerId == 3: 
                    if PlayerNo == 1:               
                        card.moveToTable(-33,177)
                    elif PlayerNo == 2:
                        card.moveToTable(-336,177)
                    elif PlayerNo == 4:
                        card.moveToTable(277,177)
                elif villainPlayerId == 4: 
                    if PlayerNo == 1:               
                        card.moveToTable(-33,177)
                    elif PlayerNo == 2:
                        card.moveToTable(-336,177)
                    elif PlayerNo == 3:
                        card.moveToTable(277,177)
                
                if card.Type == 'Mane Character Boosted':
                    card.alternate = ''

                ManeCheck = ManeCheck + 1
            else:
                notify("{}: Invalid Setup! Must not have any other cards in hand but your Mane Character".format(me))
                return

        if me.isInverted:
            pass
        elif ManeCheck != 1:
            notify("{}: Invalid Setup! Must have exactly one copy of a Mane Character in your deck!".format(me))
            return  

        shuffle(me.Deck)
        
        if len(me.Deck) == 0: return
        if len(me.Deck) < 6:
            drawAmount = len(group)
        
        for card in me.Deck.top(6):
            card.moveTo(me.hand)

        me.counters['Points'].value = 0
        me.counters['Actions'].value = 0

        notify("{} draws their opening hand of {} cards.".format(me, 6))    
        notify("{} has set up their side of the table.".format(me))

        me.setGlobalVariable("deckLoadedAndSet", "True")
        return
        #END OF VILLAIN CHALLENGE SETUP
    else:
        #Table setup for normal games
        for card in me.hand:
            if card.Type == 'Problem': 
                card.moveTo(me.piles['Problem Deck'])
            elif card.Type != 'Mane Character' and card.Type != 'Mane Character Boosted': 
                card.moveTo(me.Deck)
    
        for card in me.piles['Discard Pile']:
            if card.Type == 'Mane Character': 
                card.moveTo(me.hand)
            elif card.Type == 'Mane Character Boosted': 
                card.moveTo(me.hand)
            elif card.Type == 'Problem': 
                card.moveTo(me.piles['Problem Deck'])
            else: 
                card.moveTo(me.Deck)
        
        for card in me.piles['Banished Pile']: 
            if card.Type == 'Mane Character': 
                card.moveTo(me.hand)
            elif card.Type == 'Mane Character Boosted': 
                card.moveTo(me.hand)
            elif card.Type == 'Problem': 
                card.moveTo(me.piles['Problem Deck'])
            else: 
                card.moveTo(me.Deck)

        myCards = (card for card in table
                if card.owner == me)

        for card in myCards:
            if card.Type == 'Mane Character': 
                card.moveTo(me.hand)
            elif card.Type == 'Mane Character Boosted': 
                card.moveTo(me.hand)
            elif card.Type == 'Problem': 
                card.moveTo(me.piles['Problem Deck'])
            else: 
                card.moveTo(me.Deck)

    #Starting Problem Selection
    for c in me.piles['Problem Deck']:
        c.peek() #Reveal the cards to python

    rnd(1,2)  #allow the peeked card's properties to load
    
    StartProblems = (card for card in me.piles['Problem Deck'] if re.search(r'Starting Problem', card.Keywords))
                
    buttons = []  #This list stores all the card objects for manipulations.
    OldProblem = ""
    for c in StartProblems:
        if c.Name != OldProblem:
            buttons.append(c)
            OldProblem = c.Name
    
    desc = "Select a Starting Problem:"
    num = askChoice(desc, [c.Name + ": (" + c.ProblemPlayerElement1Power + " " + c.ProblemPlayerElement1 + " / " + c.ProblemPlayerElement2Power + " " + c.ProblemPlayerElement2 + ")" for c in buttons], customButtons = ["Cancel Setup"])
    if num > 0:
        SelectedStart = buttons.pop(num - 1)       
    else: 
        return

    #Starting Problem Position
    if (len(players) == 3 or len(players) == 4): #Starting Problem pos for multiplayer
        if PlayerNo == 1:
            SelectedStart.moveToTable(107,36)
        elif PlayerNo == 2:
            SelectedStart.moveToTable(-262,56)
            SelectedStart.orientation ^= Rot90
        elif PlayerNo == 3:
            SelectedStart.moveToTable(-197,-127)
            SelectedStart.orientation ^= Rot180
        elif PlayerNo == 4:
            SelectedStart.moveToTable(166,-167)
            SelectedStart.orientation ^= Rot270
    else:
        #Starting Problem pos for 2 player games
        if me.isInverted:
            SelectedStart.moveToTable(-215,-57)
        else:               
            SelectedStart.moveToTable(130,-53)
        
    update()
            
    for c in me.piles['Problem Deck']:  #This removes the peek status
        c.isFaceUp = True
        c.isFaceUp = False
    
    shuffle(me.piles['Problem Deck'])
    
    update()
    
    #Mane Position
    for card in me.hand: 
        if card.Type == 'Mane Character' or card.Type == 'Mane Character Boosted':
            if (len(players) == 3 or len(players) == 4): #Mane pos for multiplayer
                if PlayerNo == 1:
                    card.moveToTable(-33,191)
                elif PlayerNo == 2:
                    card.moveToTable(-461,-53)
                    card.orientation ^= Rot90
                elif PlayerNo == 3:
                    card.moveToTable(-33,-272)
                    card.orientation ^= Rot180
                elif PlayerNo == 4:
                    card.moveToTable(374,-53)
                    card.orientation ^= Rot270
                ManeCheck = ManeCheck + 1
            else:
                #Mane pos for 2 player games
                if me.isInverted:
                    card.moveToTable(-28,-220)
                else:               
                    card.moveToTable(-33,130)
            
            if card.Type == 'Mane Character Boosted':
                card.alternate = ''
            
            ManeCheck = ManeCheck + 1
        else:
            notify("{}: Invalid Setup! Must not have any other cards in hand but your Mane Character".format(me))
            return

    if ManeCheck != 1:
        notify("{}: Invalid Setup! Must have exactly one copy of a Mane Character in your deck!".format(me))
        return

    shuffle(me.Deck)
    
    if len(me.Deck) == 0: return
    if len(me.Deck) < 6:
        drawAmount = len(group)
    
    for card in me.Deck.top(6):
        card.moveTo(me.hand)

    me.counters['Points'].value = 0
    me.counters['Actions'].value = 0

    notify("{} draws their opening hand of {} cards.".format(me, 6))    
    notify("{} has set up their side of the table.".format(me))

    me.setGlobalVariable("deckLoadedAndSet", "True")

#Setup for VC
def activateVC(group, x = 0, y = 0):
    mute()
    villainList = ["Nightmare Moon", "King Sombra", "Queen Chrysalis"]
    count = 0
    playerId = me._id
    villainPicked = False
    #VCplayerID = eval(getGlobalVariable("VCplayerID"))
    
    if not confirm("Start Villian Challenge?\nNOTE: This action will reset the game!"): return
    resetGame()
    ## Checks to see if player has met proper conditions for VC
    if len(players) != 4:
        whisper("There is not enough players to start Villian Challenge! Please ensure you have 4 players and try again.")
        return
    
    while count <= 3: #Find which player is the villain and look for any additional villains
        if players[count].isInverted == True:
            if villainPicked == True:
                whisper("There are more than one player on the 'B' side of the table! Please quit the game and ensure that there is only one player on the 'B' side in the lobby.")
                return
            else:
                setGlobalVariable("villainPlayerId", players[count]._id) #Remove?
                villainPlayerId = eval(getGlobalVariable("villainPlayerId")) #Remove?

                # VCplayerID.insert(0, players[count]._id)
                # villainPlayerId = VCplayerID[0]
                # setGlobalVariable("VCplayerID", str(VCplayerID))

                villainPlayerName = players[count].name
                villainPicked = True
        count += 1
    if villainPicked == False:
        whisper("There is no player on the 'B' side of the table OR table is One-Sided! Please quit the game and ensure that there is one player on the 'B' side in the lobby AND table is Two-Sided.")
        return
    ##END OF CHECKS, let the challenge begin!
    
    ##Initialization of global variables
    #All possible scenario for each player to identify the villain player and Main player (If player 1 is villain, pick player 2 ELSE just use player 1)
    if playerId == 1: 
        if villainPlayerId == 2:
            villainPlayerNo = 1
            mainPlayerNo = 0
        elif villainPlayerId == 3:
            villainPlayerNo = 2
            mainPlayerNo = 0
        elif villainPlayerId == 4:
            villainPlayerNo = 3
            mainPlayerNo = 0
        else:
            villainPlayerNo = 0
            mainPlayerNo = 1
    elif playerId == 2:
        if villainPlayerId == 1:
            villainPlayerNo = 1
            mainPlayerNo = 0
        elif villainPlayerId == 3:
            villainPlayerNo = 2
            mainPlayerNo = 1
        elif villainPlayerId == 4:
            villainPlayerNo = 3
            mainPlayerNo = 1
        else:
            villainPlayerNo = 0
            mainPlayerNo = 1
    elif playerId == 3:
        if villainPlayerId == 1:
            villainPlayerNo = 1
            mainPlayerNo = 2
        elif villainPlayerId == 2:
            villainPlayerNo = 2
            mainPlayerNo = 1
        elif villainPlayerId == 4:
            villainPlayerNo = 3
            mainPlayerNo = 1
        else:
            villainPlayerNo = 0
            mainPlayerNo = 1
    elif playerId == 4:
        if villainPlayerId == 1:
            villainPlayerNo = 1
            mainPlayerNo = 2
        elif villainPlayerId == 2:
            villainPlayerNo = 2
            mainPlayerNo = 1
        elif villainPlayerId == 3:
            villainPlayerNo = 3
            mainPlayerNo = 1
        else:
            villainPlayerNo = 0
            mainPlayerNo = 1
    
    if villainPlayerId == 1:#Picking which player to hold the elements, it is counted by playerID, should be player 1 else player 2 (Might not be needed)
        setGlobalVariable("mainPlayerId", "2")

        #VCplayerID.insert(1, 2)
        #setGlobalVariable("VCplayerID", str(VCplayerID))
    else:
        setGlobalVariable("mainPlayerId", "1")

        #VCplayerID.insert(1, 1)
        #setGlobalVariable("VCplayerID", str(VCplayerID))
    update()
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    #mainPlayerId = VCplayerID[1]
    ##END of Initialization
    
    notify("{} starts a Villain Challenge game.".format(me))
    notify("{} is chosen to be the Villain player.".format(villainPlayerName))
    setGlobalVariable("VillainChallengeActive", "True")
    
    villainChoice = askChoice("Pick a villain:", villainList)
    setGlobalVariable("villainChoice", villainChoice)
    
    if getGlobalVariable("villainChoice") == "1": #Nightmare Moon
        notify("Nightmare Moon is chosen to be the Villain.")
        
        table.create('21dcdb56-d043-4d08-8c9d-d7f999fc3ca5', 411, 12, quantity = 1, persist = True)
        table.create('c2d92f0b-b014-4543-90ae-149a92d6590b', 411, 12, quantity = 1, persist = True)
        table.create('6d0ee873-dd4d-4aee-8b0a-9539baa2ef2f', 411, 12, quantity = 2, persist = True)
        table.create('8416ef0e-59cd-427d-a939-acca556a7e42', 411, 12, quantity = 1, persist = True)
        table.create('249f0582-cb51-4191-94d5-0a06003b27a1', 411, 12, quantity = 2, persist = True)
        table.create('281db57f-ab1b-4337-b901-f0b6e82bc949', 411, 12, quantity = 1, persist = True)
        villainProbCards = (card for card in table if re.search(r'NM', card.Number))
        
        originalVGrpControllerProb = players[villainPlayerNo].piles['Problem Deck'].controller
        
        players[villainPlayerNo].piles['Problem Deck'].controller = me
        for card in villainProbCards:
            card.controller = me
            update()
            card.moveTo(players[villainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalVGrpControllerProb
        shuffle(players[villainPlayerNo].piles['Problem Deck'])
        players[villainPlayerNo].piles['Problem Deck'].controller = originalVGrpControllerProb
        
        rnd(1,2)
        update()
        
        villainEndProbCard = table.create('f065b9bd-b95d-4239-914b-47a54833d12b', 411, 12, quantity = 1, persist = True)
        players[villainPlayerNo].piles['Problem Deck'].controller = me
        update()
        villainEndProbCard.controller = me
        update()
        villainEndProbCard.moveToBottom(players[villainPlayerNo].piles['Problem Deck'])
        update()
        villainEndProbCard.controller = originalVGrpControllerProb
        update()
        players[villainPlayerNo].piles['Problem Deck'].controller = originalVGrpControllerProb
        
        table.create('8357131c-0082-4c14-bee6-6dc58219035b', 411, 12, quantity = 1, persist = True)
        table.create('825da05c-215f-41db-b13f-eaed527976ce', 411, 27, quantity = 1, persist = True)
        table.create('97082419-23f7-4213-b7b1-0c10bc8dac9e', 411, 42, quantity = 1, persist = True)
        table.create('59a1ab57-69fa-4a04-b895-6d830ef54eb7', 411, 57, quantity = 1, persist = True)
        table.create('498b2033-cbdd-4a2a-86a2-d14eecf8709a', 411, 72, quantity = 1, persist = True)
        table.create('a220527e-3f0f-480e-a59f-6506fa3bfaf8', 411, 87, quantity = 1, persist = True)
        elementCards = (card for card in table if re.search(r'CN', card.Number))
        
        rnd(1,2)
        update()
        
        table.create('77b105e2-a1c3-4add-9124-7f44b5097caa', 411, 12, quantity = 2, persist = True)
        table.create('9db64954-25be-4689-a849-d4ffb1dd6d6d', 411, 12, quantity = 1, persist = True)
        table.create('97ff6fb4-d7c5-4604-9542-47eddf2a9066', 411, 12, quantity = 1, persist = True)
        table.create('3e8df7e8-8ded-4192-9d57-d3cc0ea9a519', 411, 12, quantity = 1, persist = True)
        table.create('4c6d9ef6-7ed8-48c3-a37e-a689d1cc1648', 411, 12, quantity = 1, persist = True)
        table.create('e80d0ce7-34dd-4ec8-a57b-56c13de54889', 411, 12, quantity = 1, persist = True)
        table.create('247b7b21-60d0-4b67-8b04-7047642c0134', 411, 12, quantity = 1, persist = True)
        table.create('959437c6-8899-479c-a784-53ff4ec6e897', 411, 12, quantity = 1, persist = True)
        challengerProbCards = (card for card in table if re.search(r'NM', card.Number))

        originalGrpControllerBanish = players[mainPlayerNo].piles['Banished Pile'].controller
        originalCGrpControllerProb = players[mainPlayerNo].piles['Problem Deck'].controller
        
        mainPlayerName = players[mainPlayerNo].name
        notify("{} is chosen to be the Main player.".format(mainPlayerName))
        
        players[mainPlayerNo].piles['Banished Pile'].controller = me
        for card in elementCards:
            card.controller = me
            update()
            card.moveTo(players[mainPlayerNo].piles['Banished Pile'])
            update()
            card.controller = originalGrpControllerBanish
        players[mainPlayerNo].piles['Banished Pile'].controller = originalGrpControllerBanish
        
        rnd(1,2)
        update()
        
        players[mainPlayerNo].piles['Problem Deck'].controller = me
        for card in challengerProbCards:
            card.controller = me
            update()
            card.moveTo(players[mainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalCGrpControllerProb
        shuffle(players[mainPlayerNo].piles['Problem Deck'])
        players[mainPlayerNo].piles['Problem Deck'].controller = originalCGrpControllerProb
        
        
        #At the end to prevent challenger prob from counting these cards on the table
        challengerCard = table.create('0901c499-21b0-4863-9857-03f7f57a9efc', -167, 177, quantity = 1, persist = True)
        challengerStartProbCard = table.create('1b08836a-ac8a-4cff-92bc-cc52decfdb8c', 130, -53, quantity = 1, persist = True)
        challengerCard.controller = players[mainPlayerNo]
        challengerStartProbCard.controller = players[mainPlayerNo]
        
        
        villainManeCard = table.create('dfe40d93-60f2-4f02-a2a2-9c8909c5e9df', -33, -268, quantity = 1, persist = True)
        villainStartProbCard = table.create('725ebc53-1252-468a-9f86-4da0d536e22c', -215, -57, quantity = 1, persist = True)
        villainManeCard.controller = players[villainPlayerNo]
        villainStartProbCard.controller = players[villainPlayerNo]
        
    elif getGlobalVariable("villainChoice") == "2": #King Sombra
        notify("King Sombra is chosen to be the Villain.")
        
        table.create('d682a5c3-c072-4704-a060-fe7e11652a41', 411, 12, quantity = 1, persist = True)
        table.create('78d0eb88-0c78-4bd6-992b-c9516bcbd151', 411, 12, quantity = 1, persist = True)
        table.create('2c2a7997-910a-4417-becc-cc12bd09b07d', 411, 12, quantity = 1, persist = True)
        table.create('5840c7e5-ba8d-480a-8f5f-ca9a18867528', 411, 12, quantity = 1, persist = True)
        table.create('207a5ffa-431c-4034-a1aa-e815de9b1b52', 411, 12, quantity = 1, persist = True)
        table.create('0e65d3aa-a0eb-481a-8391-4ebcb9f1dcab', 411, 12, quantity = 1, persist = True)
        table.create('740d9208-78fb-4663-8535-2b6c7d40c945', 411, 12, quantity = 1, persist = True)
        table.create('b00cebd5-f662-451b-91f2-8b7dfc0ef6f0', 411, 12, quantity = 1, persist = True)
        table.create('783501ab-7cd2-4373-9758-b7c65b733a79', 411, 12, quantity = 1, persist = True)
        table.create('765ccb71-ce96-46cb-af7b-60c25b141dc5', 411, 12, quantity = 1, persist = True)
        villainProbCards = (card for card in table if re.search(r'KS', card.Number))
        
        originalVGrpControllerProb = players[villainPlayerNo].piles['Problem Deck'].controller
        
        players[villainPlayerNo].piles['Problem Deck'].controller = me
        for card in villainProbCards:
            card.controller = me
            update()
            card.moveTo(players[villainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalVGrpControllerProb
        update()
        players[villainPlayerNo].piles['Problem Deck'].controller = originalVGrpControllerProb
        
        rnd(1,2)
        update()
        
        table.create('2a6a3b88-ce2b-438a-a007-8b7bced567a5', 411, 12, quantity = 1, persist = True)
        table.create('386b2f5c-33f3-4e09-8839-b082ede6db1b', 411, 12, quantity = 1, persist = True)
        table.create('17953ea5-4976-4657-a6e5-19524c1a1872', 411, 12, quantity = 1, persist = True)
        table.create('da83672d-7344-449d-b6aa-484022bfdcce', 411, 12, quantity = 1, persist = True)
        table.create('32e2e9c0-97dd-470f-88bd-9984fa47482f', 411, 12, quantity = 1, persist = True)
        table.create('7ec25817-f4bc-4dbe-9934-399735c6056f', 411, 12, quantity = 1, persist = True)
        table.create('8b3e4b09-145c-41b9-9cfe-465ba5616e44', 411, 12, quantity = 1, persist = True)
        table.create('3a7fd1e9-15f0-4ebd-9444-383752f2efee', 411, 12, quantity = 1, persist = True)
        table.create('7aeca61c-aab8-4d74-bc89-bdbca03bd50f', 411, 12, quantity = 1, persist = True)
        table.create('3c702f47-9420-4449-98f3-ea22a209cc5e', 411, 12, quantity = 1, persist = True)
        challengerProbCards = (card for card in table if re.search(r'KS', card.Number))
        
        originalCGrpControllerProb = players[mainPlayerNo].piles['Problem Deck'].controller
        
        mainPlayerName = players[mainPlayerNo].name
        notify("{} is chosen to be the Main player.".format(mainPlayerName))
        
        players[mainPlayerNo].piles['Problem Deck'].controller = me
        for card in challengerProbCards:
            card.controller = me
            update()
            card.moveTo(players[mainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalCGrpControllerProb
        players[mainPlayerNo].piles['Problem Deck'].controller = originalCGrpControllerProb
        
        challengerStartProbCard = table.create('c8c2e682-4c90-4ff0-a027-8c3dc6224330', 130, -53, quantity = 1, persist = True)
        challengerStartProbCard.controller = players[mainPlayerNo]
        
        villainStartProbCard = table.create('67cc321a-fc8d-4842-959b-4c4e4b52ed1d', -215, -57, quantity = 1, persist = True)
        villainManeCard = table.create('1395b658-c0d7-4a2d-91ea-8337e94d80a8', -33, -268, quantity = 1, persist = True)
        villainCard = table.create('ea8871b9-8f90-450e-ad09-a7dc2c55d641', -167, -268, quantity = 1, persist = True)
        villainStartProbCard.controller = players[villainPlayerNo]
        villainManeCard.controller = players[villainPlayerNo]
        villainCard.controller = players[villainPlayerNo]
        
    elif getGlobalVariable("villainChoice") == "3": #Queen Chrysalis
        notify("Queen Chrysalis is chosen to be the Villain.")
        
        table.create('afb81798-ce55-4608-9f5b-cbeb20f52ab1', 411, 12, quantity = 2, persist = True)
        table.create('265f3136-09dc-4ee2-aa69-b4848539668d', 411, 12, quantity = 2, persist = True)
        table.create('87ec85b6-e92f-49f2-87bf-1b0555a717ce', 411, 12, quantity = 2, persist = True)
        table.create('c064a952-5e92-414e-acfa-7c0aa0f80e31', 411, 12, quantity = 2, persist = True)
        table.create('77ab8a99-392c-4011-9771-4c83829c1b2f', 411, 12, quantity = 1, persist = True)
        villainProbCards = (card for card in table if re.search(r'QC', card.Number))
        
        originalVGrpControllerProb = players[villainPlayerNo].piles['Problem Deck'].controller
        
        players[villainPlayerNo].piles['Problem Deck'].controller = me
        for card in villainProbCards:
            card.controller = me
            update()
            card.moveTo(players[villainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalVGrpControllerProb
        shuffle(players[villainPlayerNo].piles['Problem Deck'])
        players[villainPlayerNo].piles['Problem Deck'].controller = originalVGrpControllerProb
        
        rnd(1,2)
        update()
        
        table.create('1ccba76c-9aaf-40ac-b55d-6085ac789f94', 411, 12, quantity = 2, persist = True)
        table.create('98e8f98f-9628-4f9b-a1e7-369b3974f2b0', 411, 12, quantity = 2, persist = True)
        table.create('f85aa7fd-5e7b-4e3f-809b-436f4aac4a62', 411, 12, quantity = 2, persist = True)
        table.create('a35c9ae8-ca69-47d4-a45c-aecabdeb3e42', 411, 12, quantity = 2, persist = True)
        table.create('08bd8c99-94fb-41ba-a6db-419ee20b943a', 411, 12, quantity = 1, persist = True)
        challengerProbCards = (card for card in table if re.search(r'QC', card.Number))

        originalCGrpControllerProb = players[mainPlayerNo].piles['Problem Deck'].controller
        
        mainPlayerName = players[mainPlayerNo].name
        notify("{} is chosen to be the Main player.".format(mainPlayerName))
        
        players[mainPlayerNo].piles['Problem Deck'].controller = me
        for card in challengerProbCards:
            card.controller = me
            update()
            card.moveTo(players[mainPlayerNo].piles['Problem Deck'])
            update()
            card.controller = originalCGrpControllerProb
        shuffle(players[mainPlayerNo].piles['Problem Deck'])
        players[mainPlayerNo].piles['Problem Deck'].controller = originalCGrpControllerProb
        
        #Creation of cards that will stay on table
        #At the end to prevent problem piles from counting these cards on the table and adding them into the pile
        challengerCard = table.create('8ad6ef37-3af1-4c10-8982-bd0c48b195a7', -167, 177, quantity = 1, persist = True)
        challengerStartProbCard = table.create('1318c3f4-8a57-404a-ace5-435f52099274', 130, -53, quantity = 1, persist = True)
        challengerCard.controller = players[mainPlayerNo]
        challengerStartProbCard.controller = players[mainPlayerNo]
        
        villainManeCard = table.create('dd893c2b-3b8e-4df5-a08c-0bb30d5e6a96', -33, -268, quantity = 1, persist = True)
        villainCard = table.create('1e4ad546-c444-4007-833d-b57e6958fe0c', -167, -268, quantity = 1, persist = True)
        villainCard1 = table.create('7f66e526-6639-4e85-8a36-812c906616df', -247, -268, quantity = 1, persist = True)
        villainCard2 = table.create('139cb1eb-28c4-44f6-9a4e-70d1ef550522', -287, -268, quantity = 1, persist = True)
        villainCard3 = table.create('c5a68c3a-6de3-4703-8a69-46a526fa38bc', -327, -268, quantity = 1, persist = True)
        villainStartProbCard = table.create('a6f82c51-7bab-427c-877e-4877ec4bc6cf', -215, -57, quantity = 1, persist = True)
        villainManeCard.controller = players[villainPlayerNo]
        villainCard.controller = players[villainPlayerNo]
        villainCard1.controller = players[villainPlayerNo]
        villainCard2.controller = players[villainPlayerNo]
        villainCard3.controller = players[villainPlayerNo]
        villainStartProbCard.controller = players[villainPlayerNo]
        
        notify("\nFor Villain:\nRemember to look through each Challenger's deck one at a time and pick one Friend from each Challenger deck for your Seemingly Innocent Pony resource card.\n\nFor Challengers:\nRemember to decide on one Harmony-legal Event for your Defensive Spell resource card.\n")
        
    whisper("Please ignore the moving errors above if any. The cards are already in the correct position, just that it's too fast for the game to track.")

#---------------------------------------------------------------------------
# Game Phases
#---------------------------------------------------------------------------

#First Turn - Only runs on the first turn of the game to properly set the Phase System
def firstTurn(group, x = 0, y = 0):
    mute()
    PlayerNo = me._id
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))

    num = askChoice("Are you first player?", ["Yes","No"])
    if num != 1:
        return
    else:
        #Set active for VC - Do you need others to setActive? Why not wait until Main/Villain player to reach here and set them as active?
        if getGlobalVariable("VillainChallengeActive") == "True":
            if getGlobalVariable("PlayerStartDone") == "Start": #If var running for the first time, create list
                PlayerStartDone = []
            else:
                PlayerStartDone = eval(getGlobalVariable("PlayerStartDone"))

            if PlayerNo != mainPlayerId and PlayerNo != villainPlayerId: #If you are the other challengers, set active for main player
                if mainPlayerId == 1:
                    players[1].setActive()
                elif mainPlayerId == 2:
                    if PlayerNo == 1:
                        players[1].setActive()
                    else:
                        players[2].setActive()
            else:
                if me.isInverted:
                    setGlobalVariable("VillainTurn", "True")
                me.setActive() #NOTE: Only active player can change phase, so challengers might not be able to do anything but to follow along
        else:
            me.setActive() #Set active for non VC games

        #Check if it is a 2 player game
        if (len(players) == 2):
            me.setGlobalVariable("noDrawFirstTurn", "True") #This person doesn't draw a card as it is the first turn of the game
        elif getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("VillainTurn") == "False": #Challengers do not draw a card if they go first?? I'm not sure
            me.setGlobalVariable("noDrawFirstTurn", "True")
            PlayerStartDone.append(PlayerNo) #This part was at the end of the phase originally, check if this placement affects anything
            setGlobalVariable("PlayerStartDone", str(PlayerStartDone))
            update()
        else:
            me.setGlobalVariable("noDrawFirstTurn", "False") #Defining the Variable for any other game
        setPhase(1) #Go to ready phase

#Ready Phase
def turnReady(group, phaseLoopCounter, x = 0, y = 0):
    mute()
    maxPoints = 0
    maxName = ""
    addActions = 0
    PlayerNo = me._id
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    phaseStops = eval(getGlobalVariable("phaseStops"))

    #Setup for tracking Challengers turn progress for VC 
    # if getGlobalVariable("VillainChallengeActive") == "True":
        # if getGlobalVariable("PlayerStartDone") == "Start": #If var running for the first time, create list
            # PlayerStartDone = []
        # else:
            # PlayerStartDone = eval(getGlobalVariable("PlayerStartDone"))
        
        # if getGlobalVariable("PlayerDone") != "Start": #Check if any challenger is done with their turns
            # PlayerDone = eval(getGlobalVariable("PlayerDone"))
            
            # for player in range(len(PlayerDone)): #If player is in the PlayerDone list, stop player from starting turn again
                # if PlayerDone[player] == PlayerNo:
                    # whisper("Please wait for the other challenger(s) to finish their turn.")
                    # return
    # else:
        # pass

    #Check if player is active before continuing
    if getGlobalVariable("VillainChallengeActive") == "True":
        if me.isActive:
            if me.isInverted:
                setGlobalVariable("VillainTurn", "True")
            else:
                if getGlobalVariable("VillainTurn") == "True": #If it is villain turn and main is still active, stop main
                    whisper("You can't start the turn when it isn't your turn.")
                    return
                else:
                    notify("*Challenger {} starts his/her turn*".format(me)) #REMOVE? See how it works out
        else:
            if getGlobalVariable("VillainTurn") == "False" and PlayerNo != villainPlayerId:
                notify("*Challenger {} starts his/her turn*".format(me))
            elif getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId: #Somehow if inactive player set villain to active, it doesn't work
                notify("*The villain, {} begins Turn {}*".format(me, turnNumber()))
            else:
                whisper("You can't start the turn when it isn't your turn.")
                return
    else:
        #For non VC games
        if me.isActive:
            pass
        else:
            whisper("You can't start the turn when it isn't your turn.")
            return
    
    #First Loop
    if phaseLoopCounter == 1:
        if "Del 1.1" not in phaseStops and "Del 1.2" not in phaseStops and "Stop" not in phaseStops:
            #Meticulous triggers here? Idk if it is before or after Ready and gain AT
            meticulous1Count = sum(1 for card in table if card.isFaceUp == True and card.controller == me and (re.search(r'Meticulous 1', card.Keywords) or re.search(r'Meticulous 1', card.Text)))
            meticulous2Count = sum(1 for card in table if card.isFaceUp == True and card.controller == me and (re.search(r'Meticulous 2', card.Keywords) or re.search(r'Meticulous 2', card.Text)))
            totalMeticulousCount = meticulous1Count + meticulous2Count
            
            if totalMeticulousCount > 0:
                #Check if auto Meticulous is on or off. If off, whisper to player instead
                if me.getGlobalVariable("toggleAutoMeticulous") == "True":
                    num = askChoice("You have {} Meticulous card(s) on the table. Use Meticulous?".format(totalMeticulousCount), ["Yes","No"])
                    if num == 1:
                        meticulous(group, x, y)
                else:
                    whisper("You have {} Meticulous card(s) on the table that you can use.".format(totalMeticulousCount))

            #Ready all cards
            readyAll(group, x, y)
            notify("{} readies all their cards.".format(me))
            setGlobalVariable("phaseLoopCounter", "2")
            return
    
    #Second Loop
    if phaseLoopCounter == 2:
        if "Del 1.1" not in phaseStops and "Del 1.2" not in phaseStops and "Stop" not in phaseStops:
            #Gain AT
            for person in players:
                if maxPoints < person.counters['Points'].value:
                    maxPoints = person.counters['Points'].value
                    maxName = person.name

            if getGlobalVariable("VillainChallengeActive") == "True":
                if getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId:
                    if maxPoints < 2:
                        addActions = 4
                    elif maxPoints < 6:
                        addActions = 5
                    elif maxPoints < 11:
                        addActions = 6
                    else:
                        addActions = 7
                    
                    if maxPoints == 0:
                        notify("*Nobody has Points yet. Being the villain, {} adds {} Action Tokens.*".format(me,addActions))
                    else:   
                        notify("*{} has {} Points. Being the villain, {} adds {} Action Tokens.*".format(maxName,maxPoints,me,addActions))
                else:
                    if maxPoints < 2:
                        addActions = 2
                    elif maxPoints < 6:
                        addActions = 3
                    elif maxPoints < 11:
                        addActions = 4
                    else:
                        addActions = 5
                
                    if maxPoints == 0:
                        notify("*Nobody has Points yet. Challenger {} adds {} Action Tokens.*".format(me,addActions))
                    else:   
                        notify("*{} has {} Points. Challenger {} adds {} Action Tokens.*".format(maxName,maxPoints,me,addActions))
            else:
                if maxPoints < 2:
                    addActions = 2
                elif maxPoints < 6:
                    addActions = 3
                elif maxPoints < 11:
                    addActions = 4
                else:
                    addActions = 5
                
                if maxPoints == 0:
                    notify("*Nobody has Points yet. {} adds {} Action Tokens.*".format(me,addActions))
                else:   
                    notify("*{} has {} Points. {} adds {} Action Tokens.*".format(maxName,maxPoints,me,addActions))
            
            me.counters['Actions'].value = me.counters['Actions'].value + addActions
            setGlobalVariable("phaseLoopCounter", "3")
            return

    if phaseLoopCounter == 3:
        #PPP Stop - Before drawing cards
        if "1.1" not in phaseStops and "Del 1.2" not in phaseStops and "Stop" not in phaseStops: #Check if there is a stop here and if .2 has been triggered before

            #Draw cards
            if me.getGlobalVariable("noDrawFirstTurn") == "True":
                notify("{} does not draw on the game's first turn.".format(me))
                me.setGlobalVariable("noDrawFirstTurn", "False")
            else:
                draw(me.deck)
            setGlobalVariable("phaseLoopCounter", "4")
            return

        elif "Del 1.2" in phaseStops: #If .2 has triggered, skip this portion
            pass
        else:
            notify("*A player has set a pause before drawing card! Once done, {} please press Spacebar to continue*".format(me))
            phaseStops.append("Stop")
            setGlobalVariable("phaseStops", str(phaseStops))
            return

    if phaseLoopCounter == 4:
        #PPP Stop - Before phase ends
        if "1.2" in phaseStops:
            phaseStops.append("Stop")
            notify("*A player has set a pause before ending this phase! Once done, {} please press Spacebar to continue*".format(me))
            return
        else:
            #Remove Del if any but loop the phase again if it is Del .1
            if "Del 1.1" in phaseStops:
                phaseStops.remove("Del 1.1")
                setGlobalVariable("phaseStops", str(phaseStops))
                return
            if "Del 1.2" in phaseStops:
                phaseStops.remove("Del 1.2")
                setGlobalVariable("phaseStops", str(phaseStops))

            setGlobalVariable("phaseLoopCounter", "1")
            setPhase(2)

#Troublemaker Phase
def turnTroublemaker(group, phaseLoopCounter, x = 0, y = 0):
    mute()
    PlayerNo = me._id
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    phaseStops = eval(getGlobalVariable("phaseStops"))

    #Check if player is active before continuing
    if me.isActive:
        if getGlobalVariable("VillainChallengeActive") == "True": #See if needed?
            if PlayerNo == villainPlayerId:
                notify("*The villain, {} begins their Troublemaker Phase.*".format(me))
            else:
                notify("*Challenger {} begins their Troublemaker Phase.*".format(me))
        else:
            pass
    else:
        #For the other challengers to get through the phase
        if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("VillainTurn") == "False": #See if needed?
            notify("*Challenger {} begins their Troublemaker Phase.*".format(me))
        elif getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId: #Somehow if inactive player set villain to active, it doesn't work
            notify("*The villain, {} begins their Troublemaker Phase.*".format(me))
        else:
            whisper("You can't set the phase when it isn't your turn.")
            return

    if phaseLoopCounter == 1:
        #PPP Stop - Before TM uncover
        if "2.1" not in phaseStops and "Del 2.2" not in phaseStops and "Stop" not in phaseStops: #Check if there is a stop here and if .2 has been triggered before

            #Uncover Troublemakers
            clearFaceoff(group, x, y)
            peekAll(group, x, y)        
            rnd(1,2)
            
            troublemakerCount = sum(1 for card in table if card.controller == me and card.Type == 'Troublemaker' and card.isFaceUp == False)
            if troublemakerCount > 0:
                setGlobalVariable("phaseLoopCounter", "2") #Trigger a loop if there is facedown TM 
                num = askChoice("You have facedown Troublemakers. Flip them up?", ["Yes","No"])
                if num == 1:
                    troublemakers = (card for card in table if card.controller == me and card.Type == 'Troublemaker' and card.isFaceUp == False)
                    for c in troublemakers:
                        c.isFaceUp = True
        elif "Del 2.2" in phaseStops: #If .2 has triggered, skip this portion
            pass #Might be redundant due to phaseLoopCounter
        else:
            notify("*A player has set a pause before uncovering Troublemaker(s)! Once done, {} please press Spacebar to continue*".format(me))
            return

    #PPP Stop - Before phase ends
    if "2.2" in phaseStops:
        phaseStops.append("Stop")
        notify("*A player has set a pause before ending this phase! Once done, {} please press Spacebar to continue*".format(me))
        return
    else:
        #Remove Del if any but loop the phase again if it is Del .1
        if "Del 2.1" in phaseStops:
            phaseStops.remove("Del 2.1")
            setGlobalVariable("phaseStops", str(phaseStops))
        if "Del 2.2" in phaseStops:
            phaseStops.remove("Del 2.2")
            setGlobalVariable("phaseStops", str(phaseStops))
            
        #Check for any TM cards covered and loop the phase again if any
        if getGlobalVariable("phaseLoopCounter") == "2":
            setGlobalVariable("phaseLoopCounter", "3") #Tell it not to go into uncover portion again
            return
        else:
            setGlobalVariable("phaseLoopCounter", "1") #Reset phaseLoopCounter for other phases
            setPhase(3)

#Main Phase
def turnMain(group, phaseLoopCounter, x = 0, y = 0):
    mute()
    PlayerNo = me._id
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    phaseStops = eval(getGlobalVariable("phaseStops"))

    #Check if player is active before continuing
    if me.isActive:
        if getGlobalVariable("VillainChallengeActive") == "True": #See if needed?
            if PlayerNo == villainPlayerId:
                notify("*The villain, {} begins their Main Phase.*".format(me))
            else:
                notify("*Challenger {} begins their Main Phase.*".format(me))
        else:
            pass
    else:
        #For the other challengers to get through the phase
        if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("VillainTurn") == "False": #See if needed?
            notify("*Challenger {} begins their Main Phase.*".format(me))
        elif getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId: #Somehow if inactive player set villain to active, it doesn't work
            notify("*The villain, {} begins their Main Phase.*".format(me))
        else:
            whisper("You can't set the phase when it isn't your turn.")
            return

    if phaseLoopCounter == 1:
        #PPP Stop - Before any main phase action
        if "3.1" not in phaseStops and "Del 3.2" not in phaseStops and "Stop" not in phaseStops: #Check if there is a stop here and if .2 has been triggered before

            #Inspired triggers here?
            inspiredCount = sum(1 for card in table if card.controller == me and card.isFaceUp == True and (re.search(r'Inspired', card.Keywords) or re.search(r'Inspired', card.Text)))
            if inspiredCount > 0:
                setGlobalVariable("phaseLoopCounter", "2") #Trigger a loop if there is inspired
                num = askChoice("You have {} Inspired on the table. Use Inspired?".format(inspiredCount), ["Yes","No"])
                if num == 1:
                    inspired(group, x, y)
        elif "Del 3.2" in phaseStops: #If .2 has triggered, skip this portion
            pass
        else:
            phaseStops.append("Stop")
            notify("*A player has set a pause before any Main Phase action! Once done, {} please press Spacebar to continue*".format(me))
            return

    #PPP Stop - Before phase ends
    if "3.2" in phaseStops:
        #setGlobalVariable("phaseLoop", "False") #Disable phaseLoop so that it cannot let the player bypass the stop
        phaseStops.append("Stop")
        notify("*A player has set a pause before ending this phase! Once done, {} please press Spacebar to continue*".format(me))
        return
    else:
        #Remove Del if any but loop the phase again if it is Del .1
        if "Del 3.1" in phaseStops:
            phaseStops.remove("Del 3.1")
            setGlobalVariable("phaseStops", str(phaseStops))
        if "Del 3.2" in phaseStops:
            phaseStops.remove("Del 3.2")
            setGlobalVariable("phaseStops", str(phaseStops))
            
        #Check for any inspired cards is on the table and loop the phase again if any
        if getGlobalVariable("phaseLoopCounter") == "2":
            setGlobalVariable("phaseLoopCounter", "3") #Tell it not to go into the inspired portion again
            return
        else:
            setGlobalVariable("phaseLoopCounter", "1") #Reset phaseLoopCounter for other phases
            setPhase(4)

#Score Phase
def turnScore(group, x = 0, y = 0):
    mute()
    PlayerNo = me._id
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    phaseStops = eval(getGlobalVariable("phaseStops"))

    #Check if player is active before continuing
    if me.isActive:
        if getGlobalVariable("VillainChallengeActive") == "True": #See if needed?
            if PlayerNo == villainPlayerId:
                notify("*The villain, {} begins their Score Phase.*".format(me))
            else:
                notify("*Challenger {} begins their Score Phase.*".format(me))
        else:
            pass
    else:
        #For the other challengers to get through the phase
        if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("VillainTurn") == "False": #See if needed?
            notify("*Challenger {} begins their Score Phase.*".format(me))
        elif getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId: #Somehow if inactive player set villain to active, it doesn't work
            notify("*The villain, {} begins their Score Phase.*".format(me))
        else:
            whisper("You can't set the phase when it isn't your turn.")
            return

    #PPP Stop - Before confronting problems
    if "4.1" in phaseStops:
        notify("*A player has set a pause before confronting problems! Once done, {} please press Spacebar to continue*".format(me))
        return

    #Check if confronting Problem A
    #PPP
    #Check if confronting Problem B
    #PPP
    #Problem Faceoff
    #PPP
    #Replace Solved Problems

    #PPP Stop - Before phase ends
    if "4.2" in phaseStops:
        notify("*A player has set a pause before ending this phase! Once done, {} please press Spacebar to continue*".format(me))
        return
    else:
        if "Del 4.1" in phaseStops:
            phaseStops.remove("Del 4.1")
            setGlobalVariable("phaseStops", str(phaseStops))
            return
        if "Del 4.2" in phaseStops:
            phaseStops.remove("Del 4.2")
            setGlobalVariable("phaseStops", str(phaseStops))

        setPhase(5)

#End Phase
def turnEnd(group, x = 0, y = 0):
    mute()
    PlayerNo = me._id #Get current player ID
    mainPlayerId = eval(getGlobalVariable("mainPlayerId"))
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    phaseStops = eval(getGlobalVariable("phaseStops"))
    CountforHandLimitCards = None
    handCount = 0
    handLimit = 8
    
    #Check if player is active before continuing
    if me.isActive:
        if getGlobalVariable("VillainChallengeActive") == "True": #See if needed?
            if PlayerNo == villainPlayerId:
                notify("*The villain, {} begins their End Phase.*".format(me))
            else:
                notify("*Challenger {} begins their End Phase.*".format(me))
        else:
            pass
    else:
        #For the other challengers to get through the phase
        if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("VillainTurn") == "False": #See if needed?
            notify("*Challenger {} begins their End Phase.*".format(me))
        elif getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId: #Somehow if inactive player set villain to active, it doesn't work
            notify("*The villain, {} begins their End Phase.*".format(me))
        else:
            whisper("You can't set the phase when it isn't your turn.")
            return

    #PPP Stop - Before phase starts
    if "5.1" in phaseStops:
        notify("*A player has set a pause before starting this phase! Once done, {} please press Spacebar to continue*".format(me))
        return
    else:
        #Remove Del if any but loop the phase again if it is Del .1
        if "Del 5.1" in phaseStops:
            phaseStops.remove("Del 5.1")
            setGlobalVariable("phaseStops", str(phaseStops))

        if not confirm("End your turn?"): return

    #Discard cards down to Max Hand Size
    choiceList = ['Ok', 'Let me just end my turn!'] #Check hand limit
    
    #Check for cards that increase hand limit
    CountforHandLimitCards = sum(1 for card in table if card.controller == me and card.isFaceUp == True and card.model == "c476a8dc-7543-4c07-8273-37a216452c69")
    if CountforHandLimitCards != None and CountforHandLimitCards != 0:
        handLimit = 10

    for card in me.hand:
        handCount += 1
    discardCount = handCount - handLimit
    if handCount > handLimit:
        choice = askChoice("You have more than {} cards in your hand. Please discard {} card(s) to continue!".format(handLimit, discardCount), choiceList)
        if choice == 1:
            return

    #Retire down to Home Limit
    #End of Turn effects end
    
    #Maybe set this part to run when VC is being played

    if getGlobalVariable("PlayerDone") == "Start": #If var running for the first time, create list
        PlayerDone = []
    else:
        PlayerDone = eval(getGlobalVariable("PlayerDone"))

    #All possible scenario for each player to identify the villain player and main player
    if getGlobalVariable("VillainChallengeActive") == "True":
        PlayerDone = eval(getGlobalVariable("PlayerDone"))
        if PlayerNo == 1: 
            if villainPlayerId == 2:
                villainPlayerNo = 1
                mainPlayerNo = 0
            elif villainPlayerId == 3:
                villainPlayerNo = 2
                mainPlayerNo = 0
            elif villainPlayerId == 4:
                villainPlayerNo = 3
                mainPlayerNo = 0
            else:
                villainPlayerNo = 0
                mainPlayerNo = 1
        elif PlayerNo == 2:
            if villainPlayerId == 1:
                villainPlayerNo = 1
                mainPlayerNo = 0
            elif villainPlayerId == 3:
                villainPlayerNo = 2
                mainPlayerNo = 1
            elif villainPlayerId == 4:
                villainPlayerNo = 3
                mainPlayerNo = 1
            else:
                villainPlayerNo = 0
                mainPlayerNo = 1
        elif PlayerNo == 3:
            if villainPlayerId == 1:
                villainPlayerNo = 1
                mainPlayerNo = 2
            elif villainPlayerId == 2:
                villainPlayerNo = 2
                mainPlayerNo = 1
            elif villainPlayerId == 4:
                villainPlayerNo = 3
                mainPlayerNo = 1
            else:
                villainPlayerNo = 0
                mainPlayerNo = 1
        elif PlayerNo == 4:
            if villainPlayerId == 1:
                villainPlayerNo = 1
                mainPlayerNo = 2
            elif villainPlayerId == 2:
                villainPlayerNo = 2
                mainPlayerNo = 1
            elif villainPlayerId == 3:
                villainPlayerNo = 3
                mainPlayerNo = 1
            else:
                villainPlayerNo = 0
                mainPlayerNo = 1

    if me.isActive:
        clearFaceoff(group, x, y)
        playSound('endturn')

        if len(players) == 1:
            players[0].setActive()
            notify("*{} is done. It is now {}'s turn.*".format(me, players[0]))
        elif len(players) == 2:
            players[1].setActive()
            #nextTurn(players[1], False)
            notify("*{} is done. It is now {}'s turn.*".format(me, players[1]))
        elif len(players) == 3 and getGlobalVariable("VillainChallengeActive") == "False":
            if PlayerNo == 3: #If last player, go back to first player
                players[1].setActive()
                notify("*{} is done. It is now {}'s turn.*".format(me, players[1]))
                return
            players[PlayerNo].setActive()
            notify("*{} is done. It is now {}'s turn.*".format(me, players[PlayerNo]))
        elif len(players) == 4 and getGlobalVariable("VillainChallengeActive") == "False":
            if PlayerNo == 4: #If last player, go back to first player
                players[1].setActive()
                notify("*{} is done. It is now {}'s turn.*".format(me, players[1]))
                return
            players[PlayerNo].setActive()
            notify("*{} is done. It is now {}'s turn.*".format(me, players[PlayerNo]))
        elif getGlobalVariable("VillainChallengeActive") == "True": #Ending turns for Villain Challenge
            if me.isInverted:
                players[mainPlayerNo].setActive()
                notify("*The villain, {} is done. It is now the Challengers' turn.*".format(me))
                setGlobalVariable("VillainTurn", "False")
            else:
                if len(PlayerDone) != 2: #Ensuring that active player being the last to end the turn
                    whisper("Unfortunately, being the active player, you must wait for the other challengers to end their turn. Please end your turn again after your fellow challengers are done.")
                    return
                else:
                    PlayerDone.append(PlayerNo)
                    setGlobalVariable("PlayerDone", str(PlayerDone))
                    update()
                    notify("*Challenger {} is done.*".format(me))
        setGlobalVariable("phaseStop", "True")
        setPhase(1) #Reset the phase for the new active player
    else:
        if getGlobalVariable("VillainChallengeActive") == "True":
            if getGlobalVariable("VillainTurn") == "False" and PlayerNo != villainPlayerId: #For all non-active challengers
                clearFaceoff(group, x, y)
                playSound('endturn')
                PlayerDone.append(PlayerNo)
                setGlobalVariable("PlayerDone", str(PlayerDone))
                update()
                notify("*Challenger {} is done.*".format(me))
            else:
                whisper("You can't pass the turn when it isn't your turn.") #For all non active players not in VC 

    if getGlobalVariable("VillainChallengeActive") == "True": #Check if last challenger is done
        if len(PlayerDone) == 3:
            players[villainPlayerNo].setActive()
            setGlobalVariable("phaseStop", "True")
            setPhase(1) #Reset the phase for the new active player
            villainName = players[villainPlayerNo].name
            notify("*The Challengers are done. It is now the villain, {}'s turn*".format(villainName))
            setGlobalVariable("PlayerDone", "Start") #Resetting the list
            setGlobalVariable("VillainTurn", "True")

#Phase passer
def nextPhase(group, x = 0, y = 0):
    update()
    currentPhaseName, currentPhaseID = currentPhase()

    if currentPhaseID == 0:
        if me.getGlobalVariable("deckLoadedAndSet") == "True": #Checks if player has loaded a deck and set it up
            #Turn Number 0 for Tab, Turn Number 1 for Green Arrow
            if turnNumber() == 0 or turnNumber() == 1:
                firstTurn(group, x, y)
            else:
                deckLoaded = eval(me.getGlobalVariable("deckLoadedAndSet"))
                noDraw = eval(getGlobalVariable("noDrawFirstTurn"))
                phaseLoopCounter = eval(getGlobalVariable("phaseLoopCounter"))
                phaseStops = eval(getGlobalVariable("phaseStops"))
                VCactive = eval(getGlobalVariable("VillainChallengeActive"))
                autoAT = eval(getGlobalVariable("toggleAutoAT"))
                
                whisper("Error with Phase 0! Report this message with the following text to GameMasterLuna ASAP!") #A debugging note to see if players do end up here
                whisper("Current ID: {}\nDeck Loaded: {}\nNo Draw First Turn: {}\nPhase Loop: {}\nPhase Stops: {}\nVC Active: {}\nAuto AT: {}\nTurn Number: {}".format(currentPhaseID, deckLoaded, noDraw, phaseLoopCounter, phaseStops, VCactive, autoAT, turnNumber()))
                return
        else:
            whisper("*Please load a deck and press F12 to setup your table to continue*")
    elif currentPhaseID == 1:
        turnReady(group, eval(getGlobalVariable("phaseLoopCounter")), x, y)
    elif currentPhaseID == 2:
        turnTroublemaker(group, eval(getGlobalVariable("phaseLoopCounter")), x, y)
    elif currentPhaseID == 3:
        turnMain(group, eval(getGlobalVariable("phaseLoopCounter")), x, y)
    elif currentPhaseID == 4:
        turnScore(group, x, y)
    elif currentPhaseID == 5:
        turnEnd(group, x, y)
    else:
        deckLoaded = eval(me.getGlobalVariable("deckLoadedAndSet"))
        noDraw = eval(getGlobalVariable("noDrawFirstTurn"))
        phaseLoopCounter = eval(getGlobalVariable("phaseLoopCounter"))
        phaseStops = eval(getGlobalVariable("phaseStops"))
        VCactive = eval(getGlobalVariable("VillainChallengeActive"))
        autoAT = eval(getGlobalVariable("toggleAutoAT"))
        
        whisper("Phase is not within 0-5! Report this message with the following text to GameMasterLuna ASAP!\n") #A debugging note to see if players do end up here
        whisper("Current ID: {}\nDeck Loaded: {}\nNo Draw First Turn: {}\nPhase Loop: {}\nPhase Stops: {}\nVC Active: {}\nAuto AT: {}\nTurn Number: {}".format(currentPhaseID, deckLoaded, noDraw, phaseLoopCounter, phaseStops, VCactive, autoAT, turnNumber()))
        return

#Phase Stop Remover
def removeStop(group, x = 0, y = 0):
    mute()
    currentPhaseName, currentPhaseID = currentPhase()
    phaseStops = eval(getGlobalVariable("phaseStops"))

    if me.isActive: #Checks if the player removing the stop is the active turn player
        if "{}.1".format(currentPhaseID) in phaseStops: #Check if there is a .1 stop in current phase
            phaseStops.remove("{}.1".format(currentPhaseID))
            phaseStops.append("Del {}.1".format(currentPhaseID))
            phaseStops[:] = (value for value in phaseStops if value != "Stop")
            notify("*The game is now unpaused! Press Tab to continue with the phase*")
        elif "{}.2".format(currentPhaseID) in phaseStops: #Check if there is a .2 stop in current phase
            phaseStops.remove("{}.2".format(currentPhaseID))
            phaseStops.append("Del {}.2".format(currentPhaseID))
            phaseStops[:] = (value for value in phaseStops if value != "Stop")
            notify("*The game is now unpaused! Press Tab when you are ready to go to the next phase*")
        else:
            return

        setGlobalVariable("phaseStops", str(phaseStops))
        setStop(currentPhaseID, False)
    else:
        whisper("Only the active turn player can unpause the game!")

    ##Guide for this stop system
    #Each phase has 2 stops defined as .1 or .2
    #The phase number will define the number in front of the "."  Eg. Phase 1 is 1.1 and 1.2 respectively
    #The "Del" suffix will been given to the stop once a player removes a stop
    #This is to let the program know that the stop is done and the player is triggering the same phase again
    #So the program will not run any actions it has done before  Eg. In TM phase, 2.2 is done, "Del 2.2" will tell uncover TM not to trigger again
    #For "Del *.1", it is to tell the program not to end the phase if player is triggering the same phase again after removing stop
    #This allows actions that have not triggered to be completed without the program jumping into the next phase immediately
    #For "Stop", it is only used in Ready Phase as to prevent actions before the first stop from triggering if a stop is active in the phase

#---------------------------------------------------------------------------
# Table Actions
#---------------------------------------------------------------------------
def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))
        
def sixSided(group, x = 0, y = 0):
    mute()
    n = rnd(1,6)
    notify("{} rolls a {} on a 6-sided die.".format(me, n))

def xSided(group, x = 0, y = 0):
    mute()
    x = askInteger("Roll a die with how many sides?", 20)
    if x < 1:
        return
    
    n = rnd(1,x)
    notify("{} rolls a {} on a {}-sided die.".format(me, n, x))

def gainPoint(group, x = 0, y = 0):
    me.counters['Points'].value = me.counters['Points'].value + 1

def losePoint(group, x = 0, y = 0):
    me.counters['Points'].value = max(0, me.counters['Points'].value - 1)

def spendAction(group, x = 0, y = 0):
    if me.counters['Actions'].value == 0:
        whisper("You do not have an Action Token to spend.")
        return
    me.counters['Actions'].value = me.counters['Actions'].value - 1
    
def increaseAction(group, x = 0, y = 0):
    me.counters['Actions'].value = me.counters['Actions'].value + 1

def peekAll(group, x = 0, y = 0):
    faceDownCards = (card for card in table if card.controller == me and card.isFaceUp == False)
    for c in faceDownCards:
        c.peek()

def clearFaceoff(group, x = 0, y = 0):
    mute()
    global FaceoffPosition
    global FaceoffOffset
    
    FaceoffPosition = 0
    FaceoffOffset = 0
    
    FaceoffCards = (card for card in table if card.highlight == FaceoffColor1 or card.highlight == FaceoffColor2 or card.highlight == FaceoffColor3 or card.highlight == FaceoffColor4 or card.highlight == ChaosColor)
    
    count = 0
    for card in FaceoffCards:
        if card.owner == me:
            card.moveToBottom(card.owner.Deck)
            count += 1
    
    if count > 0:
        notify("Faceoff Cards have been put on the bottom of {}'s deck.".format(me))

def readyAll(group, x = 0, y = 0): 
    mute()
    PlayerNo = me._id
    
    if getGlobalVariable("PermExhausted") != "Start": #Get a list of cards that is perm exhausted
        permExhaustedList = eval(getGlobalVariable("PermExhausted"))
    else:
            permExhaustedList = []
    
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False": #Setting orientation for multiplayer
        if getGlobalVariable("Exhausted") == "Start": #If no cards exhausted, return esp at start of game
            return
        else:
            exhaustedList = eval(getGlobalVariable("Exhausted"))
        myCards = []
            
        for card in table:
            if card.controller == me and card.owner == me:
                if card.isFaceUp:
                    currentCard = card._id #To compare with exhausted list
                    for c in range(len(exhaustedList)): #Checks if card is in the Exhausted list, if so card is being readied
                        permCard = False
                        
                        for c in range(len(permExhaustedList)): #Checks if card is in the PermExhausted list
                            if permExhaustedList[c] == currentCard:
                                permCard = True
                    
                        if exhaustedList[c] == currentCard and permCard == False:
                            exhaustedList.remove(currentCard)
                            card.orientation ^= Rot90
                            card.highlight = None
                            card.filter = None
                            notify("{} readies all their cards.".format(me))
                            setGlobalVariable("Exhausted", str(exhaustedList))
                            break
    else:
        if getGlobalVariable("VillainChallengeActive") == "True": #Remove card.owner as some VC cards owner are different from controller
            myCards = (card for card in table
                    if card.controller == me
                    and card.orientation == Rot90)
        else:
            myCards = (card for card in table
                        if card.controller == me
                        and card.owner == me
                        and card.orientation == Rot90)

        for card in myCards:
            currentCard = card._id
            permCard = False
            
            for c in range(len(permExhaustedList)): #Checks if card is in the PermExhausted list
                if permExhaustedList[c] == currentCard:
                    permCard = True
                    
            if card.isFaceUp and permCard == False:
                card.orientation &= ~Rot90
                card.highlight = None
                card.filter = None
                notify("{} readies all their cards.".format(me))

#Token System
def addToken(group, x = 0, y = 0):
    mute()
    
    elementChoiceList = ['Loyalty', 'Kindness', 'Honesty', 'Laughter', 'Magic', 'Generosity', 'Changeling', 'Seashell', 'Crystal Friend']
    elementChoice = askChoice("Pick a choice for your token:", elementChoiceList)
    
    if 1 <= elementChoice <= 8:
        count = askInteger("Create how many tokens? (Up to 10 tokens only)", 1)
        if count <= 10 and count != None:
            if elementChoice == 1:
                if me.isInverted:
                    table.create('2f529241-9056-4765-a925-eb6c9270df43', -28, -120, quantity = count, persist = False)
                else:
                    table.create('2f529241-9056-4765-a925-eb6c9270df43', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Loyalty token(s) onto the table.".format(me,count))
                
            elif elementChoice == 2:
                if me.isInverted:
                    table.create('b7747802-1231-426d-8edb-d8f6ebcc9af0', -28, -120, quantity = count, persist = False)
                else:
                    table.create('b7747802-1231-426d-8edb-d8f6ebcc9af0', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Kindness token(s) onto the table.".format(me,count))
                
            elif elementChoice == 3:
                if me.isInverted:
                    table.create('92fe2323-2cb1-4f7e-a252-548a1b3b739d', -28, -120, quantity = count, persist = False)
                else:
                    table.create('92fe2323-2cb1-4f7e-a252-548a1b3b739d', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Honesty token(s) onto the table.".format(me,count))
                
            elif elementChoice == 4:
                if me.isInverted:
                    table.create('a6a1fda0-9172-4f49-9aca-4709422c6493', -28, -120, quantity = count, persist = False)
                else:
                    table.create('a6a1fda0-9172-4f49-9aca-4709422c6493', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Laughter token(s) onto the table.".format(me,count))
                
            elif elementChoice == 5:
                if me.isInverted:
                    table.create('1f72b17d-6051-4115-8ce4-0574acedc9e1', -28, -120, quantity = count, persist = False)
                else:
                    table.create('1f72b17d-6051-4115-8ce4-0574acedc9e1', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Magic token(s) onto the table.".format(me,count))
            
            elif elementChoice == 6:
                if me.isInverted:
                    table.create('6d00d6dd-9b24-4938-9eb6-e412f64827d1', -28, -120, quantity = count, persist = False)
                else:
                    table.create('6d00d6dd-9b24-4938-9eb6-e412f64827d1', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Generosity token(s) onto the table.".format(me,count))
            elif elementChoice == 7:
                if me.isInverted:
                    table.create('034ac26f-1fc3-448c-b7b0-a61cc6e41f69', -28, -120, quantity = count, persist = False)
                else:
                    table.create('034ac26f-1fc3-448c-b7b0-a61cc6e41f69', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Changeling token(s) onto the table.".format(me,count))
            elif elementChoice == 8:
                if me.isInverted:
                    table.create('d69e44ce-a527-4088-b8a8-0b59d70fffde', -28, -120, quantity = count, persist = False)
                else:
                    table.create('d69e44ce-a527-4088-b8a8-0b59d70fffde', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Seashell Friend token(s) onto the table.".format(me,count))
            elif elementChoice == 9:
                if me.isInverted:
                    table.create('15340acd-d3a9-464a-9f14-18ca15e27a27', -28, -120, quantity = count, persist = False)
                else:
                    table.create('15340acd-d3a9-464a-9f14-18ca15e27a27', -33, 30, quantity = count, persist = False)
            
                notify("{} adds {} Crystal Friend token(s) onto the table.".format(me,count))
        elif count == None:
            return
        else:
            whisper("You can't create more than 10 tokens at one time.")
            return
    else:
        return

def scoop(group, x = 0, y = 0):
    mute()
    
    if not confirm("Scoop your side of the table?"): return
    
    for c in me.hand: 
        if not c.Type == "Mane Character":
            c.moveTo(me.Deck)           
    for c in me.piles['Discard Pile']: c.moveTo(me.Deck)
    for c in me.piles['Banished Pile']: c.moveTo(me.Deck)

    myCards = (card for card in table
            if card.owner == me)

    for card in myCards:
        if card.Type == "Mane Character": 
            card.moveTo(me.hand)
        elif card.Type == "Problem": 
            card.moveTo(me.piles['Problem Deck'])
        else: 
            card.moveTo(me.Deck)
    
    notify("{} scoops their side of the table.".format(me))

# NOTE: Reserved for future use when the devs allow multiple boards on the table
# def playmat(group, x = 0, y = 0):
    # mute()
    # #Just wanted to replace Default option with None so it will be more clear to the user. Note that the Default playmat is transparent
    # playmatList = ['None']
    # playmatList.extend(table.boards)
    # playmatList.remove('Default')
    # playmatList = [x for x in playmatList if not 'Inverted' in x] #Remove all elements with the word "Inverted"
    # playmatChoice = askChoice("Pick a playmat: ", playmatList)
    
    # if playmatChoice == 1:
        # table.board = 'Default'
    # elif playmatChoice == 2:
        # if me.isInverted:
            # table.board = 'Playmat 1 Inverted'
        # else:
            # table.board = 'Playmat 1'
    # elif playmatChoice == 3:
        # if me.isInverted:
            # table.board = 'Playmat 2 Inverted'
        # else:
            # table.board = 'Playmat 2'
    # else:
        # return

#---------------------------------------------------------------------------
# Card actions
#---------------------------------------------------------------------------
def exhaust(card, x = 0, y = 0):
    mute()
    PlayerNo = me._id

    if card.Type == "Problem":
        if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("villainChoice") == "2":
            buttonList = ['Won', 'Lost', 'Cancel']
            choice = askChoice("Did you win or lose the Problem Faceoff at your Problem?", buttonList)
            if choice != 3:
                setGlobalVariable("KSChoice", choice)
                replaceProblem(card, x, y)
        else:
            if confirm("Replace Problem?"):
                replaceProblem(card, x, y)    
    else:
        currentCard = card._id
        
        if getGlobalVariable("PermExhausted") != "Start": #Get a list of cards that is perm exhausted
            permExhaustedList = eval(getGlobalVariable("PermExhausted"))
        else:
            permExhaustedList = []
    
        if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False": #This method for multiplayer only, might lag game
            if getGlobalVariable("Exhausted") == "Start": #If var running for the first time, create list
                exhaustedList = []
            else:
                exhaustedList = eval(getGlobalVariable("Exhausted"))
            
            card.orientation ^= Rot90
            
            for c in range(len(exhaustedList)): #Checks if card is in the Exhausted list, if so card is being readied
                if exhaustedList[c] == currentCard:
                    for c in range(len(permExhaustedList)): #Checks if card is in the Perm Exhausted list
                        if permExhaustedList[c] == currentCard: 
                            permExhaustedList.remove(currentCard)
                            setGlobalVariable("PermExhausted", str(permExhaustedList))
                    
                    exhaustedList.remove(currentCard)
                    permExhaustedList.remove(currentCard)
                    card.filter = None
                    notify('{} readies {}.'.format(me, card))
                    setGlobalVariable("Exhausted", str(exhaustedList))
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
                    return
            
            exhaustedList.append(currentCard) #Adds to exhausted list
            notify('{} exhausts {}.'.format(me, card))
            setGlobalVariable("Exhausted", str(exhaustedList))
            #specialActions(card)
        else:
            card.orientation ^= Rot90
            if card.orientation & Rot90 == Rot90:
                notify('{} exhausts {}.'.format(me, card))
                #specialActions(card) #Exhaust doesn't take in group :/
            else:
                for c in range(len(permExhaustedList)): #Checks if card is in the Perm Exhausted list
                    if permExhaustedList[c] == currentCard: 
                        permExhaustedList.remove(currentCard)
                        setGlobalVariable("PermExhausted", str(permExhaustedList))
                card.filter = None
                notify('{} readies {}.'.format(me, card))

def permExhaust(card, x = 0, y = 0):
    mute()

    if getGlobalVariable("PermExhausted") == "Start": #If var running for the first time, create list
        permExhaustedList = []
    else:
        permExhaustedList = eval(getGlobalVariable("PermExhausted"))
        
    currentCard = card._id
    card.orientation ^= Rot90
    
    for c in range(len(permExhaustedList)): #Checks if card is in the PermExhausted list, if so card is being readied
        if permExhaustedList[c] == currentCard: 
            permExhaustedList.remove(currentCard)
            card.filter = None
            notify('{} readies {}.'.format(me, card))
            setGlobalVariable("PermExhausted", str(permExhaustedList))
            return
    
    permExhaustedList.append(currentCard) #Adds to PermExhausted list
    card.filter = "#44ff0000"
    notify('{} permanently exhausts {}.'.format(me, card))
    setGlobalVariable("PermExhausted", str(permExhaustedList))

def replaceProblem(card, x = 0, y = 0):
    mute()
    card.isFaceUp = False #Flip card down
    card.moveTo(me.piles['Problem Deck'], 0) #Move to top of Problem deck
    oldName = card.Name
    PlayerNo = me._id
    
    if getGlobalVariable("VillainChallengeActive") == "True" and getGlobalVariable("KSChoice") == "2":
        
        newProblem = me.piles['Problem Deck'][10]
        if me.isInverted:
            newProblem.moveToTable(-215,-57)
        else:               
            newProblem.moveToTable(130,-53)
        notify("{} moves {} to the top of their Problem Deck and Replaces it with {} from the bottom of their Problem Deck.".format(me,oldName,newProblem.Name))
        return
        
    card.moveToBottom(me.piles['Problem Deck'])
    
    newProblem = me.piles['Problem Deck'][0]
    
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False": #Starting Problem pos for multiplayer
        if PlayerNo == 1:
            newProblem.moveToTable(107,36)
        elif PlayerNo == 2:
            newProblem.moveToTable(-262,56)
            newProblem.orientation ^= Rot90
        elif PlayerNo == 3:
            newProblem.moveToTable(-197,-127)
            newProblem.orientation ^= Rot180
        elif PlayerNo == 4:
            newProblem.moveToTable(166,-167)
            newProblem.orientation ^= Rot270
    else:
        if me.isInverted:
            newProblem.moveToTable(-215,-57)
        else:               
            newProblem.moveToTable(130,-53)
    notify("{} moves {} to the bottom of their Problem Deck and Replaces it with {}".format(me,oldName,newProblem.Name))

def flipcard(card, x = 0, y = 0):
    mute()
    #position = card.position #TEMP, REMOVE THIS
    if card.alternate == 'Mane Character Boosted':
        card.alternate = ''
        notify("{} flips {}.".format(me, card))
        return
    else:
        #The card models are the 3 resource cards from QC villain challenge
        if card.Type == 'Mane Character' or card.model == '7f66e526-6639-4e85-8a36-812c906616df' or card.model == '139cb1eb-28c4-44f6-9a4e-70d1ef550522' or card.model == 'c5a68c3a-6de3-4703-8a69-46a526fa38bc':
            card.alternate = 'Mane Character Boosted'
            notify("{} flips {}.".format(me, card))
            return
    
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def markPumped(card, x = 0, y = 0):
    mute()
    
    if card.highlight == PumpedColor:
        card.highlight = None
        notify("{} Unflags {} as a pump card.".format(me, card))
    else:
        card.highlight = PumpedColor
        card.sendToBack()
        notify("{} Flags {} as a pump card.".format(me, card))

def markCutieMark(card, x = 0, y = 0):
    mute()
    
    if card.highlight == CutieMarkColor:
        card.highlight = None
        notify("{} Unflags {} as a cutie marked card.".format(me, card))
    else:
        card.highlight = CutieMarkColor
        notify("{} Flags {} as a cutie marked card.".format(me, card))

def duplicate(card, x = 0, y = 0):
    mute()
    
    cardGUID = card.model
    cardName = card.name
    count = askInteger("Create how many copies? (Up to 10 copies only)", 1)

    if count <= 10 and count != None:
        if me.isInverted:
            dupCard = table.create(cardGUID, -28, -120, quantity = count, persist = False)
        else:
            dupCard = table.create(cardGUID, -33, 30, quantity = count, persist = False)
        
        #Gives a TypeError for using List if there is only 1 card in the list, that's is why the "If" is there
        if count == 1:
            dupCard.filter = "#4400ff00"
        else:
            for card in dupCard:
                card.filter = "#4400ff00"
        notify("{} adds {} copy/copies of {} onto the table.".format(me,count,cardName))

def addAction(card, x = 0, y = 0):
    mute()
    notify("{} adds an Action Marker to {}.".format(me, card))
    card.markers[Action] += 1
        
def subAction(card, x = 0, y = 0):
    mute()
    notify("{} subtracts an Action Marker from {}.".format(me, card))
    card.markers[Action] -= 1

#Color Marker System
def addBlue(card, x = 0, y = 0):
    mute()
    if card.markers[Loyalty] < 1:
        card.markers[Loyalty] += 1
        notify("{} adds the colour of Loyalty to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Loyalty!".format(card))

def addOrange(card, x = 0, y = 0):
    mute()
    if card.markers[Honesty] < 1:
        card.markers[Honesty] += 1
        notify("{} adds the colour of Honesty to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Honesty!".format(card))

def addPink(card, x = 0, y = 0):
    mute()
    if card.markers[Laughter] < 1:
        card.markers[Laughter] += 1
        notify("{} adds the colour of Laughter to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Laughter!".format(card))
    
def addPurple(card, x = 0, y = 0):
    mute()
    if card.markers[Magic] < 1:
        card.markers[Magic] += 1
        notify("{} adds the colour of Magic to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Magic!".format(card))
    
def addWhite(card, x = 0, y = 0):
    mute()
    if card.markers[Generosity] < 1:
        card.markers[Generosity] += 1
        notify("{} adds the colour of Generosity to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Generosity!".format(card))
    
def addYellow(card, x = 0, y = 0):
    mute()
    if card.markers[Kindness] < 1:
        card.markers[Kindness] += 1
        notify("{} adds the colour of Kindness to {}.".format(me, card))
    else:
        whisper("{} already has the colour of Kindness!".format(card))
    
def removeColour(card, x = 0, y = 0):
    mute()
    card.markers[Loyalty] = 0
    card.markers[Honesty] = 0
    card.markers[Laughter] = 0
    card.markers[Magic] = 0
    card.markers[Generosity] = 0
    card.markers[Kindness] = 0
    notify("{} removes all colour(s) from {}.".format(me, card))

#Card Rotation for Multiplayer
def rotUp(card, x = 0, y = 0):
    mute()
    card.orientation = Rot0
    update()
    whisper("{} was rotated up.".format(card))

def rotRight(card, x = 0, y = 0):
    mute()
    card.orientation = Rot90
    update()
    whisper("{} was rotated right.".format(card))

def rotDown(card, x = 0, y = 0):
    mute()
    card.orientation = Rot180
    update()
    whisper("{} was rotated down.".format(card))

def rotLeft(card, x = 0, y = 0):
    mute()
    card.orientation = Rot270
    update()
    whisper("{} was rotated left.".format(card))

#---------------------------------------------------------------------------
# Hand Actions
#---------------------------------------------------------------------------
def randomDiscard(group):
    mute()
    card = group.random()
    if card == None: return
    card.moveTo(me.piles['Discard pile'])
    notify("{} randomly discards {}.".format(me, card))
 
def discardMany(group):
    count = 0
    discAmount = None
    
    mute()
    if len(group) == 0: return
    if discAmount == None: discAmount = askInteger("Randomly discard how many cards?", 2)
    if discAmount == None: return
    
    for index in range(0,discAmount):
        card = group.random()
        if card == None: break
        card.moveTo(me.piles['Discard pile'])
        count += 1
        notify("{} randomly discards {}.".format(me,card))
    notify("{} randomly discards {} cards.".format(me, count))

def mulligan(group):
    count = None
    draw = None
    mute()
    
    if not confirm("Are you sure you want to Mulligan?"): return
    if draw == None: draw = askInteger("How many cards would you like to draw for your Mulligan?", len(me.hand))
    if draw == None: return
    
    for card in group:
        card.moveToBottom(me.deck)
            
    me.deck.shuffle()
        
    for card in me.deck.top(draw):
        card.moveTo(me.hand)
    notify("{} mulligans and draws {} new cards.".format(me, draw))
    
def toggleAutoAT(group): #Just a on/off for the Auto AT feature
    if me.getGlobalVariable("toggleAutoAT") == "True":
        me.setGlobalVariable("toggleAutoAT", False)
        whisper("Auto AT and Color Req Check is now turned off.")
    else:
        me.setGlobalVariable("toggleAutoAT", True)
        whisper("Auto AT and Color Req Check is now turned on.")

def toggleAutoMeticulous(group): #Just a on/off for the Auto Meticulous feature
    if me.getGlobalVariable("toggleAutoMeticulous") == "True":
        me.setGlobalVariable("toggleAutoMeticulous", False)
        whisper("Auto Meticulous is now turned off. You will still be alerted via chat if there are any Meticulous cards you can use.")
    else:
        me.setGlobalVariable("toggleAutoMeticulous", True)
        whisper("Auto Meticulous is now turned on.")

#---------------------------------------------------------------------------
# Pile Actions
#---------------------------------------------------------------------------
def shuffle(group):
    group.shuffle()

def draw(group):
    mute()
    PlayerNo = me._id
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))
    
    if len(group) == 0: return
    
    if getGlobalVariable("VillainTurn") == "True" and PlayerNo == villainPlayerId:
        group[0].moveTo(me.hand)
        group[0].moveTo(me.hand)
        notify("Being the villain, {} draws two cards.".format(me))
    else:
        group[0].moveTo(me.hand)
        notify("{} draws a card.".format(me))

def payDraw(group):
    mute()
    if len(group) == 0: return
    if me.counters['Actions'].value == 0:
        whisper("You have no action tokens to draw a card with.")
        return
    group[0].moveTo(me.hand)
    spendAction(group, 0, 0)
    notify("{} pays 1 to draw a card. {} tokens left.".format(me, me.counters['Actions'].value))

def drawMany(group):
    drawAmount = None
    
    mute()
    if len(group) == 0: return
    if drawAmount == None: drawAmount = askInteger("Draw how many cards?", 6)
    if drawAmount == None: return
    
    if len(group) < drawAmount:
        drawAmount = len(group)
    
    for card in group.top(drawAmount):
        card.moveTo(me.hand)
    notify("{} draws {} cards.".format(me, drawAmount))

def discardManyFromTop(group):
    count = 0
    discAmount = None
    
    mute()
    if len(group) == 0: return
    if discAmount == None: discAmount = askInteger("Discard how many from top?", 4)
    if discAmount == None: return
    
    for index in range(0,discAmount):
        card = group.top()
        card.moveTo(me.piles['Discard pile'])
        count += 1
        if len(group) == 0: break
    notify("{} discards {} cards from the top of their Deck.".format(me, count))

def reshuffle(group):
    count = None
    
    mute()
    if len(group) == 0: return
    if not confirm("Are you sure you want to reshuffle the {} back into your deck?".format(group.name)): return
    
    myDeck = me.deck
    for card in group:
        card.moveTo(myDeck)
    myDeck.shuffle()
    notify("{} shuffles their {} back into their deck.".format(me, group.name))

#For discard pile, to move a random card from pile back to hand
def moveOneRandom(group):
    mute()
    if len(group) == 0: return
    if not confirm("Are you sure you want to move one random card from your {} to your Hand?".format(group.name)): return
    
    card = group.random()
    if card == None: return
    card.moveTo(me.hand)
    notify("{} randomly moves {} from their {} to their hand.".format(me, card.name, group.name))

def faceoffFlipTable(group, x = 0, y = 0):
    faceoffFlip(me.Deck)

def faceoffFlip(group):
    mute()
    global FaceoffPosition
    global FaceoffOffset
    PlayerNo = me._id
    villainPlayerId = eval(getGlobalVariable("villainPlayerId"))

    if len(group) == 0: return
    
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False": #Setting faceoff pos for multiplayer
        if PlayerNo == 1:
            if FaceoffPosition == 0:
                FaceoffPosition = 21
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (15 * FaceoffOffset)
            newXPos = 222 + (15 * FaceoffOffset)
            color = FaceoffColor1
        elif PlayerNo == 2:
            if FaceoffPosition == 0:
                FaceoffPosition = 190
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (-15 * FaceoffOffset)
            newXPos = -247 + (-15 * FaceoffOffset)
            color = FaceoffColor2
        elif PlayerNo == 3:
            if FaceoffPosition == 0:
                FaceoffPosition = -120
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (-15 * FaceoffOffset)
            newXPos = -309 + (-15 * FaceoffOffset)
            color = FaceoffColor3
        elif PlayerNo == 4:
            if FaceoffPosition == 0:
                FaceoffPosition = -280
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (15 * FaceoffOffset)
            newXPos = 151 + (15 * FaceoffOffset)
            color = FaceoffColor4
    elif getGlobalVariable("VillainChallengeActive") == "True": #Faceoff card pos for VC
        if me.isInverted:
            if FaceoffPosition == 0:
                FaceoffPosition = -110
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (-15 * FaceoffOffset)
            newXPos = 15 * FaceoffOffset
            color = FaceoffColor1
        if villainPlayerId == 1: 
            if PlayerNo == 2:               
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -15 * FaceoffOffset
                color = FaceoffColor2
            elif PlayerNo == 3:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -310 + (-15 * FaceoffOffset)
                color = FaceoffColor3
            elif PlayerNo == 4:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = 305 + (-15 * FaceoffOffset)
                color = FaceoffColor4
        elif villainPlayerId == 2: 
            if PlayerNo == 1:               
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -15 * FaceoffOffset
                color = FaceoffColor2
            elif PlayerNo == 3:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -310 + (-15 * FaceoffOffset)
                color = FaceoffColor3
            elif PlayerNo == 4:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = 305 + (-15 * FaceoffOffset)
                color = FaceoffColor4
        elif villainPlayerId == 3: 
            if PlayerNo == 1:                               
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -15 * FaceoffOffset
                color = FaceoffColor2
            elif PlayerNo == 2:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -310 + (-15 * FaceoffOffset)
                color = FaceoffColor3
            elif PlayerNo == 4:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = 305 + (-15 * FaceoffOffset)
                color = FaceoffColor4
        elif villainPlayerId == 4: 
            if PlayerNo == 1:                           
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -15 * FaceoffOffset
                color = FaceoffColor2
            elif PlayerNo == 2:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = -310 + (-15 * FaceoffOffset)
                color = FaceoffColor3
            elif PlayerNo == 3:
                if FaceoffPosition == 0:
                    FaceoffPosition = 10
                else:
                    FaceoffOffset += 1
                newYPos = FaceoffPosition + (15 * FaceoffOffset)
                newXPos = 305 + (-15 * FaceoffOffset)
                color = FaceoffColor4
    else:
        if me.isInverted:
            if FaceoffPosition == 0:
                FaceoffPosition = -110
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (-15 * FaceoffOffset)
            newXPos = 15 * FaceoffOffset
            color = FaceoffColor1
        else:
            if FaceoffPosition == 0:
                FaceoffPosition = 10
            else:
                FaceoffOffset += 1
            newYPos = FaceoffPosition + (15 * FaceoffOffset)
            newXPos = -15 * FaceoffOffset
            color = FaceoffColor2
    
    card = group.top()

    if re.search(r'Chaotic', card.Traits):
        color = ChaosColor
    
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False": #Setting card orientation for multiplayer
        if PlayerNo == 2:
            card.moveToTable(newXPos, newYPos)
            card.orientation = Rot90
        elif PlayerNo == 3:
            card.moveToTable(newXPos, newYPos)
            card.orientation = Rot180
        elif PlayerNo == 4:
            card.moveToTable(newXPos, newYPos)
            card.orientation = Rot270
        else:
            card.moveToTable(newXPos, newYPos)
    else:
        card.moveToTable(newXPos, newYPos)
    
    card.highlight = color
    
    notify("{} flips {} for the faceoff with printed power {}.".format(me, card, card.Power))

#---------------------------------------------------------------------------
# Special Mechanics
#---------------------------------------------------------------------------
def inspired(targetgroup, x = 0, y = 0, count = None):
    mute()
    
    PlayerNo = me._id
    
    if len(players) == 1:
        notify("There must be more than 1 player to use Inspired.")
        return
    elif len(players) == 3 and getGlobalVariable("VillainChallengeActive") == "False":
        if PlayerNo == 3: #If last player, go back to first player
            group = players[1].Deck
        else:
            group = players[PlayerNo].Deck
    elif len(players) == 4 and getGlobalVariable("VillainChallengeActive") == "False":
        if PlayerNo == 4: #If last player, go back to first player
            group = players[1].Deck
        else:
            group = players[PlayerNo].Deck
    else:
        group = players[1].Deck
    
    inspiredCount = sum(1 for card in table if card.controller == me and card.isFaceUp == True and (re.search(r'Inspired', card.Keywords) or re.search(r'Inspired', card.Text)))
    
    if count == None:
        count = askInteger("Look at how many cards?", inspiredCount)
    if count == None or count == 0:
        return
    
    notify("{} uses Inspired to look at the top {} cards of {}'s deck.".format(me, count, players[1]))
    
    topCards = group.top(count)
    
    buttons = []  ## This list stores all the card objects for manipulations.
    for c in topCards:
        c.peek()  ## Reveal the cards to python
        buttons.append(c)
    
    topList = []  ## This will store the cards selected for the top of the pile
    bottomList = []  ## For cards going to the bottom of the pile
    rnd(1,2)  ## allow the peeked card's properties to load
    loop = 'BOTTOM'  ## Start with choosing cards to put on bottom
    
    while loop != None:
        desc = "Select a card to place on {}:\n\n{}\n///////DECK///////\n{}".format(
        loop,
        '\n'.join([c.Name for c in topList]),
        '\n'.join([c.Name for c in bottomList]))
        if loop == 'TOP':
            num = askChoice(desc, ["(" + c.Power + ") " + c.Type + ": " + c.Name + " - " + c.Subname for c in buttons], customButtons = ["Select BOTTOM","Leave Rest on BOTTOM","Reset"])
            if num == -1:
                loop = 'BOTTOM'         
            elif num == -2:
                while len(buttons) > 0:
                    card = buttons.pop()
                    bottomList.append(card)
            elif num == -3:
                topList = []
                bottomList = []
                buttons = []
                for c in group.top(count):
                    c.peek()
                    buttons.append(c)
            elif num > 0:
                card = buttons.pop(num - 1)
                topList.insert(0, card)
        else:
            num = askChoice(desc, ["(" + c.Power + ") " + c.Type + ": " + c.Name + " - " + c.Subname for c in buttons], customButtons = ["Select TOP","Leave Rest on TOP","Reset"])
            if num == -1:
                loop = 'TOP'
            elif num == -2:
                while len(buttons) > 0:
                    card = buttons.pop()
                    topList.insert(0, card)
            elif num == -3:
                topList = []
                bottomList = []
                buttons = []
                for c in group.top(count):
                    c.peek()
                    buttons.append(c)
            elif num > 0:
                card = buttons.pop(num - 1)
                bottomList.append(card)
        if len(buttons) == 0: ##  End the loop
            loop = None
        if num == None:  ## closing the dialog window will cancel the ability, not moving any cards, but peek status will stay on.
            return

    topList.reverse()  ## Gotta flip topList so the moveTo's go in the right order
    
    originalOwner = group.controller
    
    update()
    
    group.controller = me

    update()
    time.sleep(.5)

    for c in topList:
        c.controller = me

    update()
    time.sleep(.2)

    for c in topList:
        c.moveTo(group,0)

    update()
        
    for c in bottomList:
        c.moveToBottom(group)
        
    update()
        
    for c in group:  ## This removes the peek status
        c.isFaceUp = True
        c.isFaceUp = False

    time.sleep(.2)

    for c in topList:
        c.controller = originalOwner
    
    update()
    time.sleep(.5)
    
    group.controller = originalOwner

    update()
    
    whisper("{}".format(group.controller))

    notify("{} looked at {} cards and put {} on top and {} on bottom.".format(me, count, len(topList), len(bottomList)))
    
def meticulous(targetgroup, x = 0, y = 0, count = None):
    mute()
    
    PlayerNo = me._id
    deck = me.Deck
    met1Left = 0
    met2Left = 0
    totalCount = 0
    meticulousAgainChoice = 0 #Tells the program to keep to the same met (For when met 1 and 2 are in play)
    met2LoopCount = 0 #To keep track of a smaller loop in met 2 so both cards can be processed

    
    #Count how many met 1 cards are on the table
    meticulous1Count = sum(1 for card in table if card.controller == me and card.isFaceUp == True and (re.search(r'Meticulous 1', card.Keywords) or re.search(r'Meticulous 1', card.Text)))
    
    #Count how many met 2 cards are on the table
    meticulous2Count = sum(1 for card in table if card.controller == me and card.isFaceUp == True and (re.search(r'Meticulous 2', card.Keywords) or re.search(r'Meticulous 2', card.Text)))
    
    #Return if 0 or none for both Met 1 and Met 2 count
    if (meticulous1Count == None or meticulous1Count == 0) and (meticulous2Count == None or meticulous2Count == 0):
        #Return if 0 or none for both Met 1 and Met 2 count
        whisper("No Meticulous cards detected on table!")
        return
    
    #Notify based on which met is used
    if meticulous1Count > 0 and meticulous2Count > 0:
        notify("{} uses '{}' Meticulous 1 and '{}' Meticulous 2 to look at the top card of {}'s deck.".format(me, meticulous1Count, meticulous2Count, me))
    else:
        if meticulous1Count > 0:
            notify("{} uses '{}' Meticulous 1 to look at the top card of {}'s deck.".format(me, meticulous1Count, me))
        else:
            notify("{} uses '{}' Meticulous 2 to look at the top cards of {}'s deck.".format(me, meticulous2Count, me))

    #Loop though all the meticulous
    totalCount = meticulous1Count + meticulous2Count
    met1Left = meticulous1Count
    met2Left = meticulous2Count

    while not totalCount <= 0:
        topCard = deck.top()
        
        #Show choice box if there is met 1 and 2, else just check which met is being used and set the choice permanently
        if meticulous1Count > 0 and meticulous2Count > 0:
            if meticulousAgainChoice == 0: #Check if the program is set to auto pick a met
                meticulousChoice = askChoice("{}/{} Meticulous 1 left!\n\n{}/{} Meticulous 2 left!\n\nWhich Meticulous do you want to use?".format(met1Left, meticulous1Count, met2Left, meticulous2Count), ["Meticulous 1","Meticulous 2", "Cancel"])
            else:
                meticulousChoice = meticulousAgainChoice #Make the choice to the auto picked met
                meticulousAgainChoice = 0 # Reset meticulousAgainChoice
        elif meticulous1Count > 0:
            meticulousChoice = 1
        else:
            meticulousChoice = 2
        
        if meticulousChoice == 1 and met1Left > 0: #Met 1
            desc = "{}/{} Meticulous 1 left!\n\nDo you want to place the card on the TOP or BOTTOM of the deck?\n\n({}) {}: {} - {}".format(met1Left, meticulous1Count, topCard.Power, topCard.Type, topCard.Name, topCard.Subname)
            choiceNum = askChoice(desc, ["TOP", "BOTTOM", "Cancel"])
            
            if choiceNum == 1: #If player picks top
                met1Left -= 1
                notify("{} leaves the card at the top, {}/{} Meticulous 1 left.".format(me, met1Left, meticulous1Count))
            elif choiceNum == 2: #If player picks bottom
                met1Left -= 1
                topCard.moveToBottom(deck)
                notify("{} moves the card to the bottom, {}/{} Meticulous left.".format(me, met1Left, meticulous1Count))
            elif choiceNum == 3: #If player picks Cancel
                if confirm("Are you sure you want to quit Meticulous 1? Any remaining Meticulous 1 will be skipped!"):
                    met1Left = 0
                    notify("{} leaves the card at the top and skips any remaining Meticulous 1.".format(me))
                else:
                    totalCount += 1 #Loop 1 additional time for player to make the choice again
                    meticulousAgainChoice = 1
            else: #If player closes the dialog box
                totalCount += 1 #Loop 1 additional time for player to make the choice again
                meticulousAgainChoice = 1
        elif meticulousChoice == 2 and met2Left > 0: #Met 2
            if met2LoopCount == 0: #First card of met 2
                topCard2 = list(deck.top(2)) #Returns an array of the top 2 cards
                desc = "{}/{} Meticulous 2 left!\n\nDo you want to place the FIRST card on the TOP or BOTTOM of the deck?\n\n>({}) {}: {} - {}\n\n({}) {}: {} - {}".format(met2Left, meticulous2Count, topCard2[0].Power, topCard2[0].Type, topCard2[0].Name, topCard2[0].Subname, topCard2[1].Power, topCard2[1].Type, topCard2[1].Name, topCard2[1].Subname)
                choiceNum = askChoice(desc, ["TOP", "BOTTOM", "Cancel"])
                
                if choiceNum == 1: #If player picks top
                    met2LoopCount = 1 #Move to the second card on next loop
                    notify("{} leaves the first card at the top.".format(me))
                elif choiceNum == 2: #If player picks bottom
                    topCard2[0].moveToBottom(deck)
                    met2LoopCount = 1 #Move to the second card on next loop
                    notify("{} moves the first card to the bottom.".format(me))
                elif choiceNum == 3: #If player picks Cancel
                    if confirm("Are you sure you want to quit Meticulous 2? Any remaining Meticulous 2 will be skipped!"):
                        met2Left = 0
                        notify("{} leaves both cards at the top and skips any remaining Meticulous 2.".format(me))
                
                #Any options the player pick, these 2 must be triggered
                totalCount += 1 #Loop 1 additional time for player to make a choice again or go to the next met 2 loop
                meticulousAgainChoice = 2 #Force the program to auto pick met 2
            else: #Second card of met 2
                desc = "{}/{} Meticulous 2 left!\n\nDo you want to place the SECOND card on the TOP or BOTTOM of the deck?\n\n({}) {}: {} - {}\n\n>({}) {}: {} - {}".format(met2Left, meticulous2Count, topCard2[0].Power, topCard2[0].Type, topCard2[0].Name, topCard2[0].Subname, topCard2[1].Power, topCard2[1].Type, topCard2[1].Name, topCard2[1].Subname)
                choiceNum = askChoice(desc, ["TOP", "BOTTOM"])
                
                if choiceNum == 1: #If player picks top
                    met2Left -= 1
                    met2LoopCount = 0 #Resets the loop for the next met 2
                    notify("{} leaves the second card at the top, {}/{} Meticulous 2 left.".format(me, met2Left, meticulous2Count))
                elif choiceNum == 2: #If player picks bottom
                    topCard2[1].moveToBottom(deck)
                    met2Left -= 1
                    met2LoopCount = 0 #Resets the loop for the next met 2
                    notify("{} moves the second card to the bottom, {}/{} Meticulous 2 left.".format(me, met2Left, meticulous2Count))
                else: #If player closes the dialog box
                    totalCount += 1 #Loop 1 additional time for player to make the choice again
                    meticulousAgainChoice = 2
        elif meticulousChoice == 3:
            if confirm("Are you sure you want to quit Meticulous? Any remaining Meticulous 1 or 2 will be skipped!"):
                totalCount = 0
                notify("{} leaves the card(s) at the top and skips any remaining Meticulous 1 or 2.".format(me))
            else:
                totalCount += 1 #Loop 1 additional time for player to make the choice again
        
        else:
            if meticulous1Count > 0 and meticulous2Count > 0:
                whisper("Please check if you have enough Meticulous left for the choice you picked and try again!")
                totalCount += 1 #Loop 1 additional time for player to make the choice again
            else:
                totalCount = 0
            
        totalCount -= 1 #Reduce the amt of Met left

    notify("{} has no Meticulous left, ending Meticulous.".format(me))