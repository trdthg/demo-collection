package com.moflowerlkh.decisionengine.vo.enums;

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