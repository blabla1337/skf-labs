package com.skf.labs.formulainjection;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import org.springframework.jdbc.core.JdbcTemplate;


@Component
public class FormulaInjectionModel {

@Autowired
private JdbcTemplate jdbcTemplate;

    public List<Page> getPage(String pageId){
        String sql = "SELECT pageId, title, content FROM pages WHERE pageId=?";
        List<Page> pages = jdbcTemplate.query(sql, new Object[]{pageId} ,(resultSet, rowNum) -> new Page(resultSet.getInt("pageId"),resultSet.getString("title"), resultSet.getString("content")));
        return pages;
    }


    public int getLastPageId(){
        String sql = "SELECT MAX(pageId) FROM pages";
        int lastPageId  = jdbcTemplate.queryForObject(sql, Integer.class);
        return lastPageId;
    }
    
    public List<Page> getAllPages(){
        String sql = "SELECT pageId, title, content FROM pages";
        List<Page> pages = jdbcTemplate.query(sql,(resultSet, rowNum) -> new Page(resultSet.getInt("pageId"),resultSet.getString("title"), resultSet.getString("content")));
        return pages;
    }

    public boolean clearPages(){
        String sql = "DELETE FROM pages WHERE pageId > 3";
        return jdbcTemplate.update(sql) == 1;
    }

    public boolean addPage(Page page){
        int pageId = getLastPageId() + 1;
        String sql = "INSERT INTO pages VALUES (?,?,?)";
        Object[] args = new Object[] {pageId,page.getTitle(), page.getContent()};
        return jdbcTemplate.update(sql, args) == 1;

    }
}
