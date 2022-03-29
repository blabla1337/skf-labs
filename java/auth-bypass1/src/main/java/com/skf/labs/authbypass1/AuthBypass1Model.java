package com.skf.labs.authbypass1;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;


@Component
public class AuthBypass1Model {

@Autowired
private JdbcTemplate jdbcTemplate;

public List<User> getUser(String username){
    String sql = "SELECT Username, Password, Hash FROM users WHERE Username=?";
    List<User> users = jdbcTemplate.query(sql,new Object[]{username} ,(resultSet, rowNum) -> new User(resultSet.getString("Username"), resultSet.getString("Password"),resultSet.getString("Hash")));
    return users;
}

public List<User> getHash(String hash){
    String sql = "SELECT Username, Password, Hash FROM users WHERE Hash=?";
    List<User> users = jdbcTemplate.query(sql,new Object[]{hash} ,(resultSet, rowNum) -> new User(resultSet.getString("Username"), resultSet.getString("Password"),resultSet.getString("Hash")));
    return users;
}

public boolean createUser(User user){
    String sql = "INSERT INTO users (UserName,Password,Hash) VALUES (?,?,?)";
    Object[] args = new Object[] {user.getUsername(),user.getPassword(),user.getHash()};
    return jdbcTemplate.update(sql, args) == 1;

}

public void updatePassword(String password, String username){
    String sql = "UPDATE users SET Password=? WHERE username=?";
    jdbcTemplate.update(sql,password, username);
   
}
    
}
