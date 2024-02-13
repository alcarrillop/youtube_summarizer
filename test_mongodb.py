from pymongo import MongoClient

# Reemplaza 'mongodb_uri' con la URI de conexión a tu instancia de MongoDB.
# Para una instancia local, podría ser algo como: "mongodb://localhost:27017/"
mongodb_uri = "mongodb://localhost:27017/"
database_name = "local"

try:
    # Establecer la conexión con MongoDB
    client = MongoClient(mongodb_uri)
    database = client[database_name]

    # Opcional: Intenta leer una colección específica
    collection_name = "youtube_summarizer"
    collection = database[collection_name]
    count = collection.count_documents({})
    print(f"Conexión exitosa. La colección '{collection_name}' tiene {count} documentos.")

except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
