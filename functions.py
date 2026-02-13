def read_number(message):
    while True:
        entry = input(message)
        try:
            valor = float(entry)
            
            if valor < 0:
                print("❌ Erro: O valor não pode ser negativo.")
            else:
                return valor 
                
        except ValueError:
            
            print("⚠️ Erro: Digite apenas números (ex: 10.50).")

