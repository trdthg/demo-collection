package com.moflowerlkh.decisionengine.vo.enums;

//取值"在职"/"待业"/"失业"/"退休"/"离休"/"退职"/"退养"/"病休"/"其他
public enum Employment {
    Employed, // 在职
    ReadyForEmployment, // 待业
    Unemployed, // 失业
    LoseJob, // 失业
    Retired, // 退休
    SickLeave, // 病休
    Other; // 其他

    public static boolean isValid(String s) {
        for (Employment employment : Employment.values()) {
            if (employment.name().equalsIgnoreCase(s)) {
                return true;
            }
        }
        return false;
    }

}