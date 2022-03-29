package com.skf.labs.authbypass2;

public class User {
    
    private String username;
    private String password;
    private String hash;
    
    public User(String username, String password, String hash) {
        this.username = username;
        this.password = password;
        this.hash = hash;
    }
  
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getHash() {
        return hash;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }
    @Override
    public String toString() {
        return String.format("User[hash=%s | username=%s | password=%s]",hash,username,password);
    }

    
}
