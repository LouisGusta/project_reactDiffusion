import json
import re
from PIL import Image
from numpy import mat
from random import random

def generateJSON(args):
    data = {
        'screen': [
            {
                'width': args.width,
                'height': args.height,
                'fps': args.fps,
                'apf': args.apf,
                'totalFrames': args.totalFrames,
            },
        ],
        'drawing': [
            {
                'dA': args.dA,
                'dB': args.dB,
                'k': args.k,
                'f': args.f,
                'deltaT': args.deltaT,
            }
        ],
        'colors': [
            {
                'mode': args.mode,
                'rA': args.rA,
                'gA': args.gA,
                'bA': args.bA,
                'rB': args.rB,
                'gB': args.gB,
                'bB': args.bB,
            }
        ],
        'metadata': [
            {
                'pathVideo': args.pathVideo,
                'pathThumb': args.pathThumb,
            }
        ]
    }

    json_string = json.dumps(data)

    with open('../simulador/data/params.json', 'w') as outfile:
        outfile.write(json_string)
    outfile.close()

        

def verifyResult(infos):
    with Image.open(infos.pathThumb) as im:
        pixels = im.load()
        diferente = False

        for x in range(20, infos.width-20):
            for y in range(20, infos.height-20):
                if pixels[x,y] != (0,0,0, 255):
                    diferente = True
                    break

        if not diferente:
            return False

        diferente = False

        for x in range(20, infos.width-20):
            for y in range(20, infos.height-20):
                if pixels[x,y] != (255,255,255, 255):
                    diferente = True
                    break

        if not diferente:
            return False
        return True

def saveBadResults(infos):
    badResultsPath = 'logs/badResults/badParams.json'
    data = json.load(open(badResultsPath))
    data['drawing'].append({'dA': infos.dA, 'dB': infos.dB, 'k':  infos.k, 'f':  infos.f})
    json_string = json.dumps(data)

    with open(badResultsPath, 'w') as outfile:
        outfile.write(json_string)

def saveGoodResults(infos):
    goodResultsPath = 'logs/goodResults/goodParams.json'
    data = json.load(open(goodResultsPath))
    
    data['drawing'].append({'dA': infos.dA, 'dB': infos.dB, 'k':  infos.k, 'f':  infos.f})
    json_string = json.dumps(data)

    with open(goodResultsPath, 'w') as outfile:
        outfile.write(json_string)

def isRepeat(f, k, dA, dB): 
    badResultsPath = 'logs/badResults/badParams.json'
    data = json.load(open(badResultsPath))

    for x in data['drawing']:
        if x['k'] == k and x['f'] == f and x['dA'] == dA and x['dB'] == dB:
            print('passei aqui no ruim')

            return True, True, True, True

    goodResultsPath = 'logs/goodResults/goodParams.json'
    data = json.load(open(goodResultsPath))
    
    for x in data['drawing']:
        if x['k'] == k and x['f'] == f and x['dA'] == dA and x['dB'] == dB:
            print('passei aqui no bom')
            return True, True, True, True
    return f, k, dA, dB

def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

def getRandomValue():
        k= f = dA = dB = False
        while k == False or f == False or dA == False or dB == False: 
            k, f, dA, dB = isRepeat(float("{:.4f}".format(mapFromTo(random(), 0, 1, 0.052, 0.066))), float("{:.4f}".format(mapFromTo(random(), 0, 1, 0.001, 0.052))), 1.0, 0.5)#float("{:.1f}".format(random()+.5)), float("{:.1f}".format(random()+.5)))
        return k, f, dA, dB

def v(u):
    u /= 255
    return u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4

def luminence(r, g, b):
    return v(r) * 0.2126 + v(g) * 0.7152 + v(b) * 0.0722

def contrast(rgbA, rgbB):
    lumA = luminence(rgbA[0], rgbA[1], rgbA[2]) 
    lumB = luminence(rgbB[0], rgbB[1], rgbB[2]) 
    brightest = max(lumA, lumB)
    darkest = min(lumA, lumB)

    return (brightest + 0.05) / (darkest + 0.05)

def getColors():
    randomMode = int(random() * 100)
    if randomMode < 5:
        mode = 2
    elif randomMode < 10:
        mode = 1
    else:
        mode = 0

    if mode == 0:
        control = 0
        while control < 4.5:
            rA = int(random() * 256)
            gA = int(random() * 256)
            bA = int(random() * 256)

            rB = int(random() * 256)
            gB = int(random() * 256)
            bB = int(random() * 256)
            
            control = contrast([rA, gA, bA], [rB, gB, bB])
        return mode, rA, gA, bA, rB, gB, bB
    return mode, None, None, None, None, None, None    





