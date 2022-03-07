package com.moflowerlkh.decisionengine.enums;

public enum Gender {
    Male,
    Female;

    public static boolean isValid(String s) {
        for (Gender gender : Gender.values()) {
            if (gender.name().equalsIgnoreCase(s)) {
                return true;
            }
        }
        return false;
    }
}