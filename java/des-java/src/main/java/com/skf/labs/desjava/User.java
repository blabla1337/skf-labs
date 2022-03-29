package com.skf.labs.desjava;

import java.io.Serializable;


public class User  implements Serializable{
    private static final long serialVersionUID = 0L;
    private String username;
    private String role;
    
    public User(String username, String role) {
        this.username = username;
        this.role = role;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
    
    
}
