import PyInstaller.__main__
import vosk
import os
vosk_path = os.path.dirname(vosk.__file__)
PyInstaller.__main__.run([
    'gui.py',                          
    '--name=Voice_assistant',            
    '--onedir',                         
    
    '--add-data=model;model',
    '--add-data=picture;picture',
    '--add-data=data.json;.',
    
    f'--add-data={vosk_path};vosk',
    
    '--add-binary=flac.exe;.',
    '--add-binary=metaflac.exe;.',
    '--add-binary=libFLAC.dll;.',
    '--add-binary=libFLAC++.dll;.',
    
    '--clean',
    
    '--noconsole' 
])
