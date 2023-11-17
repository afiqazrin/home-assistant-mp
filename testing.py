from multiprocessing import Process
from gesture import main_opencv

gesture_process = Process(target=main_opencv)
gesture_process.start()
