package com.skf.labs.xssstored;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import org.springframework.jdbc.core.JdbcTemplate;

@Component
public class XssStoredModel {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<Page> getPage(String pageId){
        String sql = "SELECT pageId, title, content FROM pages WHERE pageId=?";
        List<Page> pages = jdbcTemplate.query(sql,new Object[]{pageId} , (resultSet, rowNum) -> new Page(resultSet.getInt("pageId"),resultSet.getString("title"), resultSet.getString("content")));
        return pages;
    }

    public void updatePage(Page page){
        String sql = "UPDATE pages SET title=? , content=? WHERE pageId=?";
        jdbcTemplate.update(sql,page.getTitle(), page.getContent(), page.getPageId());
       
    }
    
}
