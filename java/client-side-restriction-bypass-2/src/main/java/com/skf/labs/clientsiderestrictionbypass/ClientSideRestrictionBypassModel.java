package com.skf.labs.clientsiderestrictionbypass;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;

@Component
public class ClientSideRestrictionBypassModel {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> getUser(String username) {
        String sql = "SELECT UserId, Username, Password FROM users WHERE Username=?";
        List<User> users = jdbcTemplate.query(sql, new Object[] { username },
                (resultSet, rowNum) -> new User(resultSet.getInt("UserId"), resultSet.getString("Username"),
                        resultSet.getString("Password")));
        return users;
    }

    public List<Prefs> getPrefs(int userId) {
        String sql = "SELECT PreferenceId, Color, Food ,UserId FROM prefs WHERE UserId=?";
        List<Prefs> pref = jdbcTemplate.query(sql, new Object[] { userId },
                (resultSet, rowNum) -> new Prefs(resultSet.getInt("PreferenceId"), resultSet.getInt("UserId"),
                        resultSet.getString("Color"), resultSet.getString("Food")));
        return pref;
    }

    public void updateColor(int userId, String color) {
        String sql = "UPDATE prefs SET Color=? WHERE UserId=?";
        jdbcTemplate.update(sql, color, userId);

    }

    public void updateFood(int userId, String food) {
        String sql = "UPDATE prefs SET Food=? WHERE UserId=?";
        jdbcTemplate.update(sql, food, userId);

    }
}
