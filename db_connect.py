from mongoengine import connect

connect(
    db="calmconnect_db",
    host="localhost",
    port=27017
)
