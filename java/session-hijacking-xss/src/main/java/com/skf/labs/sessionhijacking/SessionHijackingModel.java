package com.skf.labs.sessionhijacking;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;

@Component
public class SessionHijackingModel {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> getUser(String username) {
        String sql = "SELECT UserId, Username, Password FROM users WHERE Username=?";
        List<User> users = jdbcTemplate.query(sql, new Object[] { username },
                (resultSet, rowNum) -> new User(resultSet.getInt("UserId"), resultSet.getString("Username"),
                        resultSet.getString("Password")));
        return users;
    }

    public List<Prefs> getMessage(int userId) {
        String sql = "SELECT PreferenceId, API_key ,UserId FROM prefs WHERE UserId=?";
        List<Prefs> pref = jdbcTemplate.query(sql, new Object[] { userId },
                (resultSet, rowNum) -> new Prefs(resultSet.getInt("PreferenceId"), resultSet.getInt("UserId"),
                        resultSet.getString("API_key")));
        return pref;
    }

    public void updateMessage(int userId, String message) {
        String sql = "UPDATE prefs SET API_key=? WHERE UserId=?";
        jdbcTemplate.update(sql, message, userId);

    }
}
