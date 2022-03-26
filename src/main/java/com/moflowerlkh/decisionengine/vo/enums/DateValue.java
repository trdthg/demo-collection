package com.moflowerlkh.decisionengine.vo.enums;

import javax.validation.Constraint;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import javax.validation.Payload;
import java.lang.annotation.*;
import java.sql.Timestamp;

@Target({ ElementType.FIELD })
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = DateValue.Validator.class)
@Documented
public @interface DateValue {

    String message() default "格式只能是: `yyyy-mm-dd hh:mm:ss[.fffffffff]`";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    public class Validator implements ConstraintValidator<DateValue, String> {
        public void initialize(DateValue dateValue) {
        }

        public boolean isValid(String value, ConstraintValidatorContext context) {
            // validate the value here.
            if (value == null) {
                return false;
            }
            try {
                // Timestamp format must be yyyy-mm-dd hh:mm:ss[.fffffffff]
                Timestamp.valueOf(value);
                return true;
            } catch (Exception e) {
                return false;
            }
        }
    }

}
