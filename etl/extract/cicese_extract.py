from cicese import gather_cicese_data
import os

def main():

    # PENDIENTE: pasar a limpio, hacer un loop por todas las estaciones
    directory_to = os.path.join(os.getcwd(), "data", "raw")  

    gather_cicese_data(2021, directory_to=directory_to, location="isla_cedros")

if __name__ == '__main__':
    main()
