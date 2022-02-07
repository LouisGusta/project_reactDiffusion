import subprocess, os, sys

sys.path.insert(0, os.path.abspath(os.getcwd()) + '\\..\\upload_yt')
import upload_video
import details
from helper import generateJSON, verifyResult, saveBadResults, saveGoodResults

if __name__ == '__main__':
    # running script params in json for create a diffusion
    while True: 
        generateJSON(details.Infos)

        # SECTION PROCESSING DIFFUSION
        filePath = os.path.abspath(os.getcwd()) + '\..\simulador'
        fileName = 'diffusionVideo.exe'
        if os.path.exists(filePath +  '\\' + fileName):
            process = subprocess.Popen(fileName, stdout=subprocess.PIPE, creationflags=0x08000000, shell=True, cwd=filePath)
            process.communicate()
        
        # valid if result not is a full dark pixels or white pixels and save bad results
        if not verifyResult(details.Infos): 
            saveBadResults(details.Infos)
        else: 
            saveGoodResults(details.Infos)
            break
    # SECTION RUN YOUTUBE UPLOADER
    upload_video.uploadVideo()



