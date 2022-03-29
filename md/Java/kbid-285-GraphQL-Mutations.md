# KBID 285 - GraphQL mutations

## Running the app Java

First make sure java is installed on your host machine.
After installation, we go to the folder of the lab we want to practice.
"i.e /skf-labs/XSS, /skf-labs/RFI/" and run the following command:

```
$ ./mvnw spring-boot:run
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The application implements a very basic mutation to create a new post on the blog. The mutation used is the following

```
mutation {
  createPost(title: "This is a new title", body: "This is a new post", author_id: 2) {
    id
    title
    body
  }
}
```

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

> What can you exploit? ;)

## Additional resources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html" %}
