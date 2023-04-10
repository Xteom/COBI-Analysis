from cicese import gather_cicese_data

def main():

    # PENDIENTE: pasar a limpio, hacer un loop por todas las estaciones
    directory_to = "C:\\Users\\javi2\\Documents\\CD_aplicada_1\\COBI\\etl\\data\\cicese\\raw\\"
    gather_cicese_data(2021, directory_to=directory_to, location="guerrero_negro")

if __name__ == '__main__':
    main()
