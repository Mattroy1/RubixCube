import os

for i in os.listdir("Logs"):
    os.remove(os.path.join("Logs",i))