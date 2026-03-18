# Реализуйте здесь клиент для GraphQL.
import requests

URL = "http://localhost:8172/graphql"

PROJECT_CODE = "bookings-s18"

def build_payload(query: str, variables: dict) -> dict:

    if variables:
        return {
            "query": query,
            "variables": variables
        }
    return{"query": query}

def qu(url, query, variables:dict=None):
    pl=build_payload(query, variables or {})
    try: 
        res = requests.post(url, json=pl)
        print(res.json())
        data=res.json()
        if "errors" in data:
            print("Error:", data["errors"])
        else:    
            print("Books:", data["data"])
    except:
        print("err")



query = """
query {
    books {
        id
        name
        serial
    }
}
    """

mutation = """
    mutation($name: String!, $serial: String!) {
        createBook(name: $name, serial: $serial) {
            id
            name
            serial
        }
    }
    """

variables = {
        "name": "new_book",
        "serial": "S1"
}

variables2 ={
    "name": "new_book2",
    "serial" : "S2"
}

qu(URL, mutation, variables)
qu(URL, mutation, variables2)
qu(URL, query)