package com.skf.labs.jwtsecret;

import java.util.ArrayList;
import java.util.List;

import com.skf.labs.jwtsecret.User;

public class JwtModel {
    public static List<User> users = new ArrayList<User>();

    public static void init() {
        users.add(new User(1, "user", "user"));
        users.add(new User(2, "user2", "abcxyz"));

    }
}
