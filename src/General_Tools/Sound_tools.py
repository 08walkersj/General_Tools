import inspect

def play_sound(sound_file='success'):
    if not sound_file.endswith('.mp3'):
        path='/'.join(inspect.getsourcefile(play_sound).split('/')[:-1])
        sound_file= path+f'/Sounds/{sound_file.lower()}.mp3'
    import pygame
    pygame.mixer.init()
    sound= pygame.mixer.Sound(sound_file)
    sounda=sound.play()
    while sounda.get_busy():
    	pygame.time.delay(int(sound.get_length())+1)
