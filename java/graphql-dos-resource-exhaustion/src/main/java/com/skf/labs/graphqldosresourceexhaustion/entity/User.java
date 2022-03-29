package com.skf.labs.graphqldosresourceexhaustion.entity;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToOne;
import javax.persistence.JoinColumn;
import com.skf.labs.graphqldosresourceexhaustion.entity.Post;
import javax.persistence.CascadeType;



@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    
    private String username;
    private String password;
    private boolean admin;
    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name="post_id", referencedColumnName = "id")
    private Post post;


    public User() {
    }

    
    public User(int id) {
        this.id = id;
    }
    

    
    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public boolean is_admin() {
        return admin;
    }
    public void setAdmin(boolean admin) {
        this.admin = admin;
    }


    public Post getPost() {
        return post;
    }


    public void setPost(Post post) {
        this.post = post;
    }
}
