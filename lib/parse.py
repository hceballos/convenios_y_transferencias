import json


class Parse(object):






    def exportar_jl(self, datos, almacen):
        with open(datos['archivo_exportacion'], 'a+') as f:
            json.dump(almacen, f, ensure_ascii=False)


