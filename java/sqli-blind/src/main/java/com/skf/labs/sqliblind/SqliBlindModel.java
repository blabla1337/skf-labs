package com.skf.labs.sqliblind;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import org.springframework.jdbc.core.JdbcTemplate;


@Component
public class SqliBlindModel {

@Autowired
private JdbcTemplate jdbcTemplate;

public List<Page> getPage(String pageId){
    String sql = "SELECT pageId, title, content FROM pages WHERE pageId="+pageId;
    List<Page> pages = jdbcTemplate.query(sql, (resultSet, rowNum) -> new Page(resultSet.getInt("pageId"),resultSet.getString("title"), resultSet.getString("content")));
    return pages;
}
    
}
