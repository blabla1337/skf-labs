package com.skf.labs.csrfweak;

public class Prefs {
    private int preferenceId;
    private int userId;
    private String color;
    
    public Prefs(int preferenceId, int userId, String color) {
        this.preferenceId = preferenceId;
        this.userId = userId;
        this.color = color;
    }
    public int getPreferenceId() {
        return preferenceId;
    }
    public String getColor() {
        return color;
    }
    public void setColor(String color) {
        this.color = color;
    }
    public int getUserId() {
        return userId;
    }
    public void setUserId(int userId) {
        this.userId = userId;
    }
    public void setPreferenceId(int preferenceId) {
        this.preferenceId = preferenceId;
    }
    @Override
    public String toString() {
        return String.format("Prefs[id=%d | userId=%d | color=%s]",preferenceId,userId,color);
    }
   
    
}
