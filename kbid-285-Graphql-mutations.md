# KBID 285 - GraphQL mutations

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:graphql-mutations

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:graphql-mutations
```

Or alternatively build yourself! 

```sh
docker build . -t graphql/mutations && docker run -ti -p 5000:5000 graphql/mutations
```

The docker should be up in no time and we should now be able to browse the application on `http://0.0.0.0:5000/`


{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}

![Docker Image and write-up thanks to defev!](.gitbook/assets/logo.defdev.1608z.whtonblk.256.png)


## Reconnaissance

The application implements a very basic mutation to create a new post on the blog. The mutation used is the following

```
mutation {
  createPost(input: {body: "' -- ", title: "test_title", authorId: 2}) {
    post {
      body
      authorId
      title
    }
  }
}

```

If we look at the code we have a class `CreatePost` that will implement our logic to create a post.

```python
class CreatePost(graphene.Mutation):
    """Mutation to create a post."""
    post = graphene.Field(lambda: PostObject, description="Post created by this mutation.")

    class Arguments:
    	
        input = CreatePostInput(required=True)

    def mutate(self, info, input):
        
        post = Post(**input)
        db.session.add(post)
        db.session.commit()
        
        return CreatePost(post=post)
```

The method mutate will just get the new Post object and insert an instance in the database. 

## Exploit

> What can you exploit? ;)



