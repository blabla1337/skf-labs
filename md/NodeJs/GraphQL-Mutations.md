# GraphQL Mutations

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-graphql-mutations
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-graphql-mutations
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The application implements a very basic mutation to create a new post on the blog. The mutation used is the following

```
mutation{
  createPost(title: "This is a new title", body: "This is a new post", author_id: 2 ){
    id
    title
    body
    author_id
  }
}


```

If we look at the code we have a class `CreatePost` that will implement our logic to create a post.

```javascript
const mutationType = new graphql.GraphQLObjectType({
  name: "Mutation",
  fields: {
    createPost: {
      type: PostType,
      args: {
        title: {
          type: new graphql.GraphQLNonNull(graphql.GraphQLString),
        },
        body: {
          type: new graphql.GraphQLNonNull(graphql.GraphQLString),
        },
        author_id: { type: new graphql.GraphQLNonNull(graphql.GraphQLID) },
      },
      resolve: (root, { title, body, author_id }) => {
        return new Promise((resolve, reject) => {
          database.run(
            "INSERT INTO Posts (title, body, author_id) VALUES (?,?,?);",
            [title, body, author_id],
            (err) => {
              if (err) {
                reject(null);
              }
              database.get("SELECT last_insert_rowid() as id", (err, row) => {
                resolve({
                  id: row["id"],
                  title: title,
                  body: body,
                  author_id: author_id,
                });
              });
            }
          );
        });
      },
    },
  },
});
```

The method mutate will just get the new Post object and insert an instance in the database.

## Exploit

> What can you exploit? ;)

## Additional resources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html" %}
