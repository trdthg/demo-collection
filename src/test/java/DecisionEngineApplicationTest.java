import com.github.javafaker.Faker;
import com.moflowerlkh.decisionengine.domain.dao.BankAccountDao;
import com.moflowerlkh.decisionengine.domain.dao.UserDao;
import com.moflowerlkh.decisionengine.domain.entities.BankAccount;
import com.moflowerlkh.decisionengine.domain.entities.User;
import com.moflowerlkh.decisionengine.vo.enums.Employment;
import com.moflowerlkh.decisionengine.vo.enums.Gender;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.*;

@RunWith(SpringRunner.class)   //这两个注解是为了让测试类能拥有同等的spring boot上下文环境
@SpringBootTest(classes = com.moflowerlkh.decisionengine.DecisionEngineApplication.class)
public class DecisionEngineApplicationTest {

    @Autowired
    UserDao userDao;
    @Autowired
    BankAccountDao bankAccountDao;

    @Test
    public void faker() {
        for (int i = 1; i <= 1000; i++) {
            Faker faker = new Faker();
            User user = new User();
            user.setName(faker.name().name());
            user.setRoles(new HashSet<>(Collections.singletonList("test")));
            user.setAge(faker.random().nextInt(20, 50));
            user.setCountry("中国");
            user.setProvince("a");
            user.setDishonest(false);
            user.setEmployment(Employment.Employed);
            user.setGender(Gender.Male);
            user.setIDNumber(faker.idNumber().toString());
            user.setOverDual(0L);

            user.setUsername("user" + i);

            String encodedPassword = new BCryptPasswordEncoder().encode("000000");
            user.setPassword(encodedPassword);

            user.setYearIncome(10000L);
            userDao.save(user);

            Faker faker2 = new Faker();
            BankAccount bankAccount = new BankAccount();
            bankAccount.setId(faker2.random().nextLong());
            bankAccount.setBankAccountSN(faker2.random().nextLong());
            bankAccount.setBalance(1000000L);
            bankAccount.setUserID(user.getId());
            bankAccountDao.save(bankAccount);

            //Faker faker3 = new Faker();
            //BankAccount bankAccount2 = new BankAccount();
            //bankAccount.setId(faker3.random().nextLong());
            //bankAccount.setBankAccountSN(faker3.random().nextLong());
            //bankAccount.setBalance(faker3.random().nextInt(1, 180000));
            //bankAccount.setUserID(user.getId());
            //bankAccountDao.save(bankAccount2);
        }

        List<User> users = userDao.findAll();
        System.out.println(users);

    }

    @Test
    public void generateAccounts() {
        Faker faker2 = new Faker();
        BankAccount bankAccount = new BankAccount();
        bankAccount.setId(1L);
        bankAccount.setBankAccountSN(faker2.random().nextLong());
        bankAccount.setBalance(faker2.random().nextInt(1, 180000));
        bankAccount.setUserID(1L);
        bankAccountDao.save(bankAccount);
    }
}
