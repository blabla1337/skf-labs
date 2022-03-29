package com.skf.labs.jwtnull;

import java.util.ArrayList;
import java.util.List;

import com.skf.labs.jwtnull.User;

public class JwtModel {
    public static List<User> users = new ArrayList<User>();
    
    public static void init(){
        users.add(new User(1,"user","user","guest"));
        users.add(new User(2,"user2","user2","mortal"));
        users.add(new User(3,"immortal","immortal","admin"));


      
    }
}
