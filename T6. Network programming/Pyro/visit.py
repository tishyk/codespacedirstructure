# This is the code that runs this example.
import Pyro5.api
from person import Person


uri = input("Enter the uri of the warehouse: ").strip()
warehouse = Pyro5.api.Proxy(uri)
janet = Person("Janet")
henry = Person("Henry")
janet.visit(warehouse)
henry.visit(warehouse)