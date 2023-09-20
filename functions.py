def func_ler_arquivo(arquivo):
    with open(f"{arquivo}", "r") as arquivo:
        texto = arquivo.read()
    lista_de_views = texto.split('\n')
    for i in lista_de_views:
        if i == '':
            lista_de_views.remove(i)
    return lista_de_views

print(func_ler_arquivo('poo/query.txt'))