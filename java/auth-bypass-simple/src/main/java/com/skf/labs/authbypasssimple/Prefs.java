package com.skf.labs.authbypasssimple;

public class Prefs {
    private int preferenceId;
    private int userId;
    private String APIkey;
    
    public Prefs(int preferenceId, int userId, String APIkey) {
        this.preferenceId = preferenceId;
        this.userId = userId;
        this.APIkey = APIkey;
    }
    public int getPreferenceId() {
        return preferenceId;
    }
    public String getAPIkey() {
        return APIkey;
    }
    public void setAPIkey(String APIkey) {
        this.APIkey = APIkey;
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
        return String.format("Prefs[id=%d | userId=%d | color=%s]",preferenceId,userId,APIkey);
    }
   
    
}
