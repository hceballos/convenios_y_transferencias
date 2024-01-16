class Contraloria(Fuente):

	def opcion1(self):
		print("Has seleccionado la opción 1.")
		repo_url = "https://github.com/hceballos/convenios_y_transferencias.git"
		subprocess.run(["git", "clone", repo_url])
		print(f"Repositorio clonado exitosamente desde: {repo_url}")





	def opcion2(self):
		print("Has seleccionado la opción 2.")
		# Aquí puedes agregar la lógica correspondiente a la opción 2




	def descargar_archivo(self,url):
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		else:
			print(f"No se pudo descargar el archivo. Código de estado: {response.status_code}")
			return None

	def actualizar_archivo_local(self, archivo_contenido, ruta_local):
		with open(ruta_local, 'w') as archivo_local:
			archivo_local.write(archivo_contenido)
		print(f"Archivo actualizado localmente: {ruta_local}")






	def __init__(self, json_path):
		Fuente.__init__(self, json_path)
 
		datos = self.datos



		url_archivo_github = "https://raw.githubusercontent.com/hceballos/convenios_y_transferencias/master/lib/elementos.py"
		ruta_local_archivo = "/Users/hector/Documents/Documents/desarrollo/convenios_y_transferencias/lib/contraloria/elementos.py"

		while True:
			print("\nMenú:")
			print("1. Descargar y actualizar archivo")
			print("2. Salir")

			seleccion = input("Selecciona una opción (1/2): ")

			if seleccion == "1":
				contenido_archivo = self.descargar_archivo(url_archivo_github)
				if contenido_archivo:
					self.actualizar_archivo_local(contenido_archivo, ruta_local_archivo)
			elif seleccion == "2":
				print("Saliendo del programa. ¡Hasta luego!")
				break
			else:
				print("Opción no válida. Por favor, elige una opción válida.")