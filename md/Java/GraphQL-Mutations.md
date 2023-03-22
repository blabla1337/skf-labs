# GraphQL Mutations

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:java-graphql-mutation
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-graphql-mutation
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The application implements a very basic mutation to create a new post on the blog. The mutation used is the following

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Mutation/1.png)

```
mutation {
  createPost(title: "This is a new title", body: "This is a new post", author_id: 2) {
    id
    title
    body
  }
}
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Mutation/2.png)

If we look at the code we have a class `CreatePost` that will implement our logic to create a post.

```java
public Post createPost(String title, String body, int user_id) throws org.hibernate.exception.GenericJDBCException{
    Post post = new Post();
    post.setTitle(title);
    post.setBody(body);
    post.setUser(new User(user_id));
    postRepository.save(post);
    return post;
}
```

The method mutate will just get the new Post object and insert an instance in the database.

## Exploit

There are many ways we could exploit this, one would be to delete any post we want.
If there is a createPost class there might be another class called deletePost, let's try:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Mutation/3.png)

Bingo! Post with id:4 was deleted. If we go back and refresh the application:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/Graphql-Mutation/4.png)

You could, of course, achieve the same goal with burp.
What else can you exploit using this vulnerability?

## Additional resources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html" %}
