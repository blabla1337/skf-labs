package com.skf.labs.cors;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;


@Component
public class CorsModel {

@Autowired
private JdbcTemplate jdbcTemplate;

    public List<User> getUser(String username){
        String sql = "SELECT UserId, Username, Password FROM users WHERE Username=?";
        List<User> users = jdbcTemplate.query(sql,new Object[]{username} ,(resultSet, rowNum) -> new User(resultSet.getInt("UserId"),resultSet.getString("Username"), resultSet.getString("Password")));
        return users;
    }

    
}
