import threading


from face_commands import FaceCommands
from voice_commands import VoiceCommands

def main():

    face_commands = FaceCommands()
    voice_commands = VoiceCommands()


    face_thread = threading.Thread(target=face_commands.run)
    voice_thread = threading.Thread(target=voice_commands.listen)


    face_thread.start()
    voice_thread.start()

    
    face_thread.join()
    voice_thread.join()

if __name__ == "__main__":
    main()




   