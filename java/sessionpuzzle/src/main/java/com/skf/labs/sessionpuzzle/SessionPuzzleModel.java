package com.skf.labs.sessionpuzzle;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;

@Component
public class SessionPuzzleModel {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> getUser(String username) {
        String sql = "SELECT UserId, Username, Password FROM users WHERE Username=?";
        List<User> users = jdbcTemplate.query(sql, new Object[] { username },
                (resultSet, rowNum) -> new User(resultSet.getInt("UserId"), resultSet.getString("Username"),
                        resultSet.getString("Password")));
        return users;
    }

    public boolean createUser(User user) {
        String sql = "INSERT INTO users (UserId,UserName,Password) VALUES (?,?,?)";
        Object[] args = new Object[] { user.getUserId(), user.getUsername(), user.getPassword() };
        return jdbcTemplate.update(sql, args) == 1;

    }

    public void updatePassword(String password, String username) {
        String sql = "UPDATE users SET Password=? WHERE username=?";
        jdbcTemplate.update(sql, password, username);

    }

}
