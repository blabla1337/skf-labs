package com.skf.labs.xssstored;


public class Page{
    private int pageId;
    private String title;
    private String content;


    public Page(int pageId, String title, String content){
        this.pageId = pageId;
        this.title = title;
        this.content = content;
    }
    public int getPageId() {
        return pageId;
    }
    public void setPageId(int pageId) {
        this.pageId = pageId;
    }
    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
    }
    public String getContent() {
        return content;
    }
    public void setContent(String content) {
        this.content = content;
    }

    @Override
    public String toString(){ 
        return String.format("Page[id=%d | title=%s | cotent=%s]",pageId,title,content);
    }

}
