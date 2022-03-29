package com.skf.labs.clientsiderestrictionbypass;

public class Prefs {
    private int preferenceId;
    private int userId;
    private String Color;
    private String Food;

    public Prefs(int preferenceId, int userId, String Color, String Food) {
        this.preferenceId = preferenceId;
        this.userId = userId;
        this.Color = Color;
        this.Food = Food;
    }

    public int getPreferenceId() {
        return preferenceId;
    }

    public String getColor() {
        return Color;
    }

    public void setColor(String Color) {
        this.Color = Color;
    }

    public String getFood() {
        return Food;
    }

    public void setFood(String Food) {
        this.Food = Food;
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
        return String.format("Prefs[id=%d | userId=%d | color=%s | food=%s]", preferenceId, userId, Color, Food);
    }

}
