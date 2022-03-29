package com.skf.labs.credentialsguessing2;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;

@Component
public class CredentialsGuessingModel {

    @Autowired
private JdbcTemplate jdbcTemplate;

    public List<User> getUser(String username){
        String sql = "SELECT UserId, Username, Password FROM users WHERE Username=?";
        List<User> users = jdbcTemplate.query(sql,new Object[]{username} ,(resultSet, rowNum) -> new User(resultSet.getInt("UserId"),resultSet.getString("Username"), resultSet.getString("Password")));
        return users;
    }

    public boolean isValidUsername(String username){
        String sql = "SELECT COUNT(Username) FROM users WHERE Username=?";
        if(jdbcTemplate.queryForObject(sql,new Object[]{username},Integer.class) > 0){
            return true;
        }
        return false;
    }
    
}
