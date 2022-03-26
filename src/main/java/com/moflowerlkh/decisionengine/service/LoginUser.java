package com.moflowerlkh.decisionengine.service;

import com.alibaba.fastjson.annotation.JSONField;
import com.moflowerlkh.decisionengine.domain.User;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Set;
import java.util.stream.Collectors;

@Data
@NoArgsConstructor
public class LoginUser implements UserDetails {

    private User user;

    // 不序列化到redis里
    @JSONField(serialize = false)
    private Set<SimpleGrantedAuthority> cachedRoles;

    public LoginUser(User user) {
        System.out.println("新建用户holder: " + user);
        this.user = user;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        if (this.cachedRoles == null) {
            this.cachedRoles = this.user.getRoles().stream().map(SimpleGrantedAuthority::new)
                    .collect(Collectors.toSet());
        }
        return this.cachedRoles;
    }

    @Override
    public String getPassword() {
        return user.getPassword();
    }

    @Override
    public String getUsername() {
        return user.getUsername();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
