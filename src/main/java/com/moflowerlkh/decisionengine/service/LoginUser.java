package com.moflowerlkh.decisionengine.service;

import com.alibaba.fastjson.annotation.JSONField;
import com.moflowerlkh.decisionengine.domain.entities.User;

import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Data
@NoArgsConstructor
public class LoginUser implements UserDetails {

    private Long id;
    private String username;
    private String password;
    private Set<String> roles;

    // 不序列化到redis里
    @JSONField(serialize = false)
    private Set<SimpleGrantedAuthority> cachedRoles;

    public LoginUser(User user) {
        System.out.println("新建用户holder: " + user);
        id = user.getId();
        username = user.getUsername();
        password = user.getPassword();
        roles = user.getRoles();
        cachedRoles = user.getRoles().stream().map(SimpleGrantedAuthority::new)
                .collect(Collectors.toSet());;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        if (this.cachedRoles == null) {
            this.cachedRoles = roles.stream().map(SimpleGrantedAuthority::new)
                    .collect(Collectors.toSet());
        }
        return this.cachedRoles;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
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
