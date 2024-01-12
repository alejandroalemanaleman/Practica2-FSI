import time

import cv2
import numpy as np
from Person import Person

video = "people_walking.mp4"

def personDetectorByDistance(peopleDetectedActualFrame, activePerson):
    for personDetected in peopleDetectedActualFrame:
        distance = np.sqrt((personDetected.calculate_center()[0] - activePerson.calculate_center()[0]) ** 2 + (personDetected.calculate_center()[1] - activePerson.calculate_center()[1]) ** 2)
        if distance < 80: # Cumple que es la misma persona
            return personDetected
    return None

def personStateEvaluator(person):
    if person.state:
        if 5 < person.calculate_center()[0] > 395 or 5 < person.calculate_center()[1] > 295:
            person.state = False
            return False


fullBodies = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cap = cv2.VideoCapture(video)
allPeopleDetected = []
id = 1

while True:
    # Take each frame
    retVal, frame = cap.read()
    if not retVal:
        break
    frame = cv2.resize(frame, (400, 300))

    # Convertir la imagen a grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    personsDetected = fullBodies.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
    peopleDetectedActualFrame = []
    lista = [rect for rect in personsDetected if (rect[2] * rect[3]) < 5000] # Filtrar rectangulos muy grandes (detecciones incorrectas)

    for (x, y, w, h) in lista:
        peopleDetectedActualFrame.append(Person((x, y, w, h), frame))

    for activePerson in allPeopleDetected:
        personStateEvaluator(activePerson)
        if not activePerson.state:
            allPeopleDetected.remove(activePerson)
            continue
        repeatedPerson = personDetectorByDistance(peopleDetectedActualFrame, activePerson) # Primer control de si personas de frame actual ya estuvo en frame anterior (comprobar si hay personas nuevas)
        if repeatedPerson:
            activePerson.updateRectangle(repeatedPerson.rectangle)
            activePerson.drawRectangle(frame)
            peopleDetectedActualFrame.remove(repeatedPerson)
        else:
            activePerson.find_matching(frame)
            repeatedPerson = personDetectorByDistance(peopleDetectedActualFrame, activePerson)
            if repeatedPerson:
                peopleDetectedActualFrame.remove(repeatedPerson)

    for person in peopleDetectedActualFrame:
        person.id = id
        id += 1
        allPeopleDetected.append(person)
        person.drawRectangle(frame)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    time.sleep(0.01)

cv2.destroyAllWindows()
# Release the frame
cap.release()