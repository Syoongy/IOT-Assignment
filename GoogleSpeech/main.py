from GoogleSpeech import asr, sr, tts

tts("Welcome to Smart Fridge. To activate the voice command, say 'Smart Fridge'")

while True:
    activate = asr().lower() #Activates the fridge, convert the user's words into
    #we add in switch because in our tests, most of the result either come from smart fridge or smart switch
    if ("smart" in activate) and (("fridge" in activate) or ("switch" in activate)):
        activatecount = 0 #Count the number of attempts after it got activated
        while (activatecount<3):
	    if (activatecount!=0):
		tts("Sorry, I do not get your response. Please try again.")
	    tts("What can I do for you?")
	    command = sr().lower() #Command the fridge, like check temperature
	    if("temperature" in command):
		#do something to check fridge temperature
		break
	    elif("scan" in command):
		#do something to scan the item
		break
	    else:
		activatecount+=1
		if(activatecount==3):
		    tts("We are unable to receive your response after three tries. To activate again, say 'Smart Fridge'")
